# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2016 CADCAM Design Centar d.o.o. (<http://www.cadcam-group.eu/>).
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

from openerp import models, fields, api, _
from datetime import datetime
import openerp.addons.decimal_precision as dp


class account_invoice_line(models.Model):
    _name = 'account.invoice.line'
    _inherit = 'account.invoice.line'
    
    discount = fields.Float(string='Discount (%)', digits=dp.get_precision('Discount Percent'), digits_compute=dp.get_precision('Discount Percent'), default=0.0)
    discount1_percent = fields.Float('Discount', digits=dp.get_precision('Discount Percent'), digits_compute=dp.get_precision('Discount Percent'))
    discount2_percent = fields.Float('Second discount', digits=dp.get_precision('Discount Percent'), digits_compute=dp.get_precision('Discount Percent'))
    
