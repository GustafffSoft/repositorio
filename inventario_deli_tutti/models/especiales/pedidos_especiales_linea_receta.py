from odoo import models, fields, api

class PedidosEspecialesLineaReceta(models.Model):
    _name = 'produccion.pedidos.especiales.linea.receta'
    _description = 'Línea de Receta en Pedido Especial'

    pedido_especial_id = fields.Many2one('produccion.pedidos.especiales', string="Pedido Especial", ondelete='cascade')
    receta_id = fields.Many2one('produccion.receta', string="Receta", required=True)
    cantidad = fields.Float(string="Cantidad", required=True)
    subtotal = fields.Float(string="Subtotal", compute="_compute_subtotal", store=True)

    @api.depends('receta_id', 'cantidad')
    def _compute_subtotal(self):
        for linea in self:
            linea.subtotal = linea.cantidad * linea.receta_id.costo_por_producto
