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

class account_invoice(models.Model):
    _inherit = 'account.invoice'
   
#     @api.model
#     def create(self, values):
# 
#         document_date = values.get('document_date', False)
#         if document_date:
#             values.update({'date_invoice':document_date, 'date_delivery':document_date})
#         
#         new_id = super(account_invoice, self).create(vals)
#         return new_id
#     


    def on_change_date_invoice(self,cr,user,ids, date_invoice, context=None ):
        
        return {'value':{'invoicing_datetime':date_invoice, 'date_delivery':date_invoice}}
        

    def on_change_document_date(self,cr,user,ids, document_date, context=None ):
        
        return {'value':{'date_invoice':document_date, 'date_delivery':document_date}}
        
