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

from openerp import models, fields, api, _


class ccg_travel_order(models.Model):
    _inherit = 'hr.travel.order'
    _name = 'hr.travel.order'

    depart_vehicle_ids = fields.Many2many('travel.order.fleet', 'hr_travel_order_fleet_rel','travel_order_id', 'vehicle_id')
    arrive_vehicle_ids = fields.Many2many('travel.order.fleet', 'hr_travel_order_fleet_rel','travel_order_id', 'vehicle_id')
    
class ccg_travel_order_itinerary_lines(models.Model):
    _inherit = "hr.travel.order.itinerary.lines"
    _name = "hr.travel.order.itinerary.lines"

    vehicle_id = fields.Many2one('travel.order.fleet', 'Vehicle')
    vehicle = fields.Char('Vehicle', compute='_compute_vehicle', store=True,help="")
    license_plate = fields.Char('License Plate',compute='_compute_license_plate', store=True,)
    odometer_end = fields.Integer('Odometer end',store=True,)

    @api.one
    @api.depends('vehicle_id')
    def _compute_vehicle(self):
        print 
        vehicle = []
        if self.vehicle_id.modelname:
            vehicle.append(self.vehicle_id.modelname)
        if self.vehicle_id.brandname:
            vehicle.append(self.vehicle_id.brandname)
        self.vehicle = ' '.join(vehicle)

    @api.one
    @api.depends('vehicle_id')
    def _compute_license_plate(self):
            
        if self.vehicle_id.license_plate:
            self.license_plate = self.vehicle_id.license_plate

    @api.one
    @api.onchange('odometer_start', 'distance')
    def _compute_odometer_end(self):
            
        if self.odometer_start + self.distance != self.odometer_end:
            self.odometer_end = self.odometer_start + self.distance

