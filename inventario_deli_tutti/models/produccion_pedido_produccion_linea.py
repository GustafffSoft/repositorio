from odoo import models, fields, api
from odoo.exceptions import ValidationError

class ProduccionPedidoProduccionLinea(models.Model):
    _name = 'produccion.pedido.produccion.linea'
    _description = 'Línea de Pedido de Producción'

    pedido_id = fields.Many2one('produccion.pedido.produccion', string="Pedido", ondelete='cascade')
    receta_id = fields.Many2one('produccion.receta', string="Receta", required=True)
    cantidad = fields.Float(string="Cantidad", required=True)

    _sql_constraints = [
        ('unique_receta_per_pedido', 'UNIQUE(pedido_id, receta_id)', 'No se puede repetir la misma receta en un pedido de producción.')
    ]

    @api.constrains('receta_id')
    def _check_unique_receta(self):
        for record in self:
            other_lines = self.search([('pedido_id', '=', record.pedido_id.id), ('receta_id', '=', record.receta_id.id), ('id', '!=', record.id)])
            if other_lines:
                raise ValidationError("No se puede repetir la misma receta en un pedido de producción.")
