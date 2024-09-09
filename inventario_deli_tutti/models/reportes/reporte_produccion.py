from odoo import models, fields, api

import logging

class ReporteProduccion(models.AbstractModel):
    _name = 'report.inventario_deli_tutti.report_produccion'
    _description = 'Reporte de Producción'

    def _get_report_values(self, docids, data=None):
        # Inicializa el logger
        _logger = logging.getLogger(__name__)
        
        # Si docids está vacío, obtenemos todos los pedidos de producción
        if not docids:
            pedidos = self.env['produccion.pedido.produccion'].search([])
        else:
            pedidos = self.env['produccion.pedido.produccion'].browse(docids)
        
        # Loggea la cantidad de pedidos y sus IDs
        _logger.info(f"Pedidos obtenidos: {len(pedidos)}")
        _logger.info(f"IDs de los pedidos: {pedidos.ids}")
        
        return {
            'docs': pedidos,
        }