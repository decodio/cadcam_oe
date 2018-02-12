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
        if active_model and active_id:
            document_obj  = self.pool.get(active_model).browse(cr, uid, active_id, context=context)
            if document_obj .partner_id.is_company and not document_obj .partner_id.vat :
                raise Warning(_("Cannot print quotation without customer's VAT number!"))
        document_obj.group = {}
        partner_lang = document_obj.partner_id.lang
        context.update({'lang':partner_lang or 'en_US'})
        self.groups = [('PLC', 'PLC software', _('PLC software')),  #3rd parameter is for translation only!!!#
              ('QLC', 'QLC software', _('QLC software')), 
              ('YLC', 'YLC software', _('YLC software')), 
              ('ALC', 'ALC software', _('ALC software')), 
              ('TBL2', 'TBL2 software', _('TBL2 software')), 
              ('TBL3', 'TBL3 software', _('TBL3 software')), 
              ('OTHER', 'SERVICES', _('SERVICES')),
              ]
        self.document = self._group_lines(document_obj, self.groups)
        self.context = context
        self.force_language = self.context.get('force_language', '')
        self.localcontext.update({
            'time': time,
            'get_lines'     : self._get_lines,
            'get_data'      : self._get_data,
            'get_groups'    : self._get_groups,
            'get_total'     : self._get_total,
            'get_discount1'  : self._get_discount1,
            'get_discount2'  : self._get_discount2,
            'get_untaxed1'   : self._get_untaxed1,
            'get_untaxed2'   : self._get_untaxed2,
            'get_item_no'   : self._get_item_no,
            'get_line_total1': self._get_line_total1,
            'get_line_total2': self._get_line_total2,
            'get_all_discounts_percent' : self._get_all_discounts_percent,
            'get_discount2_percent' : self._get_discount2_percent,
            'force_language': self.force_language,
        })

    def _get_groups(self):
        groups2 = []
        for g in self.groups:
            if g[0] in self.document.group.keys():
                h = (g[0],_(g[1]))
                groups2.append(h) 
        return groups2

    def _get_discount2_percent(self, group):
        return self.document.group[group[0]]['DISCOUNT2PERCENT']

    def _get_lines(self, group):
        self.item_no = 0 # new item numbers for each group
        return self.document.group[group[0]]['LINES']

    def _get_total(self, group):
        return self.document.group[group[0]]['TOTAL'] # sum of price_unit * quantity

    def _get_discount1(self, group):
        return self.document.group[group[0]]['DISCOUNT1'] # total discount based on discount1_percent which is visible on document

    def _get_discount2(self, group):
        return self.document.group[group[0]]['DISCOUNT2'] # total discount based on discount1_percent1 and discount1_percen2 (additional discount on group) 

    def _get_untaxed1(self, group):
        return self.document.group[group[0]]['UNTAXED1'] # total price discount1

    def _get_untaxed2(self, group):
        return self.document.group[group[0]]['UNTAXED2'] # total price with both discounts

    def _get_item_no(self):
        self.item_no = self.item_no + 1 # increase item number for each line IN GROUP!
        return self.item_no

    def _empty_group(self):
        return {'LINES':[],
                'TOTAL':0.0, 
                'DISCOUNT1':0.0, 
                'DISCOUNT2':0.0, 
                'UNTAXED1':0.0, 
                'UNTAXED2':0.0, 
                'DISCOUNT2PERCENT':0.0}
    
    def _group_lines(self, document_obj, groups):
        for order_line in document_obj.order_line:
            for g in groups:
                group_name = g[0]
                if group_name in order_line.product_id.categ_id.name: #licence_category_name:
                    group = document_obj.group.get(group_name, self._empty_group())
                    new_group = self._update_group_totals(order_line, group)
                    document_obj.group.update({group_name:new_group}) 
                    break
            else:
                group = document_obj.group.get('OTHER', self._empty_group())
                new_group = self._update_group_totals(order_line,group)
                document_obj.group.update({'OTHER':new_group})
        return document_obj
    
    def _update_group_totals(self, line, group):
        lines = group['LINES'] + [line]
        total = group['TOTAL'] + (line.price_unit * line.quantity)    # without any discount
        untaxed1 = group['UNTAXED1'] + self._get_line_total1(line)    # with discount1
        untaxed2 = group['UNTAXED2'] + self._get_line_total2(line)    # with discount2
        discount1 = (total - untaxed1)
        discount2 = (total - discount1 - untaxed2)
        disc2percent = group['DISCOUNT2PERCENT']
        if disc2percent<>0 and disc2percent<>line.discount2_percent:
            raise Warning(_("Inconsistent group discount!\nDiscount must be same over whole group!"))
        else:
            disc2percent = line.discount2_percent
        group.update({'LINES':lines,
                      'TOTAL':total,
                      'UNTAXED1':untaxed1,
                      'UNTAXED2':untaxed2,
                      'DISCOUNT1':discount1,
                      'DISCOUNT2':discount2,
                      'DISCOUNT2PERCENT':disc2percent,
                      })
        return group

    def _get_data(self, param_name, default_value=None):
        data = self.context.get(param_name, False)
        return data
    
    def _get_all_discounts_percent(self, discount1, discount2 = 0.0, discount3 = 0.0):
        """
            calculate total discount percent for several discounts available in quotation lines
        """
        disc=100.00-(100.00-discount1)*(100.00-discount2)*(100.00-discount3)/1000000*100
        return disc

    def _get_additional_discount(self):
        pass
    
    def _get_total_total(self):
        pass
    
    def _get_line_total(self, line):
        line_total = line.price_unit * line.quantity 
        return line_total

    def _get_line_total1(self, line):
        disc_percent = self._get_all_discounts_percent(line.discount1_percent)
        disc_factor = (100.0 - disc_percent) / 100
        line_total = line.price_unit * line.quantity * disc_factor
        return line_total
    
    def _get_line_total2(self, line):
        disc_percent = self._get_all_discounts_percent(line.discount1_percent, line.discount2_percent)
        disc_factor = (100.0 - disc_percent) / 100
        line_total = line.price_unit * line.quantity * disc_factor
        return line_total
        
