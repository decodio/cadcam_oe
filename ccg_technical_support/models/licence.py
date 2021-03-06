# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
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

from openerp.osv import fields, osv
from datetime import date, timedelta,datetime


class ccg_license(osv.osv):

    "Class holds information about Dassault Systemes license"

    def _get_cc_list(self, cr, uid, ids, field_name, arg, context=None):
        emails = []
        lics = self.browse(cr, uid, ids)
        ret = {}
        if lics:
            for l in lics:
                for r in l.cc_recipient_ids:
                    emails.append(r.partner_id.email)
            
            cc_list = ','.join([ e for e in emails])
            ret ={ids[0]:cc_list}
        return ret             

    def _get_to_emails(self, cr, uid, ids, field_name, arg, context=None):
        emails = []
        lics = self.browse(cr, uid, ids)
        ret = {}
        if lics:
            l = lics[0]
            if  l.client_id.user_id : # salesman on customer form
                emails.append(l.client_id.user_id.email) 
            if  l.user_id and (l.user_id !=l.client_id.user_id): # salesman on license form (if different)
                emails.append(l.user_id.email)
            
            to_list = ','.join([ e for e in emails])
            ret ={ids[0]:to_list}
        return ret

    def _get_default_days(self):
        obj = self.pool.get('days.before.expiration')
        cr = self.pool.cursor()
        uid = 1
        ids = obj.search(cr, uid, [('number_of_days', 'in', [30,15,7])], order='number_of_days desc')
        return ids


    _name="ccg.licence"
    _order = "client_id asc, expiration_date desc"
    _columns={
            'client_id' :fields.many2one('res.partner','Client', help='License user', domain=[('customer', '=', True), ('is_company', '=', True)]),
            'company_id':fields.many2one('res.company','Company',help='Company'),
            'user_id'   :fields.many2one('res.users','Salesman',help='Salesman'),
            'ib_number' :fields.char('IB Number',size=64, help='IB Number'),
            'portfolio' :fields.char('Portfolio', size=64,help='Portfolio'),
            'trigram'   :fields.char('Trigram', size=64,help='Trigram'),
            'start_date' :fields.date('Start Date',help='Start Date'),
            'activation_date':fields.date('Activation Date',help='Activation Date'),
            'expiration_date'  :fields.date('Expiration Date', help='Expiration Date'),
            'quantity'  :fields.integer('Quantity', help='Number of issued licenses'),
            'note'      :fields.text('Note', help='Notes about licence'),
            'supplier_id'  :fields.many2one('res.partner', 'Supplier', help='Licence supplier', domain=[('supplier', '=', True), ('is_company', '=', True)]),
            'active'    :fields.boolean('Active', help='Is licence active or expired'),
            'notify'    :fields.boolean('Send notifications', help='System send notifications about expiration'),
            'cc_recipient_ids' :fields.many2many('res.users', 'ccg_licence_user_rel', 'licence_id', 'user_id', string='CC', help='Users which receives notifications about licence expiration'),
            'cc_emails' : fields.function(_get_cc_list, type='char', readonly=False, store=True),
            'to_emails' : fields.function(_get_to_emails, type='char', readonly=False, store=True),
            'days_before_expiration'  :fields.many2many ('days.before.expiration', 'ccg_licence_days_rel','licence_id','days_id', string='Days before expiration', help='Number of days before expiration to send notification', default=_get_default_days),
            'licence_category_id' : fields.many2one('invoice.licence.category', 'Licence Category'),
            
    }
    _defaults = {
         'notify': True,
         'active': True,
    }
    _offset = [28, 14, 7]
    
    def name_get(self, cr, user, ids, context=None):
        ret = []
        for id in ids:
            licence_obj = self.browse(cr, user, id, context=context)
            if licence_obj.client_id :
                ret.append((id, '{} [{}]'.format(licence_obj.client_id.name, licence_obj.trigram or '')))
        return ret

    def _get_licences(self, cr, uid, context={}):
        args = [('notify','=', True), ('active','=', True)]
        ids=self.search(cr, uid, args, context=context)
        licences = self.browse(cr, uid, ids, context=context)
        lic_ids = []
        for lic in licences:
            for d in lic.days_before_expiration:
                if lic.expiration_date:
                    expiration_date = datetime.strptime(lic.expiration_date, "%Y-%m-%d").date()
                    days_to_expiration = (expiration_date - date.today()).days
                    if days_to_expiration == d.number_of_days:
                        lic_ids.append(lic.id)
        return lic_ids

    def _send_email(self, cr, uid, ids, context=None):
        email_template_obj = self.pool.get('email.template')
        template_ids = email_template_obj.search(cr, uid, [('name', '=','Licence Expiration Template')], context=context) 
        if template_ids:
            for sender_id in ids:
                msg_id = email_template_obj.send_mail(cr, uid, template_ids[0], sender_id, force_send=True,context=context)
            return True
        return False

    def check_licence_expiration(self, cr, uid, context={}):
        """
            Called by cron job
        """
        send_list = self._get_licences(cr, uid, context)
        if send_list:
            self._send_email(cr, uid, send_list, context=context)

# 
# ir_mail_server.build_email(
#                         email_from=mail.email_from,
#                         email_to=email.get('email_to'),
#                         subject=email.get('subject'),
#                         body=email.get('body'),
#                         body_alternative=email.get('body_alternative'),
#                         email_cc=tools.email_split(mail.email_cc),
#                         reply_to=mail.reply_to,
#                         attachments=attachments,
#                         message_id=mail.message_id,
#                         references=mail.references,
#                         object_id=mail.res_id and ('%s-%s' % (mail.res_id, mail.model)),
#                         subtype='html',
#                         subtype_alternative='plain',
#                         headers=headers)

ccg_license()