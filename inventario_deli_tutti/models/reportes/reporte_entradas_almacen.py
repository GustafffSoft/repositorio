from odoo import models

class ReporteEntradasAlmacen(models.AbstractModel):
    _name = 'report.inventario_deli_tutti.report_entradas'

    def _get_report_values(self, docids, data=None):
        if not docids:
            docids = self.env['inventario.entrada'].search([]).ids
        entradas = self.env['inventario.entrada'].browse(docids)

        entradas_con_productos = []
        for entrada in entradas:
            productos = []
            for linea in entrada.lineas_entrada:
                productos.append({
                    'producto': linea.producto_id.descripcion,  # Usar 'descripcion' para mostrar el nombre del producto
                    'cantidad': linea.cantidad,
                    'costo_unitario': linea.costo_unitario,
                })

            entradas_con_productos.append({
                'fecha': entrada.fecha_entrada,
                'numero_factura': entrada.numero_factura,
                'numero_factura_proveedor': entrada.numero_factura_proveedor,
                'concepto': entrada.concepto,
                'productos': productos,
            })

        company_name = "Deli Tutti"
        logo_url = '/inventario_deli_tutti/static/src/img/logo.jpg'

        return {
            'docs': entradas_con_productos,
            'company_name': company_name,
            'logo_url': logo_url,
        }
