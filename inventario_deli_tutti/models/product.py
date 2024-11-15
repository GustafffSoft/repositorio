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
    existencia = fields.Float(string="Existencia", compute="_compute_existencia", store=True)
    minimo = fields.Float(string="Cantidad Mínima", default=0)
    maximo = fields.Float(string="Cantidad Máxima", default=0)
    image = fields.Binary(string="Imagen del Producto")

    # Agregar relación con los lotes (líneas de entrada)
    lotes_ids = fields.One2many('inventario.entrada.linea', 'producto_id', string="Lotes de Producto")

    # Campo calculado para mostrar los lotes en la vista de árbol
    lotes_info = fields.Char(string="Lotes Info", compute="_compute_lotes_info")

    @api.model
    def _get_next_item(self):
        last_product = self.search([], order='item desc', limit=1)
        return last_product.item + 1 if last_product else 1

    @api.depends('lotes_ids.cantidad')
    def _compute_existencia(self):
        for product in self:
            # Sumar las cantidades de los lotes activos
            product.existencia = sum(lote.cantidad for lote in product.lotes_ids if lote.active)

    @api.depends('lotes_ids')
    def _compute_lotes_info(self):
        for product in self:
            lotes = product.lotes_ids.mapped('lote')
            product.lotes_info = ", ".join(lotes) if lotes else "Sin Lotes"
