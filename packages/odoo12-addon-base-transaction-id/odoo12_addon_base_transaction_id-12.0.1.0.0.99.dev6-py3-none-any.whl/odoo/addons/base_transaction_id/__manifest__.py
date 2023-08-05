# Copyright 2019 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)

{
    "name": "Base transaction ID for financial institutes",
    "version": "12.0.1.0.0",
    "author": "Camptocamp,Odoo Community Association (OCA)",
    "maintainer": "Camptocamp",
    "category": "Hidden/Dependency",
    "depends": [
        "sale",
    ],
    "website": "https://github.com/OCA/account-reconcile",
    "data": [
        "views/invoice.xml",
        "views/sale.xml",
        "views/account_move_line.xml",
    ],
    "qweb": [
        "static/src/xml/account_reconciliation.xml",
    ],
    "installable": True,
    "license": "AGPL-3",
}
