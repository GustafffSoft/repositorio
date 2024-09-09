from odoo import models, fields, api
from odoo.exceptions import ValidationError



class ProduccionPedidoHornoLinea(models.Model):
    _name = 'produccion.pedido.horno.linea'
    _description = 'Línea de Pedido de Horno'

    pedido_id = fields.Many2one('produccion.pedido.horno', string="Pedido", ondelete='cascade')
    receta_id = fields.Many2one('produccion.receta', string="Receta", required=True)
    cantidad = fields.Float(string="Cantidad", required=True)

    _sql_constraints = [
        ('unique_receta_per_pedido', 'UNIQUE(pedido_id, receta_id)', 'No se puede repetir la misma receta en un pedido de horno.')
    ]

    @api.constrains('receta_id')
    def _check_unique_receta(self):
        for record in self:
            other_lines = self.search([('pedido_id', '=', record.pedido_id.id), ('receta_id', '=', record.receta_id.id), ('id', '!=', record.id)])
            if other_lines:
                raise ValidationError("No se puede repetir la misma receta en un pedido de horno.")