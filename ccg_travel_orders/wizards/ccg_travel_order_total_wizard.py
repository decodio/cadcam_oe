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
from datetime import datetime, date, timedelta
import csv
import locale
import base64
from pytz import timezone
from time import strptime, strftime
from codes_translation import get_country_code


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

    _travel_order_name = ''

    def get_currency_code(self, cr, uid, currency_name, context=None):
        obj = self.pool.get('currency.mapping')
        ids = obj.search(cr, uid, [('currency_name', '=', currency_name)], context=context)
        currency_codes = obj.browse(cr, uid, ids, context=context)
        if currency_codes:
            return currency_codes[0].total_id
        else:
            return False

    def get_expense_id(self, cr, uid, ccg_product_id, context=None):
        obj = self.pool.get('expense.mapping')
        ids = obj.search(cr, uid, [('product_id', '=', ccg_product_id)], context=context)
        expenses = obj.browse(cr, uid, ids, context=context)
        if expenses:
            return expenses[0].total_id
        else:
            return False

    def get_transportation_type(self, cr, uid, crm_transportation_id, context=None):
        obj = self.pool.get('transportation.mapping')
        ids = obj.search(cr, uid, [('transportation_id', '=', crm_transportation_id)], context=context)
        transportations = obj.browse(cr, uid, ids, context=context)
        if transportations:
            return transportations[0].total_id
        else:
            return False

    def get_employee_id(self, cr, uid, company_id, ccg_employee_id, context=None):
        obj = self.pool.get('employee.mapping')
        ids = obj.search(cr, uid, [('company_id', '=', company_id),('employee_id','=',ccg_employee_id)], context=context)
        employees = obj.browse(cr, uid, ids, context=context)
        if employees :
            return employees[0].total_id
        else:
            return False

    def get_responsible_person_id(self, cr, uid, company_id, context=None):
        obj = self.pool.get('responsible.person.mapping')
        ids = obj.search(cr, uid, [('company_id', '=', company_id)], context=context)
        responsible_persons = obj.browse(cr, uid, ids, context=context)
        if responsible_persons :
            return responsible_persons[0].total_id
        else:
            return False

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

    def _trim(self, text):
        if text:
            s = text.replace('\n', ' ').replace(';', '.')
            return s
        else:
            return ""


    def _reformat_date(self, date):
        dd = date[8:10]
        mm = date[5:7]
        yyyy = date[0:4]
        return '{}.{}.{}'.format(dd, mm, yyyy)

    def _reformat_datetime(self, datetime_str, sec=False):
        fmt_in = '%Y-%m-%d %H:%M:%S'
        fmt_out = '%d.%m.%Y %H:%M:%S'
        t = datetime.strptime(datetime_str, fmt_in)
        localtime =  timezone('UTC').localize(t).astimezone(timezone("Europe/Zagreb"))
        return localtime.strftime( fmt_out)

    def _document(self, cr, uid, travel_order, context=None):
        line=[]
# header - Vrijednost 1 obavezna u svakom retku
        line.append(self._quoted('1'))
# datum_naloga (+)
        if travel_order.document_date:
            document_date = self._reformat_date(travel_order.document_date)
            document_datetime = '{} {}'.format(document_date,travel_order.create_date[-8:])
            line.append(document_datetime)
        else:
            raise Warning(_("Missing or invalid document date in travel order {} ({})!".format(self._travel_order_name, travel_order.employee_id.name)))
# datum_isplate (+)
        if travel_order.date_liquidation:
            date_liquidation = self._reformat_date(travel_order.date_liquidation)
            line.append(date_liquidation)
        else:
            raise Warning(_("Missing or invalid date liquidation in travel order {} ({})!".format(self._travel_order_name, travel_order.employee_id.name)))
# sifra_zaposlenika_putnika
        employee_id = self.get_employee_id(cr, uid, travel_order.company_id.id,travel_order.employee_id.id)
        if employee_id:
            line.append(self._quoted(employee_id))
        else:
            raise Warning(_("Missing or invalid employee in travel order {}!".format(self._travel_order_name)))
# sifra_zaposlenika_odobritelja
        responsible_person_id = self.get_responsible_person_id(cr, uid,travel_order.company_id.id)
        if responsible_person_id:
            line.append(self._quoted(responsible_person_id))
        else:
            raise Warning(_("Missing or invalid responsible person in travel order {} ({})!".format(self._travel_order_name, travel_order.employee_id.name)))
# datum_i_vrijeme_odlaska
        date_from = self._reformat_datetime(travel_order.date_from)
        line.append(self._quoted(date_from))
# datum_i_vrijeme_povratka
        date_to = self._reformat_datetime(travel_order.date_to)
        line.append(self._quoted(date_to))
# pbr_mjesto_polaska
        departure_city_zip = travel_order.company_id.zip
        line.append(self._quoted(departure_city_zip))
# pbr_mjesto_odrediste (*)
#         city_destination = travel_order.dest_city.split(',')
#         line.append(city_destination[0])
        if travel_order.partner_ids:
            destination_partner = travel_order.partner_ids[0]
            if destination_partner.zip:
                destination_city_zip = destination_partner.zip
            else:
                destination_city_zip = ''
        else:
            destination_city_zip = ''
        line.append(self._quoted(destination_city_zip))

# opis_putovanja
        purpose = travel_order.purpose[:200] if travel_order.purpose else ""
        if not purpose:
            raise Warning(_("Missing purpose of travel order {} ({})!".format(self._travel_order_name, travel_order.employee_id.name)))
        else:
            line.append(self._trim(purpose))
# tip_prijevozno_sredstvo
        depart_transportation_type = self.get_transportation_type(cr, uid, travel_order.depart_transportation[0].id)
        if depart_transportation_type:
            line.append(self._quoted(depart_transportation_type))
        else:
            raise Warning(_("Missing or invalid transportation type in travel order {} ({})!".format(self._travel_order_name, travel_order.employee_id.name)))
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
            odometer_start = '0'
        line.append(self._quoted(odometer_start))
# odobreni_predujam
        advance_payment = travel_order.advance_payment
        line.append(self._quoted(locale.str(advance_payment)))
# valuta_za_predujam
        if travel_order.currency_id:
            advance_currency_code = self.get_currency_code(cr, uid, travel_order.currency_id.name)
        else:
            advance_currency_code = ''

        if advance_currency_code:
            line.append(self._quoted(advance_currency_code))
        else:
             raise Warning(_("Missing or invalid currency for advance payment in travel order {} ({})!".format(self._travel_order_name, travel_order.employee_id.name)))
# putno_izvjesce
        report = travel_order.other_data
        if not report:
            raise Warning(_("Missing travel order report (Other Data) in travel order {} ({})!".format(self._travel_order_name, travel_order.employee_id.name)))
        else:
            line.append(self._trim(report))

        csv_row = self._delimiter().join(line)
        return csv_row

    def _allowances(self, cr, uid, allowances, travel_order,context=None):
        lines = [ ]
        for allowance in allowances:
            line = [ ]
# Header - Vrijednost 2 obavezna u svakom retku
            line.append( self._quoted('2'))
# sifra_drzave
            country_code = get_country_code(allowance.country_id.code)
            if country_code:
                line.append( self._quoted(country_code))
            else:
             raise Warning(_("Missing or invalid currency for advance payment in travel order {} ({})!".format(self._travel_order_name, travel_order.employee_id.name)))

# datum_i_vrijeme_izlaska
# TODO convert datetime fron UTC to local time!!!
            date_to = allowance.date_to
            line.append(self._reformat_datetime(date_to))
            data = self._delimiter().join(line)
            lines.append(data)
        csv_rows = '\n'.join(lines)
        return (csv_rows)

    def _expenses(self, cr, uid, expenses, travel_order, context=None):
        lines = []
        for expense in expenses:
            line = []
# header - Vrijednost 3 obavezna u svakom retku
            line.append(self._quoted('3'))
# vrsta_putnog_troska
            expense_type = self.get_expense_id(cr, uid, expense.product_id.id)
            if expense_type:
                line.append(self._quoted(expense_type))
            else:
                raise Warning(_("Missing or invalid expense type for '{}' in travel order {} ({})!".format(expense.name, self._travel_order_name, travel_order.employee_id.name)))
# oznaka_placeno
            paid = 1 if expense.journal_id.type == 'bank' else 0
            line.append(self._quoted(paid)) # nije plaćeno
# tip_isplate_joppd
            line.append(self._quoted('0')) #ostalo
# opis_troska
            line.append(self._quoted(expense.name))
# kolicina
            qty = expense.unit_quantity
            line.append(self._quoted(locale.str(qty)))
# cijena
            price = expense.unit_amount
            line.append(self._quoted(locale.str(price)))
# valuta
            currency_name = expense.currency_id.name
            currency_code = self.get_currency_code(cr, uid, expense.currency_id.name)
            if currency_code:
                line.append(self._quoted(currency_code))
            else:
                raise Warning(_("Missing or invalid currency for expense '{}' in travel order {} ({})!".format(expense.name,self._travel_order_name, travel_order.employee_id.name)))
# tecaj
            currency_rate = expense.lcy_rate
            line.append(self._quoted(locale.str(currency_rate)))
# oznaka_pdv
            line.append(self._quoted(''))

            data = self._delimiter().join(line)
            lines.append(data)

        csv_rows = '\n'.join(lines)
        return (csv_rows)

    def _itinerary_expenses(self, cr, uid, itinerary_lines, travel_order,context=None):
        lines = []
        for itinerary in itinerary_lines:
            line = []
# header - Vrijednost 3 obavezna u svakom retku
            line.append(self._quoted('3'))
# vrsta_putnog_troska = 1 (kilomterina)
            line.append( self._quoted('1') )
# oznaka_placeno
            line.append(self._quoted(0)) # nije unaprijed plaćeno
# tip_isplate_joppd - za privatni auto = 4 Isplata u gotovini, za službeni = 0 - nije plaćeno
            if itinerary.vehicle_id.type == 'private':
                line.append(self._quoted('4')) # kilometrina se isplaćuje u gotovini
            else: # službeni
                line.append(self._quoted('0')) # kilometrina se ne isplaćuje
# opis_troska
            description = 'Kilometrina'
            line.append(self._quoted(description))
# kolicina
            qty = itinerary.distance
            line.append(self._quoted(locale.str(qty)))
# cijena
#            print itinerary.vehicle_type.lower(), itinerary.vehicle_id.name, itinerary.vehicle_id.type
            if itinerary.vehicle_id.type == 'private':
                price = 2.0 #HRK/km
            else:
                price = 0.0
            line.append(self._quoted(locale.str(price)))
# valuta
            currency_name = 'HRK'
            currency_code = self.get_currency_code(cr, uid, currency_name)
            line.append(self._quoted(currency_code))
# tecaj
            currency_rate = 1.0
            line.append(self._quoted(locale.str(currency_rate)))
# oznaka_pdv
            line.append(self._quoted(''))

            data = self._delimiter().join(line)
            lines.append(data)

        csv_rows = '\n'.join(lines)
        return (csv_rows)

    def _daily_allowance_expenses(self, cr, uid, daily_allowance_lines, travel_order, context=None):
        lines = []
        for allowance in daily_allowance_lines:
            if allowance.num_of_allowances:
                line = []
    # header - Vrijednost 3 obavezna u svakom retku
                line.append(self._quoted('3'))
    # vrsta_putnog_troska
                if allowance.currency_id.name == 'HRK':
                    expense_type = self._quoted('2')
                    description = 'Domaća dnevnica'
                else:
                    expense_type =  self._quoted('3')
                    description = 'Inozemna dnevnica'
                line.append( expense_type )
    # oznaka_placeno
                line.append(self._quoted(0)) # nije plaćeno
    # tip_isplate_joppd
                line.append(self._quoted('4')) # dnevnice
    # opis_troska
                line.append(self._quoted(description))
    # kolicina
                qty = allowance.num_of_allowances
                line.append(self._quoted(locale.str(qty)))
    # cijena
#                 price = allowance.allowance_amount_total
                price = allowance.allowance_unit_amount
                line.append(self._quoted(locale.str(price)))
    # valuta
                currency_name = allowance.currency_id.name
                currency_code = self.get_currency_code(cr, uid, currency_name)
                line.append(self._quoted(currency_code))
     # tecaj
                currency_rate = allowance.lcy_rate
                line.append(self._quoted(locale.str(currency_rate)))
    # oznaka_pdv
                line.append(self._quoted(''))

                data = self._delimiter().join(line)
                lines.append(data)

        csv_rows = '\n'.join(lines)
        return (csv_rows)

    def _csv_lines(self, cr, uid, travel_orders, context=None):
        csv = []
        self._set_decimal_point(self._decimal())
        for to in travel_orders:
            self._travel_order_name = to.name
            # hr.travel.order
            document_csv = self._document(cr, uid, to, context)
            csv.append(document_csv)
            # daily.allowance.lines
            if to.daily_allowance_ids:
                allowances_csv = self._allowances(cr, uid, to.daily_allowance_ids, to, context)
                csv.append(allowances_csv)
            # hr.expense.line
            if to.expense_line_ids:
                expenses_csv = self._expenses(cr, uid, to.expense_line_ids, to, context)
                csv.append(expenses_csv)
            # append itinerrary to expenses hr.travel.opder.itinerary.lines
            if to.itinerary_ids:
                itinerary_csv =self._itinerary_expenses(cr, uid, to.itinerary_ids, to, context)
                csv.append(itinerary_csv)
            # append daily allowances to expenses daily.allowance.lines
            if to.daily_allowance_ids:
                allowance_csv =self._daily_allowance_expenses(cr, uid, to.daily_allowance_ids, to, context)
                csv.append(allowance_csv)

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
            filename = 'travel_order_{}.csv'.format(travel_orders.name.replace('/', '_'))
        else:
            # ako ima više putnih naloga, ime datoteke ima ukupni broj putnih naloga
            filename = 'travel_order_{}.csv'.format(len(active_ids))

        self.write(cr, uid, ids, {'data': base64.encodestring(data.encode(self._encoding())),'name':filename,'state':'get'}, context=context)
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
