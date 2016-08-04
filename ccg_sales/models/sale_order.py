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

class SaleOrder(models.Model):
    _name = 'sale.order'
    _inherit = 'sale.order'
    
    def _delivery_time_default(self):
        return '1-2 weeks of signing the contract or order'

    def _place_of_delivery_default(self):
        return "At the user's address"

    def _payment_data_default(self):
        return "PLC - 15 days from the date of invoice, ALC - quarterly, 15 days from the date of invoice"

    payment_data = fields.Char('Payment', help='Payment',translate=True, default=_payment_data_default)
    delivery_time_data = fields.Char('Delivery Time', help='Delivery Time',translate=True, default=_delivery_time_default)
    place_of_delivery_data = fields.Char('Place of delivery', help='Place of delivery',translate=True, default=_place_of_delivery_default)
    global_discount_percent = fields.Float('Global discount', digits=dp.get_precision('Discount Percent'), digits_compute=dp.get_precision('Discount Percent'), readonly=False)
    
    def on_change_additional_discount_amount(self,cr,user,ids, additional_discount_amount, list_amount,discount_total, global_discount_percent,  context=None  ):
        if (list_amount-discount_total):
            if global_discount_percent:
                raise Warning(_('To add global discount amount, first set global discount percent to 0.00%')) 
        
            global_discount_percent = 100.00*additional_discount_amount/(list_amount-discount_total)
        else:
            global_discount_percent = 0.00
        
        return {'value':{'global_discount_percent':global_discount_percent}}
                
                

