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
# import openerp.addons.decimal_precision as dp
from openerp import models, fields, api, _
from openerp.exceptions import Warning 
from openerp.osv import orm, osv, fields
from datetime import datetime, date
from time import strptime
from Crypto import SelfTest
import base64
import csv
import locale 

from codes_translation import country_translation, currency_translation, product_to_expense 

class ccg_travel_order_total_export(osv.osv_memory):  # orm.TransientModel
    _name = 'ccg.travel.order.total.export'

    _columns = {
        'data'      : fields.binary('File', readonly=True),
        'name'      : fields.char('Filename', size=255, readonly=True),
        'state'     : fields.selection((('create', 'create'), ('get', 'get'),), default='create'),
        'delimiter' : fields.selection(((',', ', (comma)'), (';', '; (semicolon)'), ('\t', '(tab)'),), default=';'),
        'quotation' : fields.selection((('"', '"'), ("'", "'"), ('none', '(none)'),), default='none'),
        'encoding'  : fields.selection((('utf-8', 'utf-8'), ('utf-8-sig', 'utf-8 with BOM'), ("windows-1250", "windows-1250")), default='utf-8'),
        'decimal'  :  fields.selection((('.', '. (dot)'), (',', ', (comma)')), default=','),
    }
    
    def _quotation(self):
        return self.form['quotation']

    def _delimiter(self):
        return self.form['delimiter']
     
    def _encoding(self):
        return self.form['encoding']

    def _decimal(self):
        return self.form['decimal']
    
    def _quoted(self, text):
        q = self._quotation()
        if q == 'none':
            return str(text)
        else:
            return '{1}{0}{1}'.format(text, q)

    def _reformat_date(self, date):
        dd = date[8:10]
        mm = date[5:7]
        yyyy = date[0:4]
        return '{}.{}.{}'.format(dd, mm, yyyy)

    def _reformat_datetime(self, datetime):
        dd = datetime[8:10]
        mm = datetime[5:7]
        yyyy = datetime[0:4]
        HH = datetime[11:13]
        MM = datetime[14:16]
        SS = datetime[17:18]
        return '{}.{}.{} {}:{}:{}'.format(dd, mm, yyyy,HH,MM,SS)

    def _document(self, cr, uid, travel_order, context=None):
        line=[]
# header - Vrijednost 1 obavezna u svakom retku
        line.append(self._quoted('1'))
# datum_naloga
        document_date = self._reformat_date(travel_order.document_date)
        line.append(document_date)
# datum_isplate
        date_liquidation = self._reformat_date(travel_order.date_liquidation)
        line.append(date_liquidation)
# sifra_zaposlenika_putnika
        employee_id = travel_order.employee_id.id #.logika_employee_id
        line.append(self._quoted(employee_id))
# sifra_zaposlenika_odobritelja
        responsible_person_id = travel_order.employee_id.id
        line.append(self._quoted(responsible_person_id))
# datum_i_vrijeme_odlaska
        date_from = self._reformat_date(travel_order.date_from)
        line.append(date_from)
# datum_i_vrijeme_povratka
        date_from = self._reformat_date(travel_order.date_from)
        line.append(date_from)
# pbr_mjesto_polaska
        city_departure = travel_order.company_id.city
        line.append(city_departure)
# pbr_mjesto_odrediste
        city_destination = travel_order.dest_city.split(',')
        line.append(city_destination[0])
# opis_putovanja
        purpose = travel_order.purpose[:200]
        line.append(purpose)
# tip_prijevozno_sredstvo
        depart_transportation_type = travel_order.depart_transportation[0].name
        line.append(depart_transportation_type)
# marka_i_regbr_vozila
        if travel_order.depart_vehicle_ids:
            vehicle_registration = travel_order.depart_vehicle_ids[0].name
        else:
            vehicle_registration = ''
        line.append(vehicle_registration)
# pocetno_stanje_brojila
        if travel_order.itinerary_ids:
            odometer_start = travel_order.itinerary_ids[0].odometer_start
        else:
            odometer_start = ''
        line.append(self._quoted(odometer_start))
# odobreni_predujam
        advance_payment = travel_order.advance_payment
        line.append(self._quoted(advance_payment))
# valuta_za_predujam
        if travel_order.currency_id:
            currency_name = travel_order.currency_id.name
            advance_currency_code = currency_translation.get(currency_name)[0]
        else:
            advance_currency_code = ''
        line.append(advance_currency_code)
# putno_izvjesce
        report = travel_order.other_data
        line.append(report)
        
        csv_row = self._delimiter().join(line)
        return csv_row
    
    def _allowances(self, cr, uid, allowances, context=None):
        lines = [ ]
        for allowance in allowances:
            line = [ ]
# Header - Vrijednost 2 obavezna u svakom retku
            line.append( self._quoted('2'))
# sifra_drzave
            country = country_translation.get(allowance.country_id.code)[1]
            line.append( self._quoted(country))
# datum_i_vrijeme_ulaska
            date_from = allowance.date_from
            line.append(self._reformat_datetime(date_from))
# datum_i_vrijeme_izlaska
            date_to = allowance.date_to
            line.append(self._reformat_datetime(date_to))
            data = self._delimiter().join(line)
            lines.append(data)
        csv_rows = '\n'.join(lines)
        return (csv_rows)
    
    def _expenses(self, cr, uid, expenses, context=None):
        lines = []
        for expense in expenses:
            line = []
# header - Vrijednost 3 obavezna u svakom retku
            line.append(self._quoted('3'))
# vrsta_putnog_troska
            expense_type = product_to_expense.get(expense.product_id.id,99)[0]
            line.append(self._quoted(expense_type))
# oznaka_placeno
            line.append(self._quoted('0')) # nije plaćeno
# tip_isplate_joppd
            line.append(self._quoted('4')) #gotovina
# opis_troska
            description = expense.name
            line.append(self._quoted(expense.name))
# kolicina
            qty = expense.unit_quantity
            line.append(self._quoted(qty))
# cijena
            price = expense.unit_amount
            line.append(self._quoted(price))
# valuta
            currency_name = expense.currency_id.name
            line.append(self._quoted(currency_name))
# tecaj    
            currency_rate = expense.lcy_rate
            line.append(self._quoted(currency_rate))
# oznaka_pdv
            line.append(self._quoted('0'))

            data = self._delimiter().join(line)
            lines.append(data)
        csv_rows = '\n'.join(lines)
        return (csv_rows)

    def _csv_lines(self, cr, uid, travel_orders, context=None):
        csv = []
        self._set_decimal_point(self._decimal())
        for to in travel_orders:
            # hr.travel.order
            document_csv = self._document(cr, uid, to, context)
            csv.append(document_csv)
            # daily.allowance.lines
            if to.daily_allowance_ids:
                allowances_csv = self._allowances(cr, uid, to.daily_allowance_ids, context)
                csv.append(allowances_csv)
            # hr.expense.line
            if to.expense_line_ids:
                expenses_csv = self._expenses(cr, uid, to.expense_line_ids, context)
                csv.append(expenses_csv)
        
        self._set_decimal_point()  # reset decimal point to default
        return csv

    def _set_decimal_point(self, frm=''):
        if frm == '.':
            locale.setlocale(locale.LC_NUMERIC, 'en_US.utf8')
        elif frm == ',':
            locale.setlocale(locale.LC_NUMERIC, 'hr_HR.utf8')
        else:
            locale.setlocale(locale.LC_ALL, '')  # reset to system default

    def generate_csv(self, cr, uid, ids, context=None):

        if context is None:
            context = {}
        self.form = self.read(cr, uid, ids)[0]
        active_model = context.get('active_model', None)
        active_ids = context.get('active_ids', [])
        sorted_ids = self.pool.get(active_model).search(cr, uid, [('id', 'in', active_ids)] , order='name', context=context)
        travel_orders = self.pool.get(active_model).browse(cr, uid,sorted_ids, context=context)
        csv_lines = self._csv_lines(cr, uid, travel_orders, context)
        data = '\n'.join(csv_lines)
        if len(active_ids) == 1 :
            # ima datoteke se sastoji od broja putnog naloga
            filename = 'trave_order_{}.csv'.format(travel_orders.name.replace('/', '_'))
        else:
            # ako ima više računa, ime datoteke ima ukupni putnih naloga
            filename = 'trave_order_{}.csv'.format(len(active_ids))
        self.write(cr, uid, ids, {'data': base64.encodestring(data.encode(self._encoding())),
                                  'name':filename,
                                  'state':'get'}, context=context)
        # ovaj dictionary sadrži podatke kao i record 'action_export_opportunity_for_ds_wizard' u xml-u 
        # tako da po povratku iz ove metode opet otvori takav prozor
        return {
        'context': context,
        'view_type': 'form',
        'view_mode': 'form',
        'res_model': 'ccg.travel.order.total.export',
        'res_id': ids[0],
        'view_id': False,
        'type': 'ir.actions.act_window',
        'target': 'new',
        'name' : 'Export for TOTAL',
         }

