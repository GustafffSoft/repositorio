from odoo import models, fields, api
from odoo.exceptions import UserError
import logging

_logger = logging.getLogger(__name__)


class InventarioSalidaLinea(models.Model):
    _name = 'inventario.salida.linea'
    _description = 'Línea de Salida de Productos'

    producto_id = fields.Many2one('inventario.product', string="Producto", required=True)
    cantidad = fields.Float(string="Cantidad", required=True)
    detalles = fields.Text(string="Detalles")
    salida_id = fields.Many2one('inventario.salida', string="Salida", ondelete='cascade')
    lote_id = fields.Many2one('inventario.entrada.linea', string="Lote de Entrada")

    @api.model
    def create(self, vals):
        producto = self.env['inventario.product'].browse(vals['producto_id'])

        # Calcular la cantidad disponible que no está asociada a lotes (existencia inicial)
        cantidad_inicial_disponible = producto.existencia

        # Calcular la cantidad total en lotes
        lotes = self.env['inventario.entrada.linea'].search([
            ('producto_id', '=', producto.id),
            ('cantidad', '>', 0)  # Filtrar solo lotes con cantidad disponible
        ], order='fecha_entrada asc')

        cantidad_total_en_lotes = sum(lote.cantidad for lote in lotes)

        # Determinar la cantidad total disponible (inicial + lotes)
        cantidad_disponible = cantidad_inicial_disponible + cantidad_total_en_lotes

        cantidad_necesaria = vals['cantidad']

        if cantidad_necesaria > cantidad_disponible:
            mensaje = f"Advertencia: Estás intentando dar salida a {cantidad_necesaria} unidades de '{producto.descripcion}', pero solo hay {cantidad_disponible} unidades disponibles en stock."
            _logger.warning(mensaje)
            raise UserError(mensaje)

        # Primero utilizar la existencia inicial (que no está en lotes)
        if cantidad_necesaria <= cantidad_inicial_disponible:
            producto.existencia -= cantidad_necesaria
            cantidad_necesaria = 0
        else:
            cantidad_necesaria -= cantidad_inicial_disponible
            producto.existencia = 0

        # Descontar la cantidad de los lotes, comenzando por los más antiguos
        for lote in lotes:
            if cantidad_necesaria <= 0:
                break
            if cantidad_necesaria <= lote.cantidad:
                lote.cantidad -= cantidad_necesaria
                vals['lote_id'] = lote.id
                cantidad_necesaria = 0
            else:
                cantidad_necesaria -= lote.cantidad
                lote.cantidad = 0


                # Verificación para notificación de escasez
        if producto.minimo and producto.existencia < producto.minimo:
            mensaje = f"El producto '{producto.descripcion}' ha bajado por debajo del mínimo de {producto.minimo}. Existencia actual: {producto.existencia}."
            self.env['inventario.notificacion'].create({
                  'producto_id': producto.id,
                  'tipo': 'escasez',
                  'mensaje': mensaje,
                })

        return super(InventarioSalidaLinea, self).create(vals)
