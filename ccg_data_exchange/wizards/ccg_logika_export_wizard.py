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

class crm_logika_export(osv.osv_memory):  # orm.TransientModel
    _name = 'crm.logika.export'

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

    def _document(self, cr, uid, id, context=None):
        active_model = context.get('active_model', None)
        active_id = id
        invoice_obj = self.pool.get(active_model).browse(cr, uid, id, context=context)
        invoice = invoice_obj.browse(active_id)
        
# A: Header - Vrijednost 1 obavezna u svakom retku
        invoice_data = [self._quoted('1')]
# B: Alt. broj - Alternativni broj računa (broj za Total se generira automatski)
        invoice_number = invoice.internal_invoice_number
        invoice_data.append(self._quoted(invoice_number))
# C: Datum - Datum računa
        invoice_data.append(self._quoted(self._reformat_date(invoice.date_invoice)))
# D: Datum isporuke - Datum isporuke tj- datum otpreme
#        invoice_data.append(self._quoted(self._reformat_date(invoice.date_delivery))) # neće se više koristiti
        invoice_data.append(self._quoted(''))  # šalje se prazno polje 
# E: Rok plaćanja - Rok plaćanja u danima
        date_format = '%Y-%m-%d'
        dd = datetime.strptime(invoice.date_due, date_format)
        di = datetime.strptime(invoice.date_invoice, date_format)
        date_delta = dd - di 
        if date_delta.days < 0:
               raise Warning(_("Wrong date in invoice {0}. Due date ({1:%d.%m.%Y}) is prior to the invoice date ({2:%d.%m.%Y})".format(invoice_number, dd, di)))
        invoice_data.append(self._quoted(date_delta.days))
# F: Valuta - Šifra valute za račun (191 = HRK itd.)
        currency_code = {'EUR':'978', 'HRK':'191', 'USD':'840'}.get(invoice.currency_id.name)
        invoice_data.append(self._quoted(currency_code))
# G: Tečaj - Tečaj računa (za HRK upisati iznos 1)
        invoice_data.append(self._quoted(locale.str(invoice.lcy_rate)))
# H: Uvodni tekst - Uvodni tekst računa (1000 znakova)
        invoice_data.append(self._quoted('Invoice description'))
        data = self._delimiter().join(invoice_data)
 
        partner_id = invoice.partner_id
        lines = invoice.invoice_line
        return (data, invoice_number, invoice.partner_id, lines)
    
    def _partner(self, cr, uid, partner, context=None):
        fields = [ ]
# A: Header - Vrijednost 2 obavezna u svakom retku
        partner_data = [self._quoted('2')]
# B: OIB - OIB partnera prema koje će se pronaći šifra partnera
        partner_data.append(self._quoted(partner.vat.replace('HR', '')))
# C: Naziv partnera - Naziv partnera (opcionalno)
        partner_data.append(self._quoted(partner.name))
# D: Poštanski broj - Poštanski broj mjesta partnera (opcionalno)
        partner_data.append(self._quoted(partner.zip))
# E: Naziv mjesta - Naziv mjesta partnera (opcionalno)
        partner_data.append(self._quoted(partner.city))
# F: Šifra države - Šifra države partnera (opcionalno)
        partner_data.append(self._quoted(''))
# G: Adresa - Adresa i kućni broj partnera (opcionalno)
        partner_data.append(self._quoted(partner.street))

        data = self._delimiter().join(partner_data)
        return (data, partner.name)
    
    def _items(self, cr, uid, lines, context=None):
        data = []
        for line in lines:
# A: Header - Vrijednost 3 obavezna u svakom retku
            line_data = [self._quoted('3')]
# B: Kataloški broj - Kataloški broj artikla - KONTO PRODUKTA će biti šifra!!!
            line_data.append(self._quoted(line.account_id.code[4:]))
# C: Količina - Prodana količina artikla
            line_data.append(self._quoted(locale.str(line.quantity)))
# D: Oznaka stope PDV - 0 = 0%, 2 = 10%, 4 = 25%, 5 = 5%
            tax_percent = line.invoice_line_tax_id[0].amount * 100
            tax_code = {0:'0', 10:'2', 25:'4', 5:'5'}.get(tax_percent, '-1')
            line_data.append(self._quoted(tax_code))
# E: Oznaka oslobođ. PDV - Ako nema oslobođenja PDV ostaviti prazno
            line_data.append(self._quoted(''))
# F: Cijena - Veleprodajna cijena prodanog artikla
            line_data.append(self._quoted(locale.str(line.price_unit)))
# G: Rabat - Odobreni rabat
            line_data.append(self._quoted(locale.str(line.discount)))
# H: Opis artikla - Dodatni opis za ovu stavku ako postoji (ako je prefix # opis pregazi naziv iz baze artikala)
            line_data.append(self._quoted('#' + line.product_id.name))
            line_csv = self._delimiter().join(line_data)
            data.append(line_csv)
            
        return '\n'.join(data)

    def _csv_lines(self, cr, uid, ids, context=None):
        csv = []
        for id in ids:
            (invoice_data, invoice_number, partner_id, lines) = self._document(cr, uid, id, context)
            csv.append(invoice_data)
            (partner_data, partner_name) = self._partner(cr, uid, partner_id, context)
            csv.append(partner_data)
            csv.append(self._items(cr, uid, lines, context))
        
        return (csv, invoice_number, partner_name)

    def _set_decimal_point(self, frm=''):
        if frm == '.':
            locale.setlocale(locale.LC_NUMERIC, 'en_US.utf8')
        elif frm == ',':
            locale.setlocale(locale.LC_NUMERIC, 'hr_HR.utf8')
        else:
            locale.setlocale(locale.LC_ALL, '')  # reset to system default

    def _sort_ids_by_invoice_number(self, cr, uid, ids, context=None):
        active_model = context.get('active_model', None)
        sorted_ids = self.pool.get(active_model).search(cr, uid, [('id', 'in', ids)], order='internal_invoice_number', context=context)
        return sorted_ids

    def generate_csv(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
            
        self.form = self.read(cr, uid, ids)[0]
        active_ids = context.get('active_ids', [])
        sorted_ids = self._sort_ids_by_invoice_number(cr, uid, active_ids, context=context)
        self._set_decimal_point(self._decimal())
        (csv, invoice, partner) = self._csv_lines(cr, uid, sorted_ids, context)
        self._set_decimal_point()  # reset decimal point to default
        
        data = '\n'.join(csv)
        if len(active_ids) == 1 :
            # ima datoteke se sastoji od broja računa i prvih 10 slova partnera
            filename = 'invoice_{}_{}.csv'.format(invoice, partner.replace('.', '_').replace(' ', '_')[:10])
        else:
            # ako ima više računa, ime datoteke ima ukupni broj računa
            filename = 'invoices_{}.csv'.format(len(active_ids))

        self.write(cr, uid, ids, {'data': base64.encodestring(data.encode(self._encoding())),
                                  'name':filename,
                                  'state':'get'}, context=context)
        # ovaj dictionary sadrži podatke kao i record 'action_export_opportunity_for_ds_wizard' u xml-u 
        # tako da po povratku iz ove metode opet otvori takav prozor
        return {
        'context': context,
        'view_type': 'form',
        'view_mode': 'form',
        'res_model': 'crm.logika.export',
        'res_id': ids[0],
        'view_id': False,
        'type': 'ir.actions.act_window',
        'target': 'new',
        'name' : 'Export for TOTAL',
         }

