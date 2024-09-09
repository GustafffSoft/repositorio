from odoo import models, fields, api

class ProduccionPedidoHorno(models.Model):
    _name = 'produccion.pedido.horno'
    _description = 'Pedido de Horno'

    fecha_pedido = fields.Datetime(string="Fecha del Pedido", default=fields.Datetime.now, required=True)
    lineas_pedido = fields.One2many('produccion.pedido.horno.linea', 'pedido_id', string="Líneas de Pedido")

    @api.model
    def create(self, vals):
        record = super(ProduccionPedidoHorno, self).create(vals)
        for linea in record.lineas_pedido:
            for insumo in linea.receta_id.lineas_receta:
                self.env['inventario.pedido'].create({
                    'producto_id': insumo.producto_id.id,
                    'cantidad': insumo.cantidad * linea.cantidad,
                    'origen': 'horno',
                    'fecha_pedido': record.fecha_pedido,
                })
        return record
