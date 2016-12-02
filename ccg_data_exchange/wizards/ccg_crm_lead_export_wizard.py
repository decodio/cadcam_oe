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
from datetime import datetime
import base64

class crm_lead_export_for_ds(osv.osv_memory): # orm.TransientModel
    _name = 'crm.lead.export.for.ds'
    
    _columns = {
        'data': fields.binary('File', readonly=True),
        'name': fields.char('Filename', size=32, readonly=True),
        'state': fields.selection((('choose', 'choose'), ('get', 'get'),)),
        'delimiter': fields.selection(((',', ', (comma)'), (';', '; (semicolon)'), ('\t', '(tab)'),), default=','),
        'quotation': fields.selection((('"', '"'), ("'", "'"), ('', '(none)'),), default='"'),
    }
    
    _field_mappings = { 
        'CustomerName':('res_partner', 'name', 'partner_name'),
        'CustomerCity':('res_partner', 'city', 'city'),
        'CustomerCountry':('res_country', 'name', 'country'),
        'CustomerZipPostcode':('res_partner', 'zip', 'zip'),
        'OfferName':('ccg_offer_name', 'name', 'offer_name'),
        'RevenueAmount':('crm_lead', 'planned_revenue', 'planned_revenue'),
        'RevenueCurrency':('', "'EUR'", 'currency'),
        'PartnerOpportunityID':('crm_lead', 'lead_ref_no', 'opportunity_id'),
        'SalesStage':('crm_case_stage', 'name', 'sales_stage'),
        'ForecastCategory':('crm_case_stage', 'name', 'forecast_category'),
        'CloseDate':('crm_lead', 'date_deadline', 'close_date'),
        'RevenueType':('crm_lead', 'revenue_type', 'revenue_type'),
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

    def _quotation(self):
         return self.form['quotation']
 
    def _delimiter(self):
         return self.form['delimiter']

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
        FROM crm_lead LEFT JOIN res_partner ON (crm_lead.partner_id=res_partner.id)
        LEFT JOIN crm_case_stage ON (crm_lead.stage_id = crm_case_stage.id) 
        LEFT JOIN res_country ON (res_partner.country_id = res_country.id)
        LEFT JOIN ccg_offer_name ON (crm_lead.offer_name_id = ccg_offer_name.id)
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
            for ds_field_name in self._field_mappings.keys():
                value = self._field_mappings[ds_field_name]
                crm_field_name = value[2] or value[1]
                field_value = row[crm_field_name]
                if not field_value:
                   raise osv.except_osv(_('Export Error!'), _('Missing field {} in opportunity {}!'.format(crm_field_name, opportunity_id)))

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
        header = self._delimiter().join(self._field_mappings.keys())
        lines, filename = self._csv_lines(cr, uid, context)
        if header and lines:
            data = header + '\n' + lines
        self.write(cr, uid, ids, {'data': base64.encodestring(data.encode('utf-8')), 
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
