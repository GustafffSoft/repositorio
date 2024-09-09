from odoo import models, fields


class ProduccionRecetaSubreceta(models.Model):
    _name = 'produccion.receta.subreceta'
    _description = 'Subrecetas de Producción'

    receta_id = fields.Many2one('produccion.receta', string="Receta", required=True, ondelete='cascade')
    subreceta_id = fields.Many2one('produccion.receta', string="Sub-Receta", required=True)
    cantidad = fields.Float(string="Cantidad", required=True, default=1.0)
    name = fields.Char(string="Nombre", related='subreceta_id.name', store=True)