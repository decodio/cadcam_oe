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

from openerp import models, fields, _, api
import openerp.addons.decimal_precision as dp


class RecurringInvoiceLine(models.Model):
    _name = 'recurring.invoice.line'
    _inherit = 'recurring.invoice.line'

    price_unit = fields.Float('List Price', required=False, digits=dp.get_precision('Purchase Price'), digits_compute=dp.get_precision('Purchase Price'))
    tos_date = fields.Date('TOS Date', required=False )


