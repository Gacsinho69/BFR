# -*- coding: utf-8 -*-
{
    'name': 'BAUFER Base',
    'version': '18.0.1.0.0',
    'category': 'Industries',
    'summary': 'Módulo base para BAUFER - Configuraciones y extensiones core',
    'description': """
        BAUFER Base Module
        ==================
        Módulo base para el sistema ERP de BAUFER (Inversiones Séneca SpA).

        Funcionalidades principales:
        * Extensión de res.partner con datos comerciales específicos
        * Extensión de product.template con información de repuestos
        * Gestión de marcas (Caterpillar, Komatsu, etc.)
        * Gestión de regiones de Chile con foco en zonas mineras
        * Configuraciones globales BAUFER

        Empresa: Inversiones Séneca SpA (BAUFER)
        Sector: Importación y venta de repuestos para motores diesel, gasolina y gas
        Mercado: Empresas de arriendo de maquinaria pesada - Sector minero
    """,
    'author': 'BAUFER',
    'website': 'https://www.baufer.cl',
    'license': 'LGPL-3',
    'depends': [
        'base',
        'product',
        'stock',
        'sale',
        'purchase',
        'contacts',
    ],
    'data': [
        # Security
        'security/ir.model.access.csv',

        # Data
        'data/product_brands.xml',
        'data/product_categories.xml',
        'data/regions.xml',

        # Views
        'views/res_partner_views.xml',
        'views/product_views.xml',
    ],
    'demo': [],
    'installable': True,
    'application': True,
    'auto_install': False,
}
