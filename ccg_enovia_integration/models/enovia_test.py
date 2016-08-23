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
              'tnr'         : fields.char('TNR',size=64,  help='TNR is unique identifier of part'),
              'title'       : fields.char('Title',size=64,  help='Title of BOM item'),
              'description' : fields.char('Description',size=64,  help='Description of BOM item'),
              'quantity'    : fields.float('Quantity',  help='Quantity'),
              'parent'      : fields.many2one('enovia.test', string='Parent', help="Parent of BOM item"),
              'product_id'  : fields.many2one('product.product', string='Product', help="Product associated with BOM item"),
              }
    
    
    def name_get(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        if isinstance(ids, (int, long)):
            ids = [ids]
        res = []
        if context.get('special_display_name', False):
            for record in self.browse(cr, uid, ids, context=context):
                name = record.tnr
                percentage = record.insurance_percentage
                res.append((record.id, name + " - " + percentage + "%"))
        else:
            for record in self.browse(cr, uid, ids, context=context):
                res.append((record.id, record.tnr))
        return res

    def link_part_to_product(self, cr, uid, ids, context=None):
        print 'Not implemented yet!'
        print 'product_id = {}'.format(context.get('product_id', 'unknown'))
        pass
        
        
enovia_test()    
