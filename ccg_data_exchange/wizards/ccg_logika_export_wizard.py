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
#import openerp.addons.decimal_precision as dp
from openerp import models, fields, api, _
from openerp.exceptions import Warning 
from openerp.osv import orm, osv, fields
from datetime import datetime, date
from Crypto import SelfTest
import base64
import csv
#from pyxb import namespace

class crm_logika_export(osv.osv_memory): # orm.TransientModel
    _name = 'crm.logika.export'
    _columns = {
        'data'      : fields.binary('File', readonly=True),
        'name'      : fields.char('Filename', size=32, readonly=True),
        'state'     : fields.selection((('create', 'create'), ('get', 'get'),), default = 'create'),
        'delimiter' : fields.selection(((',', ', (comma)'), (';', '; (semicolon)'), ('\t', '(tab)'),), default=','),
        'quotation' : fields.selection((('"', '"'), ("'", "'"), ('', '(none)'),), default='"'),
        'encoding'  : fields.selection((('utf-8', 'utf-8'), ("windows-1250", "windows-1250")), default='utf-8'),
    }

    def _quotation(self):
        return self.form['quotation']
 
    def _delimiter(self):
        return self.form['delimiter']
     
    def _encoding(self):
        return self.form['encoding']

    def _document(self, cr, uid, id, context=None):
        active_model = context.get('active_model', None)
        active_id = id
        invoice_obj  = self.pool.get(active_model).browse(cr, uid, id, context=context)
        invoice = invoice_obj.browse(active_id)
        
 # A: Header - Vrijednost 1 obavezna u svakom retku
        invoice_data = ['1']
 # B: Alt. broj - Alternativni broj računa (broj za Total se generira automatski)
        invoice_data.append( invoice.internal_invoice_number)
 # C: Datum - Datum računa
        invoice_data.append(invoice.date_invoice)
 # D: Datum isporuke - Datum isporuke tj- datum otpreme
        invoice_data.append(invoice.date_delivery)
 # E: Rok plaćanja - Rok plaćanja u danima
        total_days = 0
        if invoice.payment_term:
            for term in invoice.payment_term.line_ids:
                total_days+=term.days
        invoice_data.append(str(total_days))
        
 # F: Valuta - Šifra valute za račun (191 = HRK itd.)
        currency_code = {'EUR':'978','HRK':'191', 'USD':'840'}.get(invoice.currency_id.name)
        invoice_data.append( currency_code)
 # G: Tečaj - Tečaj računa (za HRK upisati iznos 1)
        invoice_data.append(str(invoice.lcy_rate))
# H: Uvodni tekst - Uvodni tekst računa (1000 znakova)
        invoice_data.append('Invoice description')
        
        data = self._delimiter().join(invoice_data)
 
        partner_id = invoice.partner_id
        lines = invoice.invoice_line
        print data,partner_id, lines
        return (data, invoice.partner_id, lines)
    
    def _partner(self, cr, uid, partner, context=None):
        fields = [
        ]
        # A: Header - Vrijednost 2 obavezna u svakom retku
        partner_data = ['2']
        # B: OIB - OIB partnera prema koje će se pronaći šifra partnera
        partner_data.append(partner.vat.replace('HR', ''))
        # C: Naziv partnera - Naziv partnera (opcionalno)
        partner_data.append(partner.name)
        # D: Poštanski broj - Poštanski broj mjesta partnera (opcionalno)
        partner_data.append(partner.zip)
        # E: Naziv mjesta - Naziv mjesta partnera (opcionalno)
        partner_data.append(partner.city)
        # F: Šifra države - Šifra države partnera (opcionalno)
        partner_data.append('')
        # G: Adresa - Adresa i kućni broj partnera (opcionalno)
        partner_data.append(partner.street)

        data = self._delimiter().join(partner_data)
        print partner_data
        print data
        return data
    
    def _items(self, cr, uid, lines, context=None):
        data = []
        for line in lines:
# A: Header - Vrijednost 3 obavezna u svakom retku
            line_data = ['3']
# B: Kataloški broj - Kataloški broj artikla
            line_data.append(str(line.product_id.id))
# C: Količina - Prodana količina artikla
            line_data.append(str(line.quantity))
# D: Oznaka stope PDV - 0 = 0%, 2 = 10%, 4 = 25%, 5 = 5%
            line_data.append(line.invoice_line_tax_id[0].name)
# E: Oznaka oslobođ. PDV - Ako nema oslobođenja PDV ostaviti prazno
            line_data.append('')
# F: Cijena - Veleprodajna cijena prodanog artikla
            line_data.append(str(line.price_unit))
# G: Rabat - Odobreni rabat
            line_data.append(str(line.discount))
# H: Opis artikla - Dodatni opis za ovu stavku ako postoji
            line_data.append(line.product_id.name)
            line_csv = self._delimiter().join(line_data)
            data.append(line_csv)
            
        return '\n'.join(data)

    def _csv_lines(self, cr, uid, ids, context=None):
        csv = []
        for id in ids:
            print id
            (data, partner_id, lines) = self._document(cr, uid, id, context)
            csv.append(data)
            csv.append(self._partner(cr, uid, partner_id, context))
            csv.append(self._items(cr, uid, lines, context))
        
        return csv

    def generate_csv(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        self.form = self.read(cr, uid, ids)[0]
        active_ids = context.get('active_ids', [])
        print context
        csv = self._csv_lines(cr, uid, active_ids, context)
        data = '\n'.join(csv)
        filename = 'invoice.csv'
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

    pass
