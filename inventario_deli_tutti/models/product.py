from odoo import models, fields, api

class Product(models.Model):
    _name = 'inventario.product'
    _description = 'Producto en Inventario'

    # Asignar la descripción como el nombre del producto
    _rec_name = 'descripcion'

    item = fields.Integer(string="Item", required=True, readonly=True, default=lambda self: self._get_next_item())
    categoria_id = fields.Many2one('inventario.categoria', string="Categoría", required=True)
    clave = fields.Char(string="Clave")
    descripcion = fields.Text(string="Descripción")
    um = fields.Char(string="Unidad de Medida", required=True)
    costo_unitario = fields.Float(string="Costo Unitario")
    existencia = fields.Float(string="Existencia")
    minimo = fields.Float(string="Cantidad Mínima", default=0)
    maximo = fields.Float(string="Cantidad Máxima", default=0)

    @api.model
    def _get_next_item(self):
        last_product = self.search([], order='item desc', limit=1)
        return last_product.item + 1 if last_product else 1

    @api.model
    def create(self, vals):
        if 'item' not in vals or vals.get('item') == 0:
            vals['item'] = self._get_next_item()
        return super(Product, self).create(vals)

    def name_get(self):
        result = []
        for record in self:
            name = record.descripcion or "Sin descripción"
            result.append((record.id, name))
        return result
