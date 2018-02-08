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

from openerp import models, fields, api, _


class employee_mapping(models.Model):
    _name = 'employee.mapping'

    total_id = fields.Integer('Total ID', required=True, help="Employee ID in TOTAL")
    company_id = fields.Many2one('res.company', required=True)
    employee_id = fields.Many2one('hr.employee', required=True)
    _sql_constraints = [
        ('employee_mapping_unique', 'unique(total_id, company_id, employee_id)', 'Employee already exists in mapping!'),
        ]   

class expense_mapping (models.Model):
    _name = 'expense.mapping'
    
    total_id = fields.Integer('Total ID', required=True, help="Expense ID in TOTAL")
    product_id = fields.Many2one('product.product', required=True, help="CRM Product Related To Expense ID in TOTAL")
    _sql_constraints = [
        ('expense_mapping_unique', 'unique(total_id, product_id)', 'Expense already exists in mapping!'),
        ]   


class responsible_person_mapping (models.Model):
    _name = 'responsible.person.mapping'
    
    total_id = fields.Integer('TOTAL ID', required=True, help="Responsible person  ID  in TOTAL")
    company_id = fields.Many2one('res.company', required=True)
    _sql_constraints = [
        ('responsible_person_mapping_unique', 'unique(total_id, company_id)', 'Responsible person already exists in mapping!'),
        ]   


class transportation_mapping (models.Model):
    _name = 'transportation.mapping'
    
    total_id = fields.Integer('TOTAL ID', required=True, help="Transportation ID in TOTAL")
    transportation_id = fields.Many2one('travel.transportation', required=True, help='Transportation')
    _sql_constraints = [
        ('transportation_mapping_unique', 'unique(total_id, transportation_id)', 'Transportation already exists in mapping!'),
        ]   

class currency_mapping (models.Model):
    _name = 'currency.mapping'
    
    total_id = fields.Char('TOTAL ID', required=True, help="Currency ID in TOTAL")
    currency_name = fields.Char('Currency name', required=True, help='Currency name')
    description = fields.Char('Currency description', required=True, help='Currency Description')
    _sql_constraints = [
        ('currency_mapping_unique', 'unique(total_id, currency_name)', 'Currency already exists in mapping!'),
        ]   

