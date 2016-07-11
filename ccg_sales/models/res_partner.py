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

from openerp import models, fields, api, _, SUPERUSER_ID
from openerp.osv import fields, osv

class res_partner(models.Model):
    _inherit = 'res.partner'
    # remove check vat for SLO and BIH
    def check_vat(self, cr, uid, ids, context=None):
        for id in ids:
            partner_model = self.pool.get('res.partner').browse(cr, uid, id, context=context)
            if partner_model.vat and not partner_model.parent_id:
                vat = partner_model.vat
                if vat.isdigit() and partner_model.country_id.code in ['SI','BA']:
                    res = True # don't check vat without country code
                else:
                    res = super(res_partner, self).check_vat(cr, uid, ids, context=context)
            else:
                res = True
            
            return res
    
    constraints = [ (check_vat, '', ["vat"])]
