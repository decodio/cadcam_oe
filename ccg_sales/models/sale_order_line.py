# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2016 CADCAM Design Centar d.o.o. (http://www.cadcam-group.eu/).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
import openerp.addons.decimal_precision as dp
from openerp import models, fields, api, _
from openerp.exceptions import Warning 
import calendar
from datetime import datetime


class SaleOrderLine(models.Model):
    _name = 'sale.order.line'
    _inherit = ['sale.order.line'] 

    discount1_percent = fields.Float('Discount_percent', digits=dp.get_precision('Discount Percent'),digits_compute=dp.get_precision('Discount Percent'))
    discount2_percent = fields.Float('Second discount_percent', digits=dp.get_precision('Discount Percent'),digits_compute=dp.get_precision('Discount Percent') )
    amount1 = fields.Float('Amount1', digits=dp.get_precision('Account'),digits_compute=dp.get_precision('Discount Percent'))
    amount2 = fields.Float('Amount2', digits=dp.get_precision('Account'),digits_compute=dp.get_precision('Discount Percent'))

    def on_change_amount(self,cr,user,ids, amount1, amount2, discount2_percent, price_unit, quantity, context=None ):
        if not (price_unit and quantity):
            return {}
        disc1 = 100 - (100 * amount1)/price_unit/quantity
        amount2 = price_unit * quantity*(100 - disc1) / 100 *(100 - discount2_percent) / 100
        return { 'value': {'discount1_percent':disc1,'amount2':amount2, 'quantity':quantity}}

    def on_change_discount_percent(self,cr,user, ids, discount1_percent, discount2_percent, price_unit, quantity, context=None ):
        amount1 = price_unit * quantity*(100 - discount1_percent) / 100
        amount2 = price_unit * quantity*(100 - discount1_percent) / 100 *(100 - discount2_percent) / 100
        return { 'value':{'amount1':amount1,'amount2':amount2, 'quantity':quantity}}
    