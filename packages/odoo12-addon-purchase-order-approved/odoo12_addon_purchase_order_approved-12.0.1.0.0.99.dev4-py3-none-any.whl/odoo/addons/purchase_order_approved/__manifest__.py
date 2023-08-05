# Copyright 2017 Eficent Business and IT Consulting Services S.L.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "Purchase Order Approved",
    "summary": "Add a new state 'Approved' in purchase orders.",
    "version": "12.0.1.0.0",
    "category": "Purchases",
    "website": "https://github.com/OCA/purchase-workflow",
    "author": "Eficent, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "depends": [
        "purchase_stock",
    ],
    "data": [
        "views/purchase_order_view.xml",
        "views/res_config_view.xml",
    ],
}
