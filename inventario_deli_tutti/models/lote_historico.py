from odoo import models, fields, api
import datetime

class LoteHistorico(models.Model):
    _name = 'inventario.lote.historico'
    _description = 'Lote Histórico'

    producto_id = fields.Many2one('inventario.product', string="Producto", required=True)
    cantidad = fields.Float(string="Cantidad")
    costo_unitario = fields.Float(string="Costo Unitario")
    lote = fields.Char(string="Lote")
    fecha_entrada = fields.Datetime(string="Fecha de Entrada")
    fecha_caducidad = fields.Date(string="Fecha de Caducidad")
    fecha_consumo = fields.Datetime(string="Fecha de Consumo", default=lambda self: datetime.datetime.now())

