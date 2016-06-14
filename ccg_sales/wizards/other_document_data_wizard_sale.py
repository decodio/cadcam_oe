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

class CertificateDataWizard(models.TransientModel):
    _name = 'certificate.data.wizard'

    certificate_data_sale_ids = fields.Many2many('other.sale.data.certificates','wizard_certificate_data_sale_rel','wizard_id','certificate_data_sale_id', 'Certificates')

    @api.multi
    def populate_data(self):
        if self._context.get('active_ids') and self._context.get('active_model'):
            active_ids = self._context['active_ids']
            active_model = self._context['active_model']
            print active_model
            model = self.env[active_model]
        if self.certificate_data_sale_ids and active_ids:
            document = model.browse(active_ids)
            vals = {}
            for line in self.certificate_data_sale_ids:
                if active_model == 'account.invoice':
                    vals.update({'invoice_id': active_ids[0]})
                if active_model == 'sale.order':
                    vals.update({'sale_id': active_ids[0]})
                vals.update({'description': line.description})
                document.price_ids.create(vals)
