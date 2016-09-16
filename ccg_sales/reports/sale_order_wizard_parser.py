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

from datetime import date, timedelta, datetime
from openerp.report import report_sxw
from openerp.exceptions import Warning, ValidationError
from openerp import _

class Parser(report_sxw.rml_parse):
    def __init__(self, cr, uid, name, context):
        super(Parser, self).__init__(cr, uid, name, context)
        active_model = context.get('active_model', False)
        active_id = context.get('active_id', False)
        if active_model and active_id:
            model = self.pool.get(active_model).browse(cr, uid, active_id, context=context)
            if not model.partner_id.vat :
                raise Warning(_("Cannot print quotation without customer's VAT number!"))
            

        self.context = context
        self.localcontext.update({ 'get_data' :  self._get_data,  })

    def _get_data(self, param_name, default_value=None):
        data = self.context.get(param_name, False)
        return data
    
    