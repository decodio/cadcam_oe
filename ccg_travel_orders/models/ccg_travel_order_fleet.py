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
from openerp import models, fields, api, _, SUPERUSER_ID

class TravelOrderFleet(models.Model):
    _name = 'travel.order.fleet'
    _inherit = 'travel.order.fleet'
    
#     name = fields.Char('Vehicle', required=True)
#     registration = fields.Char('Registration', required=True)
    type = fields.Selection([('company', 'Company'), ('private', 'Private')], required=True)
    fuel = fields.Selection([('petrol', 'Petrol'), ('diesel', 'Diesel')], required=True)
    owner = fields.Many2one('hr.employee')

    name = fields.Char('Name', compute='_compute_name', store=True)
    modelname = fields.Char('Model name', required=False)

    @api.one
    @api.depends(
            'modelname',
            'brandname',
            'license_plate'
            )
    def _compute_name(self):
        name = []
        if self.brandname:
            name.append(self.brandname)
        if self.modelname:
            name.append(self.modelname)
        if self.license_plate:
            name.append('('+self.license_plate+')')
        self.name = " ".join(name)
    
