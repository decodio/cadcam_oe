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
import logging
from openerp.tools.translate import _

# _logger = logging.getLogger(__name__)

class hr_employee_ccg(osv.Model):
    _name = "hr.employee"
    _inherit = "hr.employee"
    _columns = {
                'contract_duration': fields.selection([('limited','Limited'),('unlimited','Unlimited')], 'Contract duration', default = 'unlimited'),
                'start_date' : fields.date('Start date', required=True),
                'end_date' : fields.date('End date'),
                }

    _offset = 30 #days
    
    def get_contracts_to_expire(self, cr, uid, days, context={}):
        check_date = date.today() + timedelta(days=days)
        args = [('end_date','=', check_date)]
        ids=self.search(cr, uid, args, context=context)
        return ids

    def mail_recipients(self, cr, uid, employee_ids, context={}):
        """
            Mail recipients are users with HR manager role in company of employee
        """
        recipients = {}
        # iterate over employee_ids and get employee company_id
        # get HR manager(s) of company
        # add employee_id with user_id list
        #{ user_id: [employee_id, employee_id,...]}
        # update recipients dictionary
        
        pass
    
    def check_contract(self, cr, uid, context={}):
        pass
    