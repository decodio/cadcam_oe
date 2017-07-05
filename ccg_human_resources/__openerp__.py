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
    "name" : "CCG human resources module",
    "version" : "1.0",
    "author" : "CADCAM Design Centar d.o.o.",
    "category" : "CCG internals",
    'description' : "Customization of human resources module, specific to CADCAM group",
     "depends" : [
                 "base",
                 "ccg_base",
                 "sp_cadcam",
                 "sp_hr_holidays",
                ],
    'data' : [
                "reports/human_resources_reports.xml",
                "views/hr_holidays_status_form.xml",
                "views/hr_employee_form.xml",
                "views/hr_attendance_view.xml",
                "views/edit_holiday_new_ccg.xml",
                "cron/cron_job.xml",
                "template/email_template.xml",
             ],
    'demo' : [],
    'installable': True,
}