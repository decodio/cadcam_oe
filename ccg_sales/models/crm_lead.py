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

from openerp import models, fields, api, _, SUPERUSER_ID
from datetime import datetime, date
from dateutil.relativedelta import *

 # TO DO:
 # inherit crm_lead
 # override create method
 # task_ids.company_id = company_is
 # ....
 # overwrite write method
 # task_ids.company_id = company_is
class crm_lead(models.Model):
    _name = 'crm.lead'
    _inherit = ['crm.lead']

    def prolonged_date(self):
        six_months_later = relativedelta(months=+6)
        return datetime.now() + six_months_later

    def onchange_stage_id(self, cr, uid, ids, stage_id, context=None):
        lead = self.pool.get('crm.lead').browse(cr, uid, ids[0], context=context)
        res = {}
        if lead.stage_id.name=='Lost':
             vals = {'stage_id':lead.stage_id.id} #cannot exit from lost state
        else:
            res = super(crm_lead, self).onchange_stage_id(cr, uid, ids, stage_id, context=context)
            stage = self.pool.get('crm.case.stage').browse(cr, uid, stage_id, context=context)
            vals = res.get('value', {})
            if stage.name == 'Sleeping':
                vals.update({'date_deadline': self.prolonged_date()})
        
        res.update({'value':vals})
        return res


