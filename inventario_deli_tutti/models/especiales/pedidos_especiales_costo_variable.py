from odoo import models, fields

class PedidosEspecialesCostoVariable(models.Model):
    _name = 'produccion.pedidos.especiales.costo.variable'
    _description = 'Costo Variable en Pedido Especial'
    
    pedido_especial_id = fields.Many2one('produccion.pedidos.especiales', string="Pedido Especial", ondelete='cascade')
    costo_variable_id = fields.Many2one('produccion.costos.variables', string="Costo Variable", required=True)
    costo = fields.Float(string="Costo", related='costo_variable_id.costo', readonly=True)
    descripcion = fields.Text(string="Descripción")  # Añadir este campo si es necesario
