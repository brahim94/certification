# -*- coding: utf-8 -*-
{
    'name': "attestation",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "My Company",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',
    'images': ['static/description/icon.png'],

    # any module necessary for this one to work correctly
    'depends': ['base', 'mail', 'hr', 'hr_contract'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'data/sequence.xml',
        'report/job_report.xml',
        'report/salary_report.xml',
        'report/domiciliation_report.xml',
        'data/mail_template.xml',
        'views/job_certifica.xml',
        'views/salary_certificat.xml',
        'views/domiciliation.xml',
        'views/views.xml',
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
