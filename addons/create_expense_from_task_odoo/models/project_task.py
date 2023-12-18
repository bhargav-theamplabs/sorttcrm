# -*- coding: utf-8 -*-
################################################################################
#
#    Cybrosys Technologies Pvt. Ltd.
#
#    Copyright (C) 2023-TODAY Cybrosys Technologies(<https://www.cybrosys.com>).
#    Author: Anfas Faisal K (odoo@cybrosys.info)
#
#    You can modify it under the terms of the GNU AFFERO
#    GENERAL PUBLIC LICENSE (AGPL v3), Version 3.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU AFFERO GENERAL PUBLIC LICENSE (AGPL v3) for more details.
#
#    You should have received a copy of the GNU AFFERO GENERAL PUBLIC LICENSE
#    (AGPL v3) along with this program.
#    If not, see <http://www.gnu.org/licenses/>.
#
################################################################################
from odoo import models, fields, api
from odoo.exceptions import ValidationError


class InheritProjectTask(models.Model):
    """
    InheritProjectTask model extends the project.task model in the Odoo
    framework. It adds two methods - create_task_expense() and smart_expense()
    - which are used as button actions to create expense records associated
    with a task and display existing expense records related to a task,
    respectively.
    """
    _inherit = 'project.task'

    start_date = fields.Date("Start Date") 

    @api.constrains('start_date', 'date_deadline')
    def _check_start_date_before_deadline(self):
        for record in self:
            if record.start_date and record.date_deadline and record.start_date >= record.date_deadline:
                raise ValidationError("Start Date must be before Deadline.")

    @api.onchange('stage_id')
    def on_change_is_closed(self):
        if self.is_closed:
            # Perform the action to archive the task
            self.write({'active': False})

    def action_create_task_expense(self):
        """Expense Button which will go to Expense Wizard Form where he add
        the total amount of expense and also pass the value through context"""
        return {
            'name': 'Create Expense Wizard',
            'type': 'ir.actions.act_window',
            'res_model': 'expense.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_task_id': self.id,
                'default_project_id': self.project_id.id,
                'default_name': self.name,
                'default_employee_name_id': [
                    (6, 0, self.user_ids.mapped('employee_ids').ids)]
            },
        }

    def smart_expense(self):
        """ Smart Button of Expense which will redirect to Current Expense
        Records"""
        expense_ids = self.env['hr.expense'].search([('task_id', '=', self.id)]).ids
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'hr.expense',
            'domain': [('id', 'in', expense_ids)],
            'view_mode': 'tree,form',
            'target': 'current',
        }
