from odoo import models, api, fields
import logging
from datetime import datetime, timedelta

class ReporteSalida(models.AbstractModel):
    _name = 'report.inventario_deli_tutti.report_salida'
    _description = 'Reporte de Salida de Productos'

    def _get_report_values(self, docids, data=None):
        _logger = logging.getLogger(__name__)

        # Obtener el primer y último día del mes actual con horas
        fecha_inicio = datetime.combine(datetime.today().replace(day=1), datetime.min.time())
        fecha_fin = datetime.combine((fecha_inicio + timedelta(days=31)).replace(day=1) - timedelta(days=1), datetime.max.time())

        _logger.info("-----------------------------------------------------------------------------------------------------------")
        _logger.info(f"Filtrando salidas entre {fecha_inicio} y {fecha_fin}")

        salidas = self.env['inventario.salida'].search([
            ('fecha_salida', '>=', fecha_inicio),
            ('fecha_salida', '<=', fecha_fin)
        ])

        _logger.info(f"Salidas encontradas: {len(salidas)}")

        return {
            'docs': salidas,
            'fecha_inicio': fecha_inicio.strftime('%Y-%m-%d'),
            'fecha_fin': fecha_fin.strftime('%Y-%m-%d'),
        }
