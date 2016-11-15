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

from openerp import models, fields, api, _, SUPERUSER_ID
from openerp.exceptions import except_orm, ValidationError, Warning, RedirectWarning

class PredefinedTextWizard(models.TransientModel):
    _name = 'predefined.text.wizard'
    
    text_id = fields.Many2one(string='Text', comodel_name='sale.order.predefined.text')
     
    def choose_text(self, cr, uid, ids, context=None):
        form = self.read(cr, uid, ids)[0]
        text = form['text_id']
        active_model = context.get('active_model', False)
        active_id = context.get('active_id', False)
        field_name = context.get('field', False)
        partner_id =  context.get('partner_id', False)
        partner_obj=self.pool.get('res.partner').browse(cr, uid, partner_id, context=context)
        obj = self.pool.get(active_model).browse(cr, uid, active_id, context=context)
        obj.write({field_name:text[1]})


