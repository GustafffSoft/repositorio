from odoo import models, fields, api
from odoo.exceptions import UserError

class InventarioSalidaLinea(models.Model):
    _name = 'inventario.salida.linea'
    _description = 'Línea de Salida de Productos'

    producto_id = fields.Many2one('inventario.product', string="Producto", required=True)
    cantidad = fields.Float(string="Cantidad", required=True)
    detalles = fields.Text(string="Detalles")
    salida_id = fields.Many2one('inventario.salida', string="Salida", ondelete='cascade')
    lote_id = fields.Many2one('inventario.entrada.linea', string="Lote de Entrada")

    @api.model
    def create(self, vals):
        producto = self.env['inventario.product'].browse(vals['producto_id'])

        # Obtener los lotes disponibles del producto, ordenados por fecha de caducidad y luego por fecha de entrada (FIFO)
        lotes = self.env['inventario.entrada.linea'].search([
            ('producto_id', '=', producto.id),
            ('cantidad', '>', 0),
            ('active', '=', True)  # Filtrar solo lotes activos
        ], order='fecha_caducidad asc, fecha_entrada asc')

        cantidad_necesaria = vals['cantidad']

        if cantidad_necesaria > sum(lote.cantidad for lote in lotes):
            mensaje = f"Advertencia: Estás intentando dar salida a {cantidad_necesaria} unidades de '{producto.descripcion}', pero no hay suficiente cantidad en stock."
            raise UserError(mensaje)

        cantidad_restante = cantidad_necesaria

        for lote in lotes:
            if cantidad_restante <= 0:
                break

            if cantidad_restante <= lote.cantidad:
                # Reducir la cantidad del lote disponible
                lote.sudo().write({'cantidad': lote.cantidad - cantidad_restante})

                # Asignar el lote al registro de salida
                vals['lote_id'] = lote.id

                cantidad_restante = 0
            else:
                # Si la cantidad restante es mayor a la cantidad del lote actual, consumir completamente el lote
                cantidad_consumida = lote.cantidad
                lote.sudo().write({'cantidad': 0})

                # Asignar el lote al registro de salida (se guardará solo el último lote completamente consumido)
                vals['lote_id'] = lote.id
                cantidad_restante -= cantidad_consumida

                # Archivar el lote cuando se agote
                lote.sudo().write({'active': False})

                # Crear notificación de agotamiento del lote
                self.env['inventario.notificacion'].create({
                    'producto_id': lote.producto_id.id,
                    'tipo': 'agotado',
                    'mensaje': f"El lote '{lote.lote}' del producto '{lote.producto_id.descripcion}' ha llegado a cero y ha sido archivado.",
                })

        # Crear la línea de salida
        salida_linea = super(InventarioSalidaLinea, self).create(vals)

        return salida_linea
