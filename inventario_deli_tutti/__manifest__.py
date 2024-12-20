{
    "name": "Inventario Deli Tutti",
    "version": "2.0",
    "summary": "Gestión de productos en el inventario",
    "description": "Módulo personalizado para gestionar productos en el inventario de Deli Tutti.",
    "category": "Inventory",
    "author": "GustafffSoft",
    "depends": ["base", "web"],
    "data": [
        "security/produccion_security.xml",
        "security/administrador_security.xml",
        "security/inventario_security.xml",
        "security/ir.model.access.csv",
        "views/menu_entradas_salidas.xml",        
        "views/entrada.xml",                      
        "views/salida.xml",                       
        "views/contacto_proveedor.xml",           
        "views/notificaciones_entrada_salida.xml",
        "views/receta_produccion.xml",           
        "views/produccion_pedido_horno.xml",      
        "views/pedido_produccion.xml",            
        "views/pedido_inventario.xml",
        "views/report_entradas.xml",             
        "views/report_inventario.xml",            
        "views/report_produccion.xml",            
        "views/report_salida.xml",
        "views/product_views.xml",                
        "views/productos_por_lotes_views.xml",    
        "views/lote_historico_views.xml",
        "views/especiales/costos_variables.xml",  
        "views/especiales/pedidos_especiales.xml",
        'data/cron.xml',
    ],
    "assets": {
        "web.assets_backend": [
            "inventario_deli_tutti/static/src/css/custom_styles.css"
        ]
    },
    "installable": True,
    "application": True,
    "license": "LGPL-3"
}
