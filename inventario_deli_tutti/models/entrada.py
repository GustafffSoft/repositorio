from odoo import models, fields, api
import datetime

class InventarioEntrada(models.Model):
    _name = 'inventario.entrada'
    _description = 'Entrada de Productos'

    numero_factura = fields.Char(string="Número de Factura", required=True, copy=False, readonly=True, default='Nuevo')
    proveedor_id = fields.Many2one('inventario.contacto_proveedor', string="Proveedor", required=True)
    fecha_entrada = fields.Datetime(string="Fecha de Entrada", default=lambda self: datetime.datetime.now(), required=True)
    lineas_entrada = fields.One2many('inventario.entrada.linea', 'entrada_id', string="Líneas de Entrada")
    factura_imagen = fields.Binary(string="Imagen de Factura")  # Campo para la imagen de la factura
    concepto = fields.Char(string="Concepto", required=False)  # Campo para almacenar el concepto
    numero_factura_proveedor = fields.Char(string="Número de Factura Proveedor")  # Campo opcional
    total_costo = fields.Float(string="Total de Costo", compute="_compute_total_costo", store=True)

    # Campo calculado para mostrar la información de los productos ingresados
    productos_info = fields.Char(string="Productos Info", compute="_compute_productos_info")

    @api.depends('lineas_entrada')
    def _compute_productos_info(self):
        for entrada in self:
            info = []
            for linea in entrada.lineas_entrada:
                info.append(f"{linea.producto_id.descripcion} ({linea.cantidad}) - Cad: {linea.fecha_caducidad}")
            entrada.productos_info = "; ".join(info) if info else "Sin Productos"

    @api.model
    def create(self, vals):
        if vals.get('numero_factura', 'Nuevo') == 'Nuevo':
            current_date = datetime.datetime.now()
            year_month = current_date.strftime('%Y%m')
            sequence = self.env['ir.sequence'].next_by_code('inventario.entrada') or '001'
            vals['numero_factura'] = f'ALM-{year_month}-{sequence}'
        return super(InventarioEntrada, self).create(vals)
  
  
    @api.depends('lineas_entrada.cantidad', 'lineas_entrada.costo_unitario')
    def _compute_total_costo(self):
        for entrada in self:
            entrada.total_costo = sum(linea.cantidad * linea.costo_unitario for linea in entrada.lineas_entrada)
