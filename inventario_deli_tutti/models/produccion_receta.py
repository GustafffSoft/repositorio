from odoo import models, fields, api

class ProduccionReceta(models.Model):
    _name = 'produccion.receta'
    _description = 'Receta de Producción'

    name = fields.Char(string="Nombre de la Receta", required=True)
    tamano = fields.Char(string="Tamaño", required=True)
    sabor = fields.Char(string="Sabor", required=True)
    lineas_receta = fields.One2many('produccion.receta.linea', 'receta_id', string="Insumos")
    subrecetas_rel = fields.One2many('produccion.receta.subreceta', 'receta_id', string="Sub-Recetas")
    costo_por_producto = fields.Float(string="Costo por Producto", compute='_compute_costo_por_producto', store=True, recursive=True)
    precio_de_venta = fields.Float(string="Precio de Venta")

    @api.depends('lineas_receta.cantidad', 'lineas_receta.producto_id.costo_unitario', 'subrecetas_rel.cantidad', 'subrecetas_rel.subreceta_id.costo_por_producto')
    def _compute_costo_por_producto(self):
        for receta in self:
            # Calcular el costo de los insumos directos
            costo_total = sum(linea.cantidad * linea.producto_id.costo_unitario for linea in receta.lineas_receta)
            
            # Calcular el costo de las sub-recetas en base a la cantidad
            costo_total += sum(subreceta_rel.cantidad * subreceta_rel.subreceta_id.costo_por_producto for subreceta_rel in receta.subrecetas_rel)
            
            receta.costo_por_producto = costo_total
