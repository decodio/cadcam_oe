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
import base64
from pyxb import namespace

class crm_lead_export_for_ds(osv.osv_memory): # orm.TransientModel
    _name = 'crm.lead.export.for.ds'
    
    _columns = {
        'data'      : fields.binary('File', readonly=True),
        'name'      : fields.char('Filename', size=32, readonly=True),
        'state'     : fields.selection((('choose', 'choose'), ('get', 'get'),)),
        'delimiter' : fields.selection(((',', ', (comma)'), (';', '; (semicolon)'), ('\t', '(tab)'),), default=','),
        'quotation' : fields.selection((('"', '"'), ("'", "'"), ('', '(none)'),), default='"'),
        'encoding'  : fields.selection((('utf-8', 'utf-8'), ("windows-1250", "windows-1250")), default='utf-8'),
    }
    
    _field_mappings = { # 0-table, 1-field, 2-alias, 3-string, 4-active, 5-required
        'CustomerName'      : ('res_partner', 'name', 'partner_name', 'Customer', True, True  ),
        'CustomerCity'      : ('res_partner', 'city', 'city', 'City', True, True ),
        'CustomerCountry'   : ('res_country', 'name', 'country', 'Country', True, True ),
        'CustomerZipPostcode' : ('res_partner', 'zip', 'zip', 'ZIP', True, True ),
        'OfferName'         : ('ccg_offer_name', 'name', 'offer_name', 'Offer name', True, True ),
        'RevenueAmount'     : ('crm_lead', 'ds_expected_revenue', 'planned_revenue', 'Expected revenue for DS', True, True ),
        'RevenueCurrency'   : ('', "'EUR'", 'currency', 'Currency', True, True ),
        'PartnerOpportunityID' : ('crm_lead', 'lead_ref_no', 'opportunity_id', 'Opportunity ID', True, True ),
        'SalesStage'        : ('crm_case_stage', 'name', 'sales_stage', 'Sales stage', True, True ),
        'ForecastCategory'  : ('crm_case_stage', 'name', 'forecast_category', 'Forecast category', True, True ),
        'CloseDate'         : ('crm_lead', 'date_deadline', 'close_date', 'Expected closing', True, True ),
        'RevenueType'       : ('crm_lead', 'revenue_type', 'revenue_type', 'Revenue type', True, True ),
        'CustomerContactName'       : ('partner_contact', 'name', 'contact_name', 'Customer Contact Name', False, False),
        'CustomerContactFirstName'  : ('', "''", 'contact_first_name', 'Customer Contact First Name', True, True ),
        'CustomerContactLastName'   : ('', "''", 'contact_last_name', 'Customer Contact LastName', True, True ),
        'CustomerContactEmail'  : ('partner_contact', 'email', 'contact_email', 'Customer Contact Email', True, True ),
        'DSLeadID'              : ('crm_lead', 'ds_lead_id', 'ds_lead_id', 'DS Lead ID', True, False ),
        }
    
    _stage_mapping = {
        'New':('1-Sales Lead', 'Upside'),
        'Validation' : ('2-Validate Opportunity', 'Upside'),
        'Establish value' : ('3-Establish Value', 'Commit'),
        'Negotiation' : ('4-Reach Agreement', 'Safe'),
        'Won' : ('Closed/Won', 'Won'),
        'Lost' : ('Closed/Lost', 'Lost'),
        }

    def default_get(self, cr, uid, fields, context=None):
        res = super(crm_lead_export_for_ds, self).default_get(cr, uid, fields, context=context)
        res['state'] = 'choose'
        return res

    def map_stage(self, cr, uid, row, context=None):
        sales_stage = row['sales_stage']
        new_stage = self._stage_mapping[sales_stage][0]
        forecast_category = row['forecast_category']
        new_forecast_category = self._stage_mapping[forecast_category][1]
        row.update({'sales_stage':new_stage, 'forecast_category':new_forecast_category})
        return row
    
    def split_contact_name(self, cr, uid, row, context=None):
        contact_name = row['contact_name']
        if contact_name:
            names = contact_name.split()
            first_name = names[0]
            last_name = " ".join([ln for ln in names[1:] if ln])
        else:
            opportunity_id = row['opportunity_id']
            field_label = self._field_mappings['CustomerContactName'][3]
            raise osv.except_osv(_('Export Error!'), _('Missing field "{}" in opportunity "{}"!'.format(field_label, opportunity_id)))
        row.update({'contact_first_name':first_name, 'contact_last_name':last_name})
        return row
    
    def _quotation(self):
        return self.form['quotation']
 
    def _delimiter(self):
        return self.form['delimiter']
     
    def _encoding(self):
        return self.form['encoding']

    def _get_opportunity_fields(self, cr, uid, context=None):
        ids = context.get('active_ids', [])
        fields = []
        for key in self._field_mappings.keys():
            value = self._field_mappings[key]
            table = value[0]
            field = value[1]
            alias = value[2] or field
            if table:
                fields.append('{}.{} as {}'.format(table, field, alias))
            else:
                fields.append('{} as {}'.format(field, alias))
        
        sql = '''
        SELECT {}
        FROM crm_lead 
        LEFT JOIN res_partner ON (crm_lead.partner_id=res_partner.id)
        LEFT JOIN crm_case_stage ON (crm_lead.stage_id = crm_case_stage.id) 
        LEFT JOIN res_country ON (res_partner.country_id = res_country.id)
        LEFT JOIN ccg_offer_name ON (crm_lead.offer_name_id = ccg_offer_name.id)
        LEFT JOIN res_partner partner_contact ON (crm_lead.contact_name_id=partner_contact.id)
        WHERE crm_lead.id in ({})
        '''.format(','.join([f for f in fields ]), ','.join([str(i) for i in ids]))
        cr.execute(sql)
        return  cr.dictfetchall()

    def _csv_lines(self, cr, uid, context=None):
        data = self._get_opportunity_fields(cr, uid, context)
        lines = []
        for row_original in data:
            line = []
            opportunity_id = row_original['opportunity_id']
            row = self.map_stage(cr, uid, row_original, context)
            row = self.split_contact_name(cr, uid, row, context)
            for ds_field_name in self._field_mappings.keys():
                value = self._field_mappings[ds_field_name]
                if value[4]: # is active
                    crm_field_name = value[2] or value[1]
                    field_value = row[crm_field_name]
                    required = value[5]
                    if required and not field_value:
                       field_label = value[3]
                       raise osv.except_osv(_('Export Error!'), _('Missing field "{}" in opportunity "{}"!'.format(field_label, opportunity_id)))
                    if crm_field_name == 'close_date':
                        field_value = '{}.{}.{}'.format(field_value[8:10],field_value[5:7],field_value[0:4])
                    field_value_strnig = '{1}{0}{1}'.format(field_value, self._quotation())
                    line.append(field_value_strnig)
            csv_line = self._delimiter().join(line)   
            lines.append(csv_line)
        if len(lines) > 1:
            csv_file_name ='opportunities.csv'
        else:
            csv_file_name = 'opportunity_{}.csv'.format(opportunity_id)
        return '\n'.join(lines), csv_file_name
    
    def generate_csv(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        self.form = self.read(cr, uid, ids)[0]
        header = self._delimiter().join([k for k in self._field_mappings.keys() if self._field_mappings[k][4]])
        lines, filename = self._csv_lines(cr, uid, context)
        if header and lines:
            data = header + '\n' + lines
        self.write(cr, uid, ids, {'data': base64.encodestring(data.encode(self._encoding())), 
                                  'name':filename, 
                                  'state':'get'}, context=context)
        # ovaj dictionary sadrži podatke kao i record 'action_export_opportunity_for_ds_wizard' u xml-u 
        # tako da po povratku iz ove metode opet otvori takav prozor
        return {
        'context': context,
        'view_type': 'form',
        'view_mode': 'form',
        'res_model': 'crm.lead.export.for.ds',
        'res_id': ids[0],
        'view_id': False,
        'type': 'ir.actions.act_window',
        'target': 'new',
        'name' : 'Export for DS portal',
         }
