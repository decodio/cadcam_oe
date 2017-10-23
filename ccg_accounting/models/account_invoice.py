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


class account_invoice(models.Model):
    _name = 'account.invoice'
    _inherit = 'account.invoice'
    
    advance_amount_total = fields.Float('Advance Total', compute='_compute_amount_total', store=False)
    advance_amount_untaxed = fields.Float('Advance Untaxed', compute='_compute_amount_untaxed', store=False)
    advance_amount_tax = fields.Float('Advance Tax', compute='_compute_amount_tax', store=False)
    advance_invoices = fields.Char('List of advance invoices', compute='_list_of_advance_invoices', store=False)

    @api.one
    def _compute_amount_total(self):
        amount = 0.0
        if self.advance_invoice_ids:
            for advance_invoice in self.advance_invoice_ids:
                amount += advance_invoice.amount_total
        self.advance_amount_total = amount

    @api.one
    def _compute_amount_untaxed(self):
        amount = 0.0
        if self.advance_invoice_ids:
            for advance_invoice in self.advance_invoice_ids:
                amount += advance_invoice.amount_untaxed
        self.amount_untaxed
        self.advance_amount_untaxed = amount

    @api.one
    def _compute_amount_tax(self):
        amount = 0.0
        if self.advance_invoice_ids:
            for advance_invoice in self.advance_invoice_ids:
                amount += advance_invoice.amount_tax
        self.advance_amount_tax = amount
    
    @api.one
    def _list_of_advance_invoices(self):
         l =[]
         if self.advance_invoice_ids:
             for advance_invoice in self.advance_invoice_ids:
                 l.append(advance_invoice.internal_number)
         self.advance_invoices = ', '.join(l)
    
    def on_change_date_invoice(self,cr,user,ids, date_invoice, invoicing_datetime, date_delivery,context=None ):
        """
            when changed, write date_invoice into 
            date_delivery field and invoicing_datetime 
        """
        ret = {}
        if date_invoice:
            ret.update({'date_delivery':date_invoice})
            now = datetime.now()
            date = datetime.strptime(date_invoice, '%Y-%m-%d')
            invoicing_timestamp = datetime(date.year, 
                                           date.month, 
                                           date.day, 
                                           now.hour, 
                                           now.minute, 
                                           now.second )
            ret.update({'invoicing_datetime':invoicing_timestamp})
            
        return {'value':ret}
        

    def on_change_document_date(self,cr,user,ids, document_date, date_invoice, date_delivery, context=None ):
        """
            when changed, write document_date into 
            date_delivery field and date_invoice 
        """
        ret = {}
        if document_date:
            ret.update({'date_delivery':document_date})
            ret.update({'date_invoice':document_date})
            
        return {'value':ret}
                
