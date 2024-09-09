from odoo import models
import logging
_logger = logging.getLogger(__name__)

class ReporteInventario(models.AbstractModel):
    _name = 'report.inventario_deli_tutti.report_inventario'
    _description = 'Reporte de Inventario Deli Tutti'

    def _get_report_values(self, docids, data=None):
        if not docids:
            docids = self.env['inventario.product'].search([]).ids
        productos = self.env['inventario.product'].browse(docids)
        
        productos_con_lotes = []
        total_inventario = 0
        for producto in productos:
            total_costo = 0
            lotes = []
            for linea in self.env['inventario.entrada.linea'].search([('producto_id', '=', producto.id)]):
                lotes.append({
                    'lote': linea.lote,
                    'cantidad': linea.cantidad,
                    'costo_unitario': linea.costo_unitario
                })
                total_costo += linea.cantidad * linea.costo_unitario
            
            productos_con_lotes.append({
                'item': producto.item,
                'descripcion': producto.descripcion,
                'um': producto.um,
                'existencia': producto.existencia,
                'lotes': lotes,
                'total_costo': total_costo,
            })

            total_inventario += total_costo

        # Definir el nombre de la compañía y la ruta del logo
        company_name = "Deli Tutti"
        logo_url = '/inventario_deli_tutti/static/src/img/logo.jpg'

        # Log para verificar que los valores se están pasando correctamente
        _logger.info(f"Logo URL: {logo_url}")
        _logger.info(f"Company Name: {company_name}")

        return {
            'docs': productos_con_lotes,
            'total_inventario': total_inventario,
            'company_name': company_name,
            'logo_url': logo_url,
        }



# from odoo import models

# import logging
# _logger = logging.getLogger(__name__)

# class ReporteInventario(models.AbstractModel):
#     _name = 'report.inventario_deli_tutti.report_inventario'

#     def _get_report_values(self, docids, data=None):
#         if not docids:
#             _logger.info('No docids provided, fetching all products.')
#             docids = self.env['inventario.product'].search([]).ids
#         _logger.info(f'Generating report for docids: {docids}')
#         docs = self.env['inventario.product'].browse(docids)
#         return {
#             'docs': docs,
#         }
