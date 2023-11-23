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

    @api.model
    def create(self, vals):
        project = super(Project, self).create(vals)
        if project.name:
            task_types = self.env['project.task.type'].search([('default_stage', '=', True)])
            for task_type in task_types:
                task_type.project_ids = [(4, project.id)]
        return project

class CRMLeadDocument(models.Model):
    _name = 'crm.lead.document'
    _description = 'CRM Lead Document'
    _inherits = {
        'ir.attachment': 'ir_attachment_id',
    }

    doc_name = fields.Char(string='Document Name', required=False)
    document = fields.Binary(string='Document', required=True)
    lead_id = fields.Many2one('crm.lead', string='Lead')
    ir_attachment_id = fields.Many2one('ir.attachment', string='Related attachment', required=True)
    active = fields.Boolean('Active', default=True)
    priority = fields.Selection([
        ('0', 'Normal'),
        ('1', 'Low'),
        ('2', 'High'),
        ('3', 'Very High')], string="Priority") # used to order


    def create(self, values):
        record = super(CRMLeadDocument, self).create(values)
        record.create_chatter_log('Document uploaded: %s' % record.name)
        return record

    def create_chatter_log(self, message):
        self.lead_id.message_post(body=message)

    def unlink(self):
        for record in self:
            record.create_chatter_log(f'Document removed: {record.name}')
        return super(CRMLeadDocument, self).unlink()



class Lead(models.Model):
    _inherit = "crm.lead"
  
    project_id = fields.Many2one('project.project', string="Project")
    construction_type_id = fields.Many2one('project.type.template', string='Construction Type', required="True")
    # Address fields
    site_street = fields.Char('Street', readonly=False, store=False)
    site_street2 = fields.Char('Street2', readonly=False, store=False)
    site_zip = fields.Char('Zip', change_default=True, readonly=False, store=False)
    site_city = fields.Char('City', readonly=False, store=False)
    site_state_id = fields.Many2one(
        "res.country.state", string='State',
         readonly=False, store=False,
        domain="[('country_id', '=?', country_id)]")
    site_country_id = fields.Many2one(
        'res.country', string='Country',
        readonly=False, store=False)

    lead_documents = fields.One2many('crm.lead.document', 'lead_id', string='Documents')
    estate = fields.Char(string='Estate')

    def create_project_on_won(self):
        if self.stage_id.is_won:
            project_vals = {
                'name': self.name,
                'partner_id': self.partner_id.id,
                'construction_type_id': self.construction_type_id.id
            }
            project = self.env['project.project'].create(project_vals)
            self.project_id = project.id

            task_obj = self.env['project.task']
            project_milestone_obj = self.env['project.milestone']

            milestone_records = self.env['project.milestone.stage'].search([('type_id', '=', self.construction_type_id.id)])
            for milestone in milestone_records:
                new_milestone = project_milestone_obj.create({'name': milestone.stage_id.name, 'project_id': project.id})
                for task in milestone.activity_line_ids:
                    task_obj.create({
                        'name': task.name,
                        'milestone_id': new_milestone.id,
                        'project_id': project.id,
                    })
            project.write({'task_create': True})

        return True

    def write(self, vals):
        res = super(Lead, self).write(vals)
        for rec in self:
            if not rec.project_id:
                rec.create_project_on_won()
        return res


class ProjectType(models.Model):
    _inherit = "project.task.type"

    default_stage = fields.Boolean(string="Default stage", default=False)
