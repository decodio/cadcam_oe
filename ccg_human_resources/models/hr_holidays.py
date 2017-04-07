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

import datetime
import math
import time
from openerp import models, fields, api, _
from openerp.exceptions import Warning
from openerp.tools import (DEFAULT_SERVER_DATE_FORMAT,DEFAULT_SERVER_DATETIME_FORMAT)


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
            print 'CCG:leave_days', leave_days
            print 'CCG:record.number_of_days_temp',record.number_of_days_temp
            if leave_days['remaining_leaves'] < 0 or leave_days['virtual_remaining_leaves'] < 0 : 
               # Raising a warning gives a more user-friendly feedback than the default constraint error
               raise Warning(_('CCG:The number of remaining leaves ({0:d} day(s)) is not sufficient for this leave type!'.format(int(leave_days['remaining_leaves']))))
        return True
