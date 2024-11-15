from odoo import models, fields, api
import datetime

class InventarioEntradaLinea(models.Model):
    _name = 'inventario.entrada.linea'
    _description = 'Línea de Entrada de Productos'

    producto_id = fields.Many2one('inventario.product', string="Producto", required=True)
    cantidad = fields.Float(string="Cantidad", required=True)  # Cantidad que queda disponible del lote
    cantidad_inicial = fields.Float(string="Cantidad Inicial", required=True)  # Cantidad que ingresó originalmente
    costo_unitario = fields.Float(string="Costo Unitario", required=True)
    lote = fields.Char(string="Lote")
    entrada_id = fields.Many2one('inventario.entrada', string="Entrada", ondelete='cascade')
    fecha_entrada = fields.Datetime(related='entrada_id.fecha_entrada', string="Fecha de Entrada", store=True)
    fecha_caducidad = fields.Date(string="Fecha de Caducidad", required=True)
    active = fields.Boolean(string="Activo", default=True)  # Campo agregado para archivar lotes

    @api.model
    def create(self, vals):
        # Al crear el registro, aseguramos que la cantidad inicial sea igual a la cantidad ingresada
        vals['cantidad_inicial'] = vals['cantidad']

        # Crear la línea de entrada
        linea_entrada = super(InventarioEntradaLinea, self).create(vals)

        # Verificar excedente después de crear la línea
        producto = linea_entrada.producto_id
        if producto.maximo and producto.existencia > producto.maximo:
            mensaje = f"El producto '{producto.descripcion}' ha excedido la cantidad máxima de {producto.maximo}."
            self.env['inventario.notificacion'].create({
                'producto_id': producto.id,
                'tipo': 'excedente',
                'mensaje': mensaje,
            })

        return linea_entrada

    def write(self, vals):
        # Antes de escribir los cambios, verificar si la cantidad va a ser reducida a cero
        lotes_a_mover = self.filtered(lambda l: l.cantidad > 0 and vals.get('cantidad', 0) == 0)

        # Mover los lotes al histórico antes de que su cantidad se actualice a cero
        for lote in lotes_a_mover:
            self.env['inventario.lote.historico'].create({
                'producto_id': lote.producto_id.id,
                'cantidad': lote.cantidad_inicial,  # Guardar la cantidad inicial, que fue la cantidad que ingresó originalmente
                'costo_unitario': lote.costo_unitario,
                'lote': lote.lote,
                'fecha_entrada': lote.fecha_entrada,
                'fecha_caducidad': lote.fecha_caducidad,
                'fecha_consumo': fields.Datetime.now(),  # Fecha en la cual se agotó el lote
            })

        # Aplicar los cambios (incluyendo la cantidad a cero)
        res = super(InventarioEntradaLinea, self).write(vals)

        # Después de realizar la actualización, archivar si la cantidad llega a cero
        for lote in self.filtered(lambda l: l.cantidad == 0 and l.active):
            lote.sudo().write({'active': False})

            # Crear una notificación cuando el lote se archive
            self.env['inventario.notificacion'].create({
                'producto_id': lote.producto_id.id,
                'tipo': 'agotado',
                'mensaje': f"El lote '{lote.lote}' del producto '{lote.producto_id.descripcion}' ha llegado a cero y ha sido archivado.",
            })

        return res
