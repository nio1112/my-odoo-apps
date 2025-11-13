{
    'name': 'Ask Management',
    'version': '1.3',  # 适配弹窗新建问货单
    'summary': 'Manage customer ask and procurement process.',
    'description': """
        This module implements the "Ask" functionality to support periodic material requirements collection from customers,
        aggregate them by material to form procurement references, and improve stocking accuracy.
    """,
    'author': 'CodeBuddy',
    'website': 'https://github.com/your-org/odoo-ask',
    'license': 'LGPL-3',
    'category': 'Sales/Inventory',
    'depends': [
        'base',
        'stock',
        'purchase',
        'sale_management',
        'product',
        'mail',
        'account',
    ],
    'data': [
        'security/ask_security.xml',
        'security/ir.model.access.csv',
        'data/sequence.xml',
        'views/ask_views.xml',
        'views/ask_wizard_views.xml',
        'views/reservation_views.xml',
        'views/procurement_dashboard.xml',
        'data/cron_data.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'odoo_ask/static/src/css/ask_form_view.css',
            'odoo_ask/static/src/js/ask_create_dialog.js',
        ],
    },
    'installable': True,
    'application': True,
    'auto_install': False,
    'post_init_hook': 'post_init_hook',
}