# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2017 CADCAM Design Centar d.o.o. (<http://www.cadcam-group.eu/>).
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


{
    'name' : 'CCG travel orders module',
    'version' : '1.0',
    'author' : 'CADCAM Design Centar d.o.o.',
    'category' : 'CCG internals',
    'description' : 'Customization of travel orders module, specific to CADCAM group',
    'depends' : [
                 'base',
                 'ccg_base',
                 'sp_cadcam',
                ],
    'data' : [
              'reports/travel_order_reports.xml',
              'views/ccg_travel_order_fleet.xml',
              'views/ccg_travel_order_view.xml',
              'views/data_mapping_view.xml',
#              'data/travel.order.fleet.csv',
              'security/ir.model.access.csv',
              'wizards/ccg_travel_order_total_wizard.xml',
              'templates/travel_order_approved.xml',
              'templates/travel_order_done.xml',
              'templates/travel_order_for_approval.xml',
              'templates/travel_order_for_liquidation.xml',
              
              ],
    'demo' : [],
    'installable': True,
}
