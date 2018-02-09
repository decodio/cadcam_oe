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

from openerp import models, fields, api, _
import openerp.addons.decimal_precision as dp

class crm_lead(models.Model):
    _name = 'crm.lead'
    _inherit = 'crm.lead'
 
    offer_name_id = fields.Many2one('ccg.offer.name')
    revenue_type = fields.Selection([('PLC', 'PLC'),('YLC', 'YLC')], default = 'PLC', required=True)
    contact_name_id = fields.Many2one('res.partner', help="Contact Person related to this opportunity.")
    ds_expected_revenue = fields.Float('DS Revenue', digits=dp.get_precision('Account'), help="Revenue related to PLC licence.\This revenue will be send to DS portal.")
    ds_lead_id = fields.Char('DS Lead ID', size=11, help='DS lead ID, format is ADOA-XXXXXX')
#    comarketing_yn = fields.Selection([('Y', 'Yes'),('N', 'No')], help='CoMarketing, yes or no?')
    comet_campaign_code = fields.Char('COMET campaign code', size=40, help='COMET campaign code')
    campaign_name = fields.Char('Campaign name', size=40, help='Campaign name') 
    next_milestone = fields.Char('Next Milestone', size=250, help='Next Milestone') 
