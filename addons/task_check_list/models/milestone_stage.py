from odoo import models, fields, api, _

class MilestoneLine(models.Model):
    _name = 'project.milestone.line'

    template_id = fields.Many2one(
    'project.milestone.stage', 'Template', required=False)

    sequence = fields.Integer(string='Sort')
    name = fields.Char(string='Name')
    serial_no = fields.Integer(string='S.No.')  


class TaskChecklist(models.Model):
    _name = 'project.milestone.stage'
    _description = 'Checklist for the task'
    _rec_name = 'stage_id'

    stage_id = fields.Many2one(
        'project.milestone.template', 'Milestone', required=True)
    type_id = fields.Many2one(
        'project.type.template', 'Construction Type', required=True)


    activity_line_ids = fields.One2many(
        'project.milestone.line','template_id',copy=False)

    _sql_constraints = [
        ('unique_stage_type_combination', 'UNIQUE(stage_id, type_id)', 'Milestone and Type combination must be unique.')
    ]

    @api.onchange('stage_id', 'type_id')
    def _onchange_stage_type(self):
        if self.stage_id and self.type_id:
            task_records = self.env['task.template'].search([('project_type_ids','=', self.type_id.id),('project_stage_ids','=', self.stage_id.id)])
            activity_lines = [(5, 0, 0)]
            for task in task_records:
                activity_lines.append((0, 0, {'name': task.name, 'serial_no': task.serial_no}))
            self.activity_line_ids = activity_lines