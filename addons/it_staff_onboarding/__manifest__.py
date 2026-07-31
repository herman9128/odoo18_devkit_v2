{
    'name': 'IT Staff Onboarding & Offboarding',
    'version': '18.0.1.0.0',
    'category': 'IT Management',
    'summary': 'Track staff IT assets, licenses, onboarding, and resignation history.',
    'depends': ['base', 'mail','project'],  # Inherits mail chatter and optionally core HR
    'data': [
        'security/ir.model.access.csv',
        'data/ir_sequence_data.xml',
        'views/staff_onboard_views.xml',
        'data/mail_template_data.xml',
    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}


