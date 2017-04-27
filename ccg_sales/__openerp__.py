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
    "name" : "CCG sales module",
    "version" : "1.0",
    "author" : "CADCAM Design Centar d.o.o.",
    "category" : "CCG internals",
    'description' : "Customization of sales module, specific to CADCAM group",
     "depends" : [
                 "base_vat",
                 "base_base",
                 "sp_cadcam",
                 "crm",
                ],
    'data' : [
              "wizards/print_sale_order_wizard.xml",
              "wizards/predefined_text_wizard.xml",
              "views/crm_lead_form_view_oppor_ccg.xml",
              "views/sale_view_ccg.xml",
              "views/view_partner_form_ccg.xml",
              "views/predefined_text_view.xml",
              #"views/res_users_view_ccg.xml",
              "views/crm_lead_search_ccg.xml",
              "views/recurring_invoice_line_tree.xml",
              "views/res_partner_industry_view.xml",
              "views/crm_close_reason_ccg.xml",
              "reports/sale_order_wizard_reports.xml",
              "reports/sale_order_group_reports.xml",
#              "reports/partner_reports.xml",
              "data/sale.order.predefined.text.csv",
              "data/res.partner.industry.csv",
              #"security/invoices_acces_rules.xml",
              ],
    'demo' : [],
    'installable': True,
}
