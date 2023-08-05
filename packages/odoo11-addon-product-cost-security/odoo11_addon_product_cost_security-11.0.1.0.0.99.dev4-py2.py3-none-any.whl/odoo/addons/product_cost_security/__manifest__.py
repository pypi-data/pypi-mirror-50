# Copyright 2018 Tecnativa - Sergio Teruel
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    'name': 'Product Cost Security',
    'summary': 'Product cost security restriction view',
    'version': '11.0.1.0.0',
    'development_status': 'Beta',
    'category': 'Product',
    'website': 'https://github.com/OCA/product-attribute',
    'author': 'Tecnativa, Odoo Community Association (OCA)',
    'license': 'AGPL-3',
    'application': False,
    'installable': True,
    'depends': [
        'product',
    ],
    'data': [
        'security/product_cost_security.xml',
        'views/product_views.xml',
    ],
}
