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

    partner_ids = fields.Many2many('res.partner', 'hr_travel_order_partner_rel','travel_order_id', 'partner_id')
    depart_vehicle_ids = fields.Many2many('travel.order.fleet', 'hr_travel_order_fleet_rel','travel_order_id', 'vehicle_id')
    arrive_vehicle_ids = fields.Many2many('travel.order.fleet', 'hr_travel_order_fleet_rel','travel_order_id', 'vehicle_id')
    @api.multi
    @api.onchange('partner_ids')
    def _on_change_partner(self):
        countries = []
        cities = [self.dest_city] if self.dest_city else []
        for partner in self.partner_ids:
            if partner.country_id:
                 countries.append(partner.country_id.id)
            if (not self.dest_city and partner.city ) or (partner.city and self.dest_city and not (partner.city in self.dest_city)):
                 cities.append(partner.city)
        if countries:
            self.country_ids = countries
        if cities:
            self.dest_city = ", ".join(cities)

    @api.multi
    @api.onchange('depart_vehicle_ids')
    def _on_change_depart_vehicle_ids(self):
        if self.depart_vehicle_ids and not self.arrive_vehicle_ids:
            self.arrive_vehicle_ids = [vehicle_id.id for vehicle_id in self.depart_vehicle_ids if vehicle_id]

    @api.multi
    @api.onchange('depart_transportation')
    def _on_change_depart_transportation(self):
        if self.depart_transportation and not self.arrive_transportation:
            self.arrive_transportation = self.depart_transportation


class ccg_travel_order_itinerary_lines(models.Model):
    _inherit = "hr.travel.order.itinerary.lines"
    _name = "hr.travel.order.itinerary.lines"

    vehicle_id = fields.Many2one('travel.order.fleet', 'Vehicle')
    vehicle = fields.Char('Vehicle', compute='_compute_vehicle', store=True,help="")
    license_plate = fields.Char('License Plate',compute='_compute_license_plate', store=True,)
    odometer_end = fields.Integer('Odometer end',store=True,)
    calc_odometer = fields.Boolean("km?")
    
    def get_odometer_previous(self, cr, uid, ids, context=None):
        self.cr = cr
        dateto = context.get('dateto', 'False')
        vehicle_id    = context.get('vehicle_id',False)
        distance = context.get('distance', 0)
        if vehicle_id and dateto: 
            sql = """
            select
                l.odometer_end
            from 
                hr_travel_order_itinerary_lines l left join 
                hr_travel_order t on l.travel_order_id = t.id
            where 
                t.date_to < '{}' and l.vehicle_id = {}
            order by 
                l.odometer_end desc
            limit 1
            """.format(dateto , vehicle_id)
            print sql
            self.cr.execute( sql)
            data = self.cr.fetchall()
            if data :
                odometer_last_value = data[0][0]
            else:
                odometer_last_value = 0
            return {'value': {'odometer_start': odometer_last_value,
                                             'odometer_end':odometer_last_value + distance,
                                             'calc_odometer':0}}    
    
    @api.one
    @api.depends('vehicle_id')
    def _compute_vehicle(self):
        vehicle = []
        if self.vehicle_id.modelname:
            vehicle.append(self.vehicle_id.modelname)
        if self.vehicle_id.brandname:
            vehicle.append(self.vehicle_id.brandname)
        self.vehicle = ' '.join(vehicle)

    @api.multi
    @api.onchange('vehicle_id')
    def _on_change_vehicle_id(self):
        if self.vehicle_id.type:
            self.vehicle_type = self.vehicle_id.type
            
    @api.multi
    def action_recompute_itinerary(self):
#        print 'CCG action_recompute_itinerary'
        total_itinerary = 0.00
        for l in self.itinerary_ids:
#            print l.vehicle_type
            if l.vehicle_type == 'private':
                total_itinerary = total_itinerary + l.lcy_amount_total
            else: 
                l.lcy_amount_total = 0.0
        return self.write({'lcy_itinerary_amount_total': total_itinerary,
                         })
            

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



    @api.onchange('odometer_start')
    def onchange_odometer_start(self):
        end = self.odometer_end
        start = self.odometer_start
        distance = self.distance
        if (start and end) and (start > end):
            raise Warning(
                _('Warning!'),
                _('The odometer start value must be lower than end value.'))
        if start and not end:
            self.odometer_end = (distance and start + distance or start)
        if (end and start) and (start <= end):
            self.distance = end - start
        if self.vehicle_type == 'private':
            self.lcy_amount_total = self.distance * 2.0
        else:
            self.lcy_amount_total = 0.0
            
    @api.onchange('odometer_end')
    def onchange_odometer_end(self):
        end = self.odometer_end
        start = self.odometer_start
        if (start and end) and (start > end):
            raise Warning(
                _('Warning!'),
                _('The odometer start value must be lower than end value.'))
        if (end and start) and (start <= end):
            self.distance = end - start
        if self.vehicle_type == 'private':
            self.lcy_amount_total = self.distance * 2.0
        else:
            self.lcy_amount_total = 0.0

