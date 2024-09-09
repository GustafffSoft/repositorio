from odoo import models, fields, api
import datetime

class InventarioSalida(models.Model):
    _name = 'inventario.salida'
    _description = 'Salida de Productos'

    fecha_salida = fields.Datetime(string="Fecha de Salida", default=lambda self: datetime.datetime.now(), required=True)
    lineas_salida = fields.One2many('inventario.salida.linea', 'salida_id', string="Líneas de Salida")

