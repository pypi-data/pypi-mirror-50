# Copyright (C) 2018 - TODAY, Open Source Integrators
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Field Service - Repair',
    'summary': 'Integrate FSM orders with MRP repair orders',
    'version': '12.0.1.0.0',
    'category': 'Field Service',
    'author': 'Open Source Integrators, Odoo Community Association (OCA)',
    'website': 'https://github.com/OCA/field-service',
    'depends': [
        'fieldservice_stock',
        'repair',
    ],
    'data': [
        'views/fsm_order_view.xml'
    ],
    'license': 'AGPL-3',
    'development_status': 'Beta',
    'maintainers': [
        'smangukiya',
        'max3903',
    ],
    'installable': True,
}
