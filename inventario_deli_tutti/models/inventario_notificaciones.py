from odoo import models, fields, api

class InventarioNotificacion(models.Model):
    _name = 'inventario.notificacion'
    _description = 'Notificaciones de Inventario'

    producto_id = fields.Many2one('inventario.product', string="Producto", required=True)
    tipo = fields.Selection([('excedente', 'Excedente'), ('escasez', 'Escasez')], string="Tipo", required=True)
    mensaje = fields.Text(string="Mensaje", required=True)
    fecha = fields.Datetime(string="Fecha", default=lambda self: fields.Datetime.now(), required=True)
