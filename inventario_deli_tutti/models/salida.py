from odoo import models, fields, api
import datetime

class InventarioSalida(models.Model):
    _name = 'inventario.salida'
    _description = 'Salida de Productos'

    fecha_salida = fields.Datetime(string="Fecha de Salida", default=lambda self: datetime.datetime.now(), required=True)
    lineas_salida = fields.One2many('inventario.salida.linea', 'salida_id', string="Líneas de Salida")
    productos_cantidad_resumen = fields.Text(string="Productos y Cantidades", compute="_compute_productos_cantidad_resumen")

    @api.depends('lineas_salida.producto_id', 'lineas_salida.cantidad')
    def _compute_productos_cantidad_resumen(self):
        for salida in self:
            resumen = [
                f"{linea.producto_id.descripcion}: {linea.cantidad} unidades"
                for linea in salida.lineas_salida
                if linea.producto_id and linea.cantidad > 0
            ]
            salida.productos_cantidad_resumen = ', '.join(resumen) if resumen else 'Sin productos'
