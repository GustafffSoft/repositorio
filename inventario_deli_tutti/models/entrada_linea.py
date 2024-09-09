from odoo import models, fields, api
import datetime

class InventarioEntradaLinea(models.Model):
    _name = 'inventario.entrada.linea'
    _description = 'Línea de Entrada de Productos'

    producto_id = fields.Many2one('inventario.product', string="Producto", required=True)
    cantidad = fields.Float(string="Cantidad", required=True)
    costo_unitario = fields.Float(string="Costo Unitario", required=True)
    lote = fields.Char(string="Lote", compute="_compute_lote", store=True)
    entrada_id = fields.Many2one('inventario.entrada', string="Entrada", ondelete='cascade')
    fecha_entrada = fields.Datetime(related='entrada_id.fecha_entrada', string="Fecha de Entrada", store=True)

    @api.depends('costo_unitario')
    def _compute_lote(self):
        for record in self:
            if record.costo_unitario:
                record.lote = f"lote-{record.costo_unitario}"

    @api.model
    def create(self, vals):
        producto = self.env['inventario.product'].browse(vals['producto_id'])
        producto.existencia += vals['cantidad']
        producto.costo_unitario = vals['costo_unitario']
        
        # Verificación para notificación de excedentes
        if producto.maximo and producto.existencia > producto.maximo:
            mensaje = f"El producto '{producto.descripcion}' ha excedido la cantidad máxima de {producto.maximo}."
            self.env['inventario.notificacion'].create({
                'producto_id': producto.id,
                'tipo': 'excedente',
                'mensaje': mensaje,
            })

        return super(InventarioEntradaLinea, self).create(vals)
