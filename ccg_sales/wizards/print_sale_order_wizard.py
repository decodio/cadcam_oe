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
    currency_type = fields.Selection([('document','Document currency'),('company','Company currency'),('dual','Dual currency')], 'Currency', default = 'document',
                                     help='Display all prices in currency as specified on quotation \ in company currency \n or displays totals in document currency and company currency')
    group_by_licence = fields.Boolean('Group products', default = False, help='Group products by categories')
    force_language = fields.Many2one('res.lang', help='Use specified language instead of partner''s language', string='Force language')
    
    def print_report(self, cr, uid, ids, context=None):
        data = {
                 'ids': ids,
                 'model': 'sale.order',
                 }
        form = self.read(cr, uid, ids)[0]
        dual_currency = form['currency_type'] == 'dual'
        company_currency = form['currency_type'] == 'company'
        document_currency = form['currency_type'] == 'document'
        show_line_discount = form['show_line_discount']
        show_total_discount = form['show_total_discount']
        show_vat = form['show_vat']
        group_by_licence  = form['group_by_licence']
        force_language  = form['force_language']
        if force_language:
            lang_obj = self.pool.get('res.lang').browse(cr, uid, force_language[0], context=context)
            fl = lang_obj.code
        else:
            fl = ''
        
        if group_by_licence:
            if dual_currency:
                report_name = 'sale_order_group_dual_currency_report'
            elif company_currency:
                raise Warning(_('Print Error!'), _('Unsupported report option(s)'))
                report_name = 'sale_order_group_document_currency_report'
            elif document_currency:
                report_name = 'sale_order_group_document_currency_report'
            else:
                raise Warning(_('Print Error!'), _('Unsupported report option(s)'))
        else:
            if dual_currency: 
                if show_line_discount:
                    report_name = 'sale_order_wizard_dual_currency_report'
                else:
                    report_name = 'sale_order_wizard_dual_currency_report_no_disc'
            elif company_currency:
                if show_line_discount:
                    report_name = 'sale_order_wizard_company_currency_report'
                else:
                    report_name = 'sale_order_wizard_company_currency_report_no_disc'
            elif document_currency:
                if show_line_discount:
                    report_name = 'sale_order_wizard_document_currency_report'
                else:
                    report_name = 'sale_order_wizard_document_currency_report_no_disc'
            else:
                raise Warning(_('Print Error!'), _('Unsupported report option(s)'))

        context.update({'show_vat':show_vat, 
                        'show_total_discount':show_total_discount,
                        'company_currency' : company_currency,
                        'document_currency':document_currency,
                        'force_language' : fl,
                        })
        return self.pool['report'].get_action(cr, uid, [], report_name, data=data, context=context)

    def email_report(self, cr, uid, ids, context=None):
        print 'email_report_ids', ids
        data = {
                 'ids': ids,
                 'model': 'sale.order',
                 }
        form = self.read(cr, uid, ids)[0]
        dual_currency = form['currency_type'] == 'dual'
        company_currency = form['currency_type'] == 'company'
        document_currency = form['currency_type'] == 'document'
        show_line_discount = form['show_line_discount']
        show_total_discount = form['show_total_discount']
        show_vat = form['show_vat']
        group_by_licence  = form['group_by_licence']
        force_language  = form['force_language']
        if force_language:
            lang_obj = self.pool.get('res.lang').browse(cr, uid, force_language[0], context=context)
            fl = lang_obj.code
        else:
            fl = ''
        
        if group_by_licence:
            if dual_currency:
                email_template_name = 'sale_order_group_dual_currency_email'
            elif company_currency:
                raise Warning(_('Print Error!'), _('Unsupported report option(s)'))
                email_template_name = 'sale_order_group_document_currency_email'
            elif document_currency:
                email_template_name = 'sale_order_group_document_currency_email'
            else:
                raise Warning(_('Print Error!'), _('Unsupported report option(s)'))
        else:
            if dual_currency: 
                if show_line_discount:
                    email_template_name = 'sale_order_wizard_dual_currency_email'
                else:
                    email_template_name = 'sale_order_wizard_dual_currency_email_no_disc'
            elif company_currency:
                if show_line_discount:
                    email_template_name = 'sale_order_wizard_company_currency_email'
                else:
                    email_template_name = 'sale_order_wizard_company_currency_email_no_disc'
            elif document_currency:
                if show_line_discount:
                    email_template_name = 'sale_order_wizard_document_currency_email'
                else:
                    email_template_name = 'sale_order_wizard_document_currency_email_no_disc'
            else:
                raise Warning(_('Email Error!'), _('Unsupported email option(s)'))

        context.update({'show_vat':show_vat, 
                        'show_total_discount':show_total_discount,
                        'company_currency' : company_currency,
                        'document_currency':document_currency,
                        'force_language' : fl,
                        })
        email_template_obj = self.pool.get('email.template')
        template_ids = email_template_obj.search(cr, uid, [('name', '=', email_template_name)], context=context) 
        print 'template_ids:', template_ids
        if template_ids:
            template_id = template_ids[0]
            sender_id = context.get('active_id', False)
            msg_id = email_template_obj.send_mail(cr, uid, template_id, sender_id, force_send=True, context=context)
            return True
        return False
    
    def on_change_line_discount(self, cr, user, ids, show_line_discount, context=None ):
        return {'value':{'show_total_discount':show_line_discount}}
    
    def on_change_group_by_licence(self, cr, user, ids, group_by_licence, context=None ):
        if group_by_licence:
            ret ={'value':{'show_total_discount':True, 'show_line_discount':True, 'show_vat':False, 'currency_type' : 'document'}}
        else:
            ret = {} 
        return ret

