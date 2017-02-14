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

class SaleOrder(models.Model):
    _name = 'sale.order'
    _inherit = 'sale.order'
    
    payment_data = fields.Char('Payment', help='Payment',translate=False)
    delivery_time_data = fields.Char('Delivery Time', help='Delivery Time',translate=False)
    place_of_delivery_data = fields.Char('Place of delivery', help='Place of delivery',translate=False)
    global_discount_percent = fields.Float('Global discount', digits=dp.get_precision('Discount Percent'), digits_compute=dp.get_precision('Discount Percent'), readonly=False)
    offer_validity_data = fields.Char('Validity of offer', help='Validity of offer')

    def on_change_additional_discount_amount(self,cr,user,ids, additional_discount_amount, list_amount,discount_total, global_discount_percent,  context=None  ):
        if (list_amount-discount_total):
            if global_discount_percent:
                raise Warning(_('To add global discount amount, first set global discount percent to 0.00%')) 
        
            global_discount_percent = 100.00*additional_discount_amount/(list_amount-discount_total)
        else:
            global_discount_percent = 0.00
        
        return {'value':{'global_discount_percent':global_discount_percent}}
                
                

