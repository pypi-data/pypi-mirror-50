# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields
from odoo.tests.common import TransactionCase


class TestStockWarehouseCalendar(TransactionCase):

    def setUp(self):
        super(TestStockWarehouseCalendar, self).setUp()
        self.move_obj = self.env['stock.move']
        self.company = self.env.ref('base.main_company')
        self.warehouse = self.env.ref('stock.warehouse0')
        self.customer_loc = self.env.ref('stock.stock_location_customers')
        self.company_partner = self.env.ref('base.main_partner')
        self.calendar = self.env.ref('resource.resource_calendar_std')
        self.warehouse.calendar_id = self.calendar
        self.warehouse_2 = self.env['stock.warehouse'].create({
            'code': 'WH-T',
            'name': 'Warehouse Test',
            'calendar_id': self.calendar.id,
        })

        self.product = self.env['product.product'].create({
            'name': 'test product',
            'default_code': 'PRD',
            'type': 'product',
        })

        route_vals = {
            'name': 'WH2 -> WH',
        }
        self.transfer_route = self.env['stock.location.route'].create(
            route_vals)
        rule_vals = {
            'location_id': self.warehouse.lot_stock_id.id,
            'location_src_id': self.warehouse_2.lot_stock_id.id,
            'action': 'move',
            'warehouse_id': self.warehouse.id,
            'propagate_warehouse_id': self.warehouse_2.id,
            'picking_type_id': self.env.ref('stock.picking_type_internal').id,
            'name': 'WH2->WH',
            'route_id': self.transfer_route.id,
            'delay': 1,
        }
        self.transfer_rule = self.env['procurement.rule'].create(rule_vals)
        self.product.route_ids = [(6, 0, self.transfer_route.ids)]

    def test_procurement_with_calendar(self):
        values = {
            'date_planned': '2097-01-07 09:00:00',  # Monday
            'warehouse_id': self.warehouse,
            'company_id': self.company,
            'rule_id': self.transfer_rule,
        }
        self.env['procurement.group'].run(
            self.product, 100,
            self.product.uom_id,
            self.warehouse.lot_stock_id, 'Test',
            'Test', values)
        move = self.env['stock.move'].search(
            [('product_id', '=', self.product.id)], limit=1)
        date_expected = fields.Datetime.from_string(move.date_expected).date()
        # Friday 4th Jan 2017
        friday = fields.Datetime.from_string('2097-01-04 09:00:00').date()

        self.assertEquals(date_expected, friday)
