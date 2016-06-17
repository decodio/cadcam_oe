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

class account_invoice(models.Model):
    _inherit = 'account.invoice'
   
    def on_change_date_invoice(self,cr,user,ids, date_invoice, invoicing_datetime, date_delivery,context=None ):
        """
            when changed, write date_invoice into 
            date_delivery field and invoicing_datetime 
            only if those fields are empty
            invoicing_datetime got the currrent time!
        """
        ret = {}
        if date_invoice:
            if not date_delivery:
                ret.update({'date_delivery':date_invoice})
            if not invoicing_datetime:
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
            only if those fields are empty
        """
        ret = {}
        if document_date:
            if not date_delivery:
                ret.update({'date_delivery':document_date})
            if not date_invoice:
                ret.update({'date_invoice':document_date})
            
        return {'value':ret}
                
