{
    'name': 'Public Delivery Note Signature',
    'version': '18.0.1.0.0',
    'category': 'Inventory',
    'summary': 'Allows customers to sign delivery confirmations via public web link',
    'depends': ['stock', 'website'],
    'data': [
        'views/stock_picking_views.xml',  
        'views/delivery_portal_templates.xml',
    ],
    'installable': True,
    'application': False,
    'license': 'LGPL-3',
}
