{
    'name': 'Helpdesk Website Form',
    'version': '18.0.1.0.0',
    'category': 'Website',
    'summary': 'Frontend support ticket submission form for OCA Helpdesk Management',
    'license': 'LGPL-3',
    'depends': [
        'base',
        'website',
        'helpdesk_mgmt',
    ],
    'data': [
        'views/website_form_templates.xml',
        'views/helpdesk_ticket_views.xml',
    ],
    'installable': True,
    'auto_install': False,
}
