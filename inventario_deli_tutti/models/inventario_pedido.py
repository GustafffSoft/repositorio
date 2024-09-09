from odoo import models, fields, api

class InventarioPedido(models.Model):
    _name = 'inventario.pedido'
    _description = 'Pedido en Inventario'

    producto_id = fields.Many2one('inventario.product', string="Producto", required=True)
    cantidad = fields.Float(string="Cantidad Total", required=True)
    origen = fields.Selection([
        ('horno', 'Pedido de Horno'),
        ('produccion', 'Pedido de Producción'),
        ('pedido_especial', 'Pedido Especial')  # Añadir la opción 'pedido_especial'
    ], string="Origen del Pedido", required=True)    
    fecha_pedido = fields.Datetime(string="Fecha del Pedido", required=True)
    estado = fields.Selection([('por_entregar', 'Por entregar'), ('entregado', 'Entregado')], string="Estado", default='por_entregar')
    um = fields.Char(string="Unidad de Medida", related='producto_id.um', store=True, readonly=True)  # Agregado este campo



    @api.model
    def create(self, vals):
        record = super(InventarioPedido, self).create(vals)
        # Inicialmente, el estado es "por_entregar", así que no se hace ninguna acción en la creación
        return record

    def write(self, vals):
        if 'estado' in vals:
            for record in self:
                if record.estado == 'por_entregar' and vals['estado'] == 'entregado':
                    # Restar del inventario porque se entrega el pedido
                    record.producto_id.existencia -= record.cantidad
                elif record.estado == 'entregado' and vals['estado'] == 'por_entregar':
                    # Sumar nuevamente al inventario porque se vuelve a "por entregar"
                    record.producto_id.existencia += record.cantidad
        return super(InventarioPedido, self).write(vals)


    def action_set_por_entregar(self):
        self.write({'estado': 'por_entregar'})

    def action_set_entregado(self):
        self.write({'estado': 'entregado'})