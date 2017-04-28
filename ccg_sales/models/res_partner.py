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
from openerp.addons.crm import crm



class ResPartnerCCG(models.Model):
    _name = 'res.partner'
    _inherit = 'res.partner'
    priority = fields.Selection(crm.AVAILABLE_PRIORITIES , 'Priority', default = '0')
    head_office_id = fields.Char('Head Office ID')
    site_id = fields.Char('Site ID')
    industry_ids = fields.Many2many('res.partner.industry', 'res_partner_partner_industry_rel','res_partner_id', 'industry_id',string="Industry" )

    @api.multi
    @api.onchange('site_id')
    def _on_change_partner(self):
        if not self.head_office_id and self.site_id:
            self.head_office_id = self.site_id
