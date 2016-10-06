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
 
    discount1_percent = fields.Float('Discount', digits=dp.get_precision('Discount Percent'),digits_compute=dp.get_precision('Discount Percent'))
    discount2_percent = fields.Float('Second discount', digits=dp.get_precision('Discount Percent'),digits_compute=dp.get_precision('Discount Percent') )
       
    def on_change_line_discount_total(self, cr, user, ids, discount_total, price_unit, global_discount_percent, quantity,context=None ):
        if price_unit:
            discount1_percent = 100.00*discount_total/(quantity*price_unit*(100.00-global_discount_percent)/100.00)
        else:
            discount1_percent = 0.00
        return {'value':{'discount1_percent':discount1_percent}}

