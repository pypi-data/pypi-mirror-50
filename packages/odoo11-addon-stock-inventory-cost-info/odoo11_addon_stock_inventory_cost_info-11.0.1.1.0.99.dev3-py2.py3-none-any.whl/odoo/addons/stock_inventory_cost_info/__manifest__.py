# Copyright 2019 Tecnativa - Ernesto Tejeda
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Stock Inventory Cost Info",
    "summary": "Shows the cost of the inventory adjustments",
    "version": "11.0.1.1.0",
    "author": "Tecnativa, "
              "Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/stock-logistics-warehouse",
    "category": "Warehouse Management",
    "depends": [
        "stock",
    ],
    "data": [
        "views/stock_inventory_views.xml",
        "views/report_stockinventory.xml",
    ],
    "pre_init_hook": "pre_init_hook",
    "license": "AGPL-3",
    'installable': True,
    'application': False,
}
