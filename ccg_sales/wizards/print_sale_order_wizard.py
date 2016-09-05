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

from openerp import models, fields, api, _, SUPERUSER_ID
from openerp.exceptions import except_orm, ValidationError, Warning, RedirectWarning

class PrintSaleOrderWizard(models.TransientModel):
    _name = 'print.sale.order.wizard'

    show_line_discount = fields.Boolean('Show line discount', default = False, help='Diplays discont on salae order lines')
    show_total_discount = fields.Boolean('Show total discount', default = False, help='Diplays total discont sale order')
    show_vat = fields.Boolean('Show VAT', default = False, help='Diplays total VAT on sale order')
    currency_type = fields.Selection([('document','Document currency'),('dual','Dual currency')], 'Currency', default = 'document')
    
    def print_report(self, cr, uid, ids, context=None):
        data = {
                 'ids': ids,
                 'model': 'sale.order',
                 'form': self.read(cr, uid, ids)[0]
                 }
        if data['form']['currency_type'] == 'dual':
            report_name = 'sale_order_dual_currency_report'
        else:
            report_name = 'sale_order_document_currency_report'

#        logging.warning('%s' %(x))
        return self.pool['report'].get_action(cr, uid, [], report_name, data=data, context=context)

