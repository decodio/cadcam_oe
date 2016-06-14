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
# import email, mimetypes 
# from email.Header  import decode_header 
# from email.MIMEText  import MIMEText 



class ccg_license(osv.osv):

    "Class holds information about Dassault Systemes license"

    _name="ccg.licence"
    _order = "client_id asc, end_date desc"
    _columns={
            'client_id' :fields.many2one('res.partner','Client', help='License user', domain=[('customer', '=', True)]),
            'company_id':fields.many2one('res.company','Company',help='License user'),
            'user_id'   :fields.many2one('res.users','Salesman',help='Salesman'),
            'ib_number' :fields.char('IB Number',size=64, help='IB Number'),
            'portfolio' :fields.char('Portfolio', size=64,help='Portfolio'),
            'trigram'   :fields.char('Trigram', size=16,help='Trigram'),
            'start_date':fields.date('Start Date',help='Start Date'),
            'end_date'  :fields.date('End Date', help='Start Date'),
            'quantity'  :fields.integer('Quantity', help='Number of issued licenses'),
            'notify'    :fields.boolean('Send notifications', help='System send notifications about expiration'),
            'note'      :fields.text('Note', help='Notes about licence')
    }
    _defaults = {
         'notify': True,
    }
    
    def get_licenses(self, cr, uid, days, context={}):
        check_date = date.today() + timedelta(days=days)
        args = [('end_date','=', check_date), ('notify','=', True)]
        ids=self.search(cr, uid, args, context=context)
        return ids
    
    def send_notification_mail(self, cr, uid, msg="", recipients=[]):
        if recipients: 
            ir_mail_server = self.pool.get('ir.mail_server') 
            msg = ir_mail_server.build_email("Administrator <crm@cadcam-group.eu>", recipients, "License expire soon", msg) 
            ir_mail_server.send_email(cr, uid, msg)

    def check_and_notify(self, cr, uid, days=7, context={}):
        """
            search for licenses which expire in next 'days' days
            send notification e-mail
        """
        lic_ids = self.get_licenses(cr, uid, days)
        if lic_ids :
            msg = "Some licenses will expire in next {0} days:\n".format(days)
            line =  " - client: {0};  number: {1};  exp. date: {2}\n"
            for l in self.read(cr, uid, lic_ids, ['client_id', 'ib_number', 'end_date'], context):
                msg = msg +line.format(l['client_id'][1], l['ib_number'], datetime.strptime(l['end_date'], "%Y-%m-%d").strftime("%d.%m.%Y"))  

            self.send_notification_mail(cr, uid, msg=msg,recipients=[ "boris.kumpar@cadcam-group.eu", "nikola.marekovic@cadcam-group.eu" ])
        return lic_ids
        
    def check_licenses(self, cr, uid, context={}):
        """
            Called by cron job
        """
        self.check_and_notify( cr, uid, days=7, context=context)
        self.check_and_notify( cr, uid, days=15, context=context)
        self.check_and_notify( cr, uid, days=30, context=context)
        
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