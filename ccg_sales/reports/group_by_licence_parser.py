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

from datetime import date, time, timedelta, datetime
from openerp.report import report_sxw
from openerp.exceptions import Warning, ValidationError
from openerp import _

class Parser(report_sxw.rml_parse):
    
    def __init__(self, cr, uid, name, context=None):
        super(Parser, self).__init__(cr, uid, name, context)
        active_model = context.get('active_model', False)
        active_id = context.get('active_id', False)
        document_obj = self.pool.get(active_model).browse(cr, uid, active_id, context=context)
        document_obj.group = {}
        partner_lang = document_obj.partner_id.lang
        context.update({'lang':partner_lang or 'en_US'})
        self.groups = [('PLC', _('PLC software')), 
              ('QLC', _('QLC software')), 
              ('YLC', _('YLC software')), 
              ('ALC', _('ALC software')), 
              ('OTHER', _('SERVICES')),
              ]
        self.document = self._group_lines(document_obj, self.groups)
        self.context = context
        self.localcontext.update({
            'time': time,
            'get_lines'     : self._get_lines,
            'get_data'      : self._get_data,
            'get_groups'    : self._get_groups,
            'get_total'     : self._get_total,
            'get_discount'  : self._get_discount,
            'get_untaxed'   : self._get_untaxed,
            'get_item_no'   : self._get_item_no,
                    })

    def _get_groups(self):
        groups2 = []
        for g in self.groups:
            if g[0] in self.document.group.keys():
                groups2.append(g) 
        return groups2

    def _get_lines(self, group):
        self.item_no = 0
        return self.document.group[group[0]]['LINES']

    def _get_total(self, group):
        return self.document.group[group[0]]['TOTAL']

    def _get_discount(self, group):
        return self.document.group[group[0]]['DISCOUNT']

    def _get_untaxed(self, group):
        return self.document.group[group[0]]['UNTAXED']

    def _get_item_no(self):
        self.item_no = self.item_no + 1
        return self.item_no

    def _group_lines(self, document_obj, groups):
        for order_line in document_obj.order_line:
            for g in groups:
                group_name = g[0]
                empty_group = {'LINES':[], 'TOTAL':0.0, 'DISCOUNT':0.0, 'UNTAXED':0.0}
                if group_name in order_line.product_id.categ_id.name: #licence_category_name:
                    group = document_obj.group.get(group_name, empty_group)
                    new_group = self._update_group_totals(order_line, group)
                    document_obj.group.update({group_name:new_group}) 
                    break
            else:
                empty_group = {'LINES':[], 'TOTAL':0.0, 'DISCOUNT':0.0, 'UNTAXED':0.0}
                group = document_obj.group.get('OTHER', empty_group)
                new_group = self._update_group_totals(order_line,group)
                document_obj.group.update({'OTHER':new_group})
        return document_obj
    
    def _update_group_totals(self, line, group):
        lines = group['LINES'] + [line]
        total = group['TOTAL'] + (line.price_unit * line.quantity)
        untaxed = group['UNTAXED'] + line.amount
        discount = (total - untaxed)
        group.update({'LINES':lines,'TOTAL':total,'UNTAXED':untaxed,'DISCOUNT':discount})
        return group

    def _get_data(self, param_name, default_value=None):
        data = self.context.get(param_name, False)
        return data
    
