{
    'name': 'Your Custom Addon Name',
    'version': '18.0.1.0.0',
    'depends': [
        'base',
        'mail',
        'helpdesk_mgmt',  # <-- CRITICAL: Tells Odoo to load helpdesk.ticket FIRST
    ],
    'data': [
        # your XML view files
    ],
    'installable': True,
}