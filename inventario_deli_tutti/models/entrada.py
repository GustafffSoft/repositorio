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
    concepto = fields.Char(string="Concepto")  # Campo para almacenar el concepto
    numero_factura_proveedor = fields.Char(string="Número de Factura Proveedor")  # Campo opcional

    @api.model
    def create(self, vals):
        if vals.get('numero_factura', 'Nuevo') == 'Nuevo':
            # Generación del número de factura en base a la estructura sugerida
            current_date = datetime.datetime.now()
            year_month = current_date.strftime('%Y%m')
            sequence = self.env['ir.sequence'].next_by_code('inventario.entrada') or '001'
            vals['numero_factura'] = f'ALM-{year_month}-{sequence}'
        return super(InventarioEntrada, self).create(vals)
