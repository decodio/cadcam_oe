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

class PrintInvoiceWizard(models.TransientModel):
    _name = 'print.invoice.wizard'

    show_line_discount = fields.Boolean('Show line discount', default = False, help='Diplays discont on invoice lines')
    show_total_discount = fields.Boolean('Show total discount', default = False, help='Diplays total discont ')
    currency_type = fields.Selection([('document','Document currency'),('dual','Dual currency')], 'Currency', default = 'document')
    
    def print_report(self, cr, uid, ids, context=None):
        data = {
                 'ids': ids,
                 'model': 'account.invoice',
                 'form': self.read(cr, uid, ids)[0]
                 }
        dual_currency = data['form']['currency_type'] == 'dual'
        discount = data['form']['show_line_discount']
        
        if dual_currency and discount:
            report_name = 'dual_currency_invoice_report'
        elif dual_currency and not discount:
            report_name = 'dual_currency_invoice_report_no_disc'
        elif not dual_currency and discount:
            report_name = 'document_currency_invoice_report'
        elif not dual_currency and not discount:
            report_name = 'document_currency_invoice_report_no_disc'
        else:
            raise osv.except_osv(_('Print Error!'), _('Unsupported report option(s)'))


#        logging.warning('%s' %(x))
        return self.pool['report'].get_action(cr, uid, [], report_name, data=data, context=context)

