from odoo import models, fields

class Categoria(models.Model):
    _name = 'inventario.categoria'
    _description = 'Categoría de Productos'

    name = fields.Char(string="Nombre de la Categoría", required=True)
    descripcion = fields.Text(string="Descripción")

    def name_get(self):
        result = []
        for record in self:
            name = record.name or "Sin nombre"
            result.append((record.id, name))
        return result
