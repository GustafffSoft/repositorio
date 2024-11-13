from odoo import models, fields

class VentaProduct(models.Model):
    _name = 'venta.product'
    _description = 'Venta Product'

    name = fields.Char(string='Nombre del producto', required=True)
    image = fields.Binary(string='Imagen del producto')
    cost = fields.Float(string='Costo del producto', required=True)
    best_seller = fields.Boolean(string='Más vendido', default=False)