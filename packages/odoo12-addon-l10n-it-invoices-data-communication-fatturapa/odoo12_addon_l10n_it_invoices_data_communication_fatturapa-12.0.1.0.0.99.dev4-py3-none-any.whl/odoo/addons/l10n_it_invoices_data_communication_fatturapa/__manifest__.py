# Copyright 2019 Lorenzo Battistini
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

{
    'name': 'ITA - Comunicazione dati fatture - '
            'Integrazione e-fattura',
    'summary': 'Integrazione fatturazione elettronica e comunicazione dati '
               'fatture (c.d. "nuovo spesometro")',
    'version': '12.0.1.0.0',
    'category': 'Hidden',
    'author': "Agile Business Group, "
              "Odoo Community Association (OCA)",
    'website': 'https://github.com/OCA/l10n-italy/',
    'license': 'LGPL-3',
    'depends': [
        'l10n_it_invoices_data_communication',
        'l10n_it_fatturapa_in',
        'l10n_it_fatturapa_out',
    ],
    'data': [
        'views/communication_view.xml'
    ],
    'installable': True,
    'auto_install': True,
}
