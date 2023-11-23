# Copyright 2016-2017 Tecnativa - Pedro M. Baeza
# Copyright 2017 Tecnativa - Carlos Dauden
# Copyright 2021 Open Source Integrators - Daniel Reis
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class ProjectTask(models.Model):
    _inherit = "project.task"

    date_start = fields.Datetime("Start Date")

    def update_date_end(self, stage_id):
        res = super().update_date_end(stage_id)
        res.pop("date_end", None)
        return res

class ProjectProject(models.Model):
    _inherit = "project.project"


    construction_type_id = fields.Many2one(
        'project.type.template', 'Construction Type', required=False)
    task_create = fields.Boolean(string="Task Create")

    def action_auto_create(self):
        task_obj = self.env['project.task']
        for project in self:
            task_records = self.env['project.milestone.stage'].search([('type_id','=', project.construction_type_id.id)])
            for milestone in task_records:
                for task in milestone.activity_line_ids:
                    task_obj.create({
                        'name': task.name or "Hello",
                        'milestone_id': milestone.stage_id.id,
                        'project_id': project.id,
                        })
            project.write({'task_create': True})
            return True
