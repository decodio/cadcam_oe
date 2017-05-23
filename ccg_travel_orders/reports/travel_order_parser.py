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
import math

class Parser(report_sxw.rml_parse):
    def __init__(self, cr, uid, name, context):
        super(Parser, self).__init__(cr, uid, name, context)
        self.context = context
        self.localcontext.update({ 'get_estimated_days' :  self._get_estimated_days,  })

    def _get_dates(self, cr, uid, context=None):
        active_model = context.get('active_model', False)
        active_id = context.get('active_id', False)
        if active_model and active_id:
            travel_order_obj = self.pool.get(active_model).browse(cr, uid, active_id, context=context)
        return (travel_order_obj.date_from, travel_order_obj.date_to)

    def _get_estimated_days(self, date_from, date_to):
        if date_from and date_to:
            df = datetime.strptime(date_from, "%Y-%m-%d %H:%M:%S")
            dt = datetime.strptime(date_to, "%Y-%m-%d %H:%M:%S")
            print dt
            print df
            print (dt - df).days,  (dt - df).seconds / 3600 / 24 + 1
            return int(math.ceil((dt - df).seconds / 3600.0 / 24.0 + 1))
        else:
            return 0
    
    