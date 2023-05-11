# -*- coding: utf-8 -*-

{
    'name': 'Cinetpay Payment Acquirer',
    'category': 'Hidden',
    'summary': 'Payment Acquirer: Cinetpay Implementation',
    'version': '1.0',
    'autor': 'Innoving',
    'description': """Cinetpay Payment Acquirer""",
    'depends': ['base','account','payment','website_sale','web'],
    'data': [
        'views/payment_cinetpay_templates.xml',
        'data/journal_cinetpay_data.xml',
        'data/payment_acquirer_data.xml',
        'views/payment_views.xml',
        
    ],
    'images': ['static/description/icon.png'],
    'installable': True,
    'post_init_hook': 'create_missing_journal_for_acquirers',
    'uninstall_hook': 'uninstall_hook',
}
