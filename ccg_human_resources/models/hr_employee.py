# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2016 CADCAM Design Centar d.o.o. (http://www.cadcam-group.eu/).
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
from openerp.osv import fields, osv
from openerp.tools.translate import _
from datetime import date, timedelta
#from samba.dcerpc.samr import Ids

#import logging
#_logger = logging.getLogger(__name__)

class hr_employee_ccg(osv.Model):
    _name = "hr.employee"
    _inherit = "hr.employee"

    def _get_receivers_list(self, cr, uid, ids, field_name, field_value, context=None):
        ret = {}
        for employee in self.browse(cr, uid, ids):
            l = ''
            reclist = []
            for manager in employee.hr_manager_ids:
                reclist.append(manager.partner_id.id)
                l = ','.join([ str(l) for l in reclist])
            ret.update({employee.id:l})
        return ret

    _columns = {
                'contract_duration': fields.selection([('limited','Limited'),('unlimited','Unlimited')], 'Contract duration', default = 'unlimited'),
                'start_date' : fields.date('Start date', required=True),
                'end_date' : fields.date('End date'),
                'hr_manager_ids' :fields.many2many('res.users', 'hr_employee_user_rel', 'employee_id', 'user_id', 'HR Managers',help='Users which receives HR notifications from employee'), 
                'receivers_list' : fields.function(_get_receivers_list, type='char', string='Receivers', readonly=True, store=True)
                }

    _offset = 30 #days

    def _get_contracts_soon_expire(self, cr, uid, days, context={}):
        check_date = date.today() + timedelta(days=days)
        args = [('end_date','=', check_date)]
        employee_ids=self.search(cr, uid, args, context=context)
        return employee_ids 

    def _send_email(self, cr, uid, ids, context=None):
        email_template_obj = self.pool.get('email.template')
        template_ids = email_template_obj.search(cr, uid, [('name', '=','email_template_contract_expiration')], context=context) 
        if template_ids:
            for sender_id in ids:
                msg_id = email_template_obj.send_mail(cr, uid, template_ids[0], sender_id, force_send=True,context=context)
            return True
        return False


    def check_contract_expiration(self, cr, uid, context={}):
        send_list = self._get_contracts_soon_expire(cr, uid, self._offset, context)
        if send_list:
            self._send_email(cr, uid, send_list, context=context)
    
     