from odoo import models, fields, api

class PedidosEspeciales(models.Model):
    _name = 'produccion.pedidos.especiales'
    _description = 'Pedidos Especiales'

    name = fields.Char(string="Nombre del Pedido Especial", required=True)
    fecha_pedido = fields.Datetime(string="Fecha del Pedido", default=fields.Datetime.now, required=True, readonly=True)
    fecha_entrega = fields.Datetime(string="Fecha de Entrega")
    direccion_entrega = fields.Char(string="Dirección de Entrega")  # Dirección como un campo de texto
    imagen_pedido = fields.Image(string="Imagen del Pedido")  # Imagen del pedido
    numero_pedido = fields.Char(string="Número de Pedido")
    costo_venta_pastel = fields.Float(string="Costo de Venta del Pastel", required=False)
    total_costo = fields.Float(string="Costo Total", compute="_compute_total_costo", store=True)
    
    lineas_receta = fields.One2many('produccion.pedidos.especiales.linea.receta', 'pedido_especial_id', string="Líneas de Receta")
    costos_variables = fields.One2many('produccion.pedidos.especiales.costo.variable', 'pedido_especial_id', string="Costos Variables")

    @api.depends('lineas_receta.subtotal', 'costos_variables.costo')
    def _compute_total_costo(self):
        for pedido in self:
            total = sum(linea.subtotal for linea in pedido.lineas_receta)
            total += sum(costo.costo for costo in pedido.costos_variables)
            pedido.total_costo = total

    @api.model
    def create(self, vals):
        # Crear el pedido especial
        record = super(PedidosEspeciales, self).create(vals)
        
        # Generar registros en el inventario basado en las líneas de receta
        for linea_receta in record.lineas_receta:
            for linea in linea_receta.receta_id.lineas_receta:
                # Calcular la cantidad total de cada producto necesario
                cantidad_total = linea.cantidad * linea_receta.cantidad
                
                # Crear el registro en inventario
                self.env['inventario.pedido'].create({
                    'producto_id': linea.producto_id.id,
                    'cantidad': cantidad_total,
                    'origen': 'pedido_especial',
                    'fecha_pedido': record.fecha_pedido,
                })
        
        return record