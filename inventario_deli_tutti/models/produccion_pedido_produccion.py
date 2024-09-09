from odoo import models, fields, api

class ProduccionPedidoProduccion(models.Model):
    _name = 'produccion.pedido.produccion'
    _description = 'Pedido de Producción'

    fecha_pedido = fields.Datetime(string="Fecha del Pedido", default=fields.Datetime.now, required=True)
    lineas_pedido = fields.One2many('produccion.pedido.produccion.linea', 'pedido_id', string="Líneas de Pedido")

    @api.model
    def create(self, vals):
        record = super(ProduccionPedidoProduccion, self).create(vals)
        for linea in record.lineas_pedido:
            for insumo in linea.receta_id.lineas_receta:
                self.env['inventario.pedido'].create({
                    'producto_id': insumo.producto_id.id,
                    'cantidad': insumo.cantidad * linea.cantidad,
                    'origen': 'produccion',
                    'fecha_pedido': record.fecha_pedido,
                })
        return record
