# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
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

from openerp.osv import fields, osv


class enovia_test(osv.osv):

    """
    Test class to store ENOVIA data
    """

    _name = 'enovia.test'
    _columns={
              'level'       : fields.char('Level',size=64,  help='Level in BOM tree'),
              'name'        : fields.char('Name',size=64,  help='Name'),
              'data'        : fields.char('Data',size=64,  help='Any text data associated with BOM item'),
              'value'       : fields.float('Value',  help='Any numerical data associated with BOM item'),
              'parent'      : fields.many2one('enovia.test', relation='name', string='Parent', help="Parent of BOM item"),
              }
    
enovia_test()    
