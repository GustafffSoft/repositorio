from odoo import models, fields

class ProduccionRecetaLinea(models.Model):
    _name = 'produccion.receta.linea'
    _description = 'Línea de Insumo de Receta'

    receta_id = fields.Many2one('produccion.receta', string="Receta", ondelete='cascade')
    producto_id = fields.Many2one('inventario.product', string="Producto", required=True)
    clave_mp = fields.Char(string="Clave MP", related='producto_id.clave', store=True, readonly=True)
    cantidad = fields.Float(string="Cantidad", required=True)
    um = fields.Selection(
    selection=[
        ('kg', 'Kilogramos (KG)'),
        ('lt', 'Litros (LT)'),
        ('Pzs', 'Piezas (Pz)'),
    ],
    string="Unidad de Medida",
    related='producto_id.um',
    store=True
)
