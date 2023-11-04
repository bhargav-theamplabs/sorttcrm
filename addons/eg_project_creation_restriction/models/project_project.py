from odoo import models, fields, api, _
from odoo.exceptions import UserError


class Project(models.Model):
    _inherit = "project.project"

    @api.model
    def create(self, vals):
        if self.env.user.has_group('eg_project_creation_restriction.project_creation_restriction'):
            raise UserError(_("You don't have access to create Project."))
        else:
            return super(Project, self).create(vals)

class Lead(models.Model):
    _inherit = "crm.lead"
  
    project_id = fields.Many2one('project.project', string="Project")

    @api.onchange('stage_id')
    def create_project_on_won(self):
        if self.stage_id.name == 'Won':
            project_vals = {
                'name': self.name,
                'partner_id': self.partner_id.id,
            }
            project = self.env['project.project'].create(project_vals)
