from odoo import models, fields

class CostoVariable(models.Model):
    _name = 'produccion.costos.variables'
    _description = 'Costos Variables de Pedidos Especiales'

    name = fields.Char(string="Nombre", required=True)
    costo = fields.Float(string="Costo", required=True)
    pedido_especial_id = fields.Many2one('produccion.pedidos.especiales', string="Pedido Especial")
