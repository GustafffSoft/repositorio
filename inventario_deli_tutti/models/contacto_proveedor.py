from odoo import models, fields

class ContactoProveedor(models.Model):
    _name = 'inventario.contacto_proveedor'
    _description = 'Contacto de Proveedor'

    # Campo utilizado como nombre de referencia
    name = fields.Char(string="Nombre", required=True)
    telefono = fields.Char(string="Teléfono")
    correo = fields.Char(string="Correo Electrónico")
    direccion = fields.Char(string="Dirección")
    ciudad = fields.Char(string="Ciudad")
    pais = fields.Char(string="País")
    notas = fields.Text(string="Notas")
