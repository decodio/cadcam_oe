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

{
"name" : "CCG ENOVIA - odoo integration",
"version" : "1.0",
"author" : "CADCAM Design Centar d.o.o.",
"category" : "CCG internals",
"depends" : [
             "base",
             ],
"init_xml" : [],
"demo_xml" : [],
"update_xml" : [
                "enovia_test.xml",
                "security/enovia_integration_security.xml"
               ],
"installable": True,
"active": True
}