# Copyright 2014 Guewen Baconnier (Camptocamp SA)
# Copyright 2013-2014 Nicolas Bessi (Camptocamp SA)
# Copyright 2018 Qubiq - Xavier Jiménez
# Copyright 2018 Tecnativa - Pedro M. Baeza
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{'name': 'Account Invoice Comments',
 'summary': 'Comments templates on invoice documents',
 'version': '11.0.1.0.0',
 'depends': [
     'account',
     'base_comment_template',
 ],
 'author': "Camptocamp, "
           "Tecnativa, "
           "Odoo Community Association (OCA)",
 "license": "AGPL-3",
 'data': ['views/account_invoice_view.xml',
          'views/base_comment_template_view.xml',
          'security/ir.model.access.csv',
          'views/report_invoice.xml',
          'views/res_partner_views.xml',
          ],
 'category': 'Sale',
 'installable': True,
 }
