from odoo import http
from odoo.http import request
import base64

class VentaProductController(http.Controller):

    # Endpoint público sin seguridad
    @http.route('/api/venta_product', type='json', auth='public', methods=['GET'], csrf=False)
    def get_venta_products(self, **kwargs):
        # Obtener todos los productos de venta
        productos = request.env['venta.product'].sudo().search([])

        # Preparar la respuesta con los productos
        productos_data = []
        for producto in productos:
            productos_data.append({
                'name': producto.name,
                'cost': producto.cost,
                'best_seller': producto.best_seller,
                'image': base64.b64encode(producto.image).decode('utf-8') if producto.image else None
            })

        return {
            'status': 'success',
            'data': productos_data
        }

    # Endpoint con seguridad para referencia futura
    # @http.route('/api/venta_product', type='json', auth='user', methods=['GET'], csrf=False)
    # def get_venta_products_secure(self, **kwargs):
    #     # Asegurarse de que el usuario tiene permisos para leer los productos
    #     if not request.env.user.has_group('base.group_user'):
    #         return {"error": "No tienes permisos para acceder a esta información."}
    #
    #     # Obtener todos los productos de venta
    #     productos = request.env['venta.product'].sudo().search([])
    #
    #     # Preparar la respuesta con los productos
    #     productos_data = []
    #     for producto in productos:
    #         productos_data.append({
    #             'name': producto.name,
    #             'cost': producto.cost,
    #             'best_seller': producto.best_seller,
    #             'image': base64.b64encode(producto.image).decode('utf-8') if producto.image else None
    #         })
    #
    #     return {
    #         'status': 'success',
    #         'data': productos_data
    #     }
