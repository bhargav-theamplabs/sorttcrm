from odoo import models, fields, api

class TaskChecklist(models.Model):
    _name = 'task.template'
    _description = 'Tasks template'
    _order ="sequence, id"


    sequence = fields.Integer(string='Sort', required=True, default=10)
    name = fields.Char(string='Name', required=True)
    serial_no = fields.Integer(string='S.No.', required=True)
    project_type_ids = fields.Many2many(
        'project.type.template', string="Construction Type", required=True)
    project_stage_ids = fields.Many2many(
        'project.milestone.template', string="Milestones", required=True)
    # template_id = fields.Many2one(
    # 'project.milestone.stage', 'Template', required=False)

class ProjectTemplateLines(models.Model):
    _name="project.type.template"
    _description = "Construction Type"

    name = fields.Char(string='Name', required=True)


class ProjectStages(models.Model):
    _name="project.milestone.template"

    name = fields.Char(string='Name', required=True)

    # def name_get(self):
    #     result = []
    #     for record in self:
    #         result.append((record.id, record.project_stage))
    #     return result



    # @api.onchange('construction_type')
    # def onchange_construction_type(self):
    #     print('--------------------_onchange-------------------')
    #     if self.construction_type == 'Single Storey':
    #         single_story_stages = self.env['construction.stage.first.template'].search([])
    #         self.selected_stage_ids = [(6, 0, single_story_stages.ids)]
    #     else:
    #         self.selected_stage_ids = [(5, 0, 0)]