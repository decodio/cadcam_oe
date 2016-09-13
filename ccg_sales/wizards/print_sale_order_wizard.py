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

    show_line_discount = fields.Boolean('Show line discount', default = False, help='Diplay discount for each product in quotation')
    show_total_discount = fields.Boolean('Show total discount', default = False, help='Diplay total discont on quotation')
    show_vat = fields.Boolean('Show VAT', default = False, help='Diplay total VAT on quotation')
    currency_type = fields.Selection([('document','Document currency'),('dual','Dual currency')], 'Currency', default = 'document',
                                     help='Display all prices in currency as specified on quotation \n or displays products price in document currency but totals in document currency and customer currency')
    
    def print_report(self, cr, uid, ids, context=None):
        data = {
                 'ids': ids,
                 'model': 'sale.order',
                 'form': self.read(cr, uid, ids)[0]
                 }

        dual_currency = data['form']['currency_type'] == 'dual'
        show_line_discount = data['form']['show_line_discount']
        show_total_discount = data['form']['show_total_discount']
        show_vat = data['form']['show_vat']
        
        
        if dual_currency and show_line_discount:
            report_name = 'sale_order_wizard_dual_currency_report'
        elif dual_currency and not show_line_discount:
            report_name = 'sale_order_wizard_dual_currency_report_no_disc'
        elif not dual_currency and show_line_discount:
            report_name = 'sale_order_wizard_document_currency_report'
        elif not dual_currency and not show_line_discount:
            report_name = 'sale_order_wizard_document_currency_report_no_disc'
        else:
            raise osv.except_osv(_('Print Error!'), _('Unsupported report option(s)'))

        context.update({'show_vat':show_vat, 'show_total_discount':show_total_discount})
        return self.pool['report'].get_action(cr, uid, [], report_name, data=data, context=context)

    def on_change_line_discount(self, cr, user, ids, show_line_discount, context=None ):
        return {'value':{'show_total_discount':show_line_discount}}

