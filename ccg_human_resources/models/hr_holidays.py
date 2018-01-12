# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2016, 2017 CADCAM Design Centar d.o.o. (http://www.cadcam-group.eu/).
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

import math
import time
from openerp import models, fields, api, _
from openerp.exceptions import Warning
from openerp.tools import (DEFAULT_SERVER_DATE_FORMAT,DEFAULT_SERVER_DATETIME_FORMAT)
from datetime import datetime, date
from time import strptime


class HrHolidays(models.Model):
    _inherit = "hr.holidays"
    
    def check_holidays(self, cr, uid, ids, context=None):
        for record in self.browse(cr, uid, ids, context=context):
            if record.holiday_type != 'employee' or record.type != 'remove' or not record.employee_id or record.holiday_status_id.limit:
                continue
            if not context:
                context = {}
            context = context.copy()
            context.update({'current_holiday': record.id})
            leave_days = self.pool.get('hr.holidays.status').get_days(cr, uid, [record.holiday_status_id.id], record.employee_id.id, context=context)[record.holiday_status_id.id]
            if leave_days['remaining_leaves'] < 0 or leave_days['virtual_remaining_leaves'] < 0 : 
               # Raising a warning gives a more user-friendly feedback than the default constraint error
               raise Warning(_('CCG:The number of remaining leaves ({0:d} day(s)) is not sufficient for this leave type!'.format(int(leave_days['remaining_leaves']))))
        return True

    def create(self, cr, uid, vals, context=None):
        date_from_str = vals.get('date_from', None)
        date_from = None
        datetime_format = '%Y-%m-%d %H:%M:%S'
        if date_from_str:
            date_from = datetime.strptime(date_from_str, datetime_format).replace(hour=7, minute=00)
            vals.update({'date_from':date_from})
        date_to_str = vals.get('date_to', date_from)
        if date_to_str:
            date_to = datetime.strptime(date_to_str, datetime_format).replace(hour=19, minute=0)
            vals.update({'date_to':date_to})
        return super(HrHolidays, self).create(cr, uid, vals, context)