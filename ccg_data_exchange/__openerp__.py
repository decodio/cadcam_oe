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


{
    "name" : "CCG data exchange",
    "version" : "1.0",
    "author" : "CADCAM Design Centar d.o.o.",
    "category" : "CCG internals",
    'description' : "Various export and import functionality, for example CRM and CMS collaboration, CRM to DS portal export, etc.",
     "depends" : [
                  'base',
                  'ccg_base',
                  'sp_cadcam',
                  'ccg_accounting',
                  'ccg_sales',
                ],
    'data' : [
              'security/ir.model.access.csv',
              'wizards/ccg_crm_lead_export_wizard.xml',
              'views/ccg_crm_lead_export_view.xml',
              'views/ccg_offer_name_view.xml',
              'data/ccg.offer.name.csv',
              'data/ir.model.access.csv',
              'wizards/ccg_logika_export_wizard.xml'
              ],
    'demo' : [],
    'installable': True,
}
