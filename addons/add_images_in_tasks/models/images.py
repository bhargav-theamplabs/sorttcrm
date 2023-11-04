from odoo import models, fields


class Task(models.Model):
    _inherit = 'project.task'

    ref = fields.Char(string="Ref:")
    images = fields.One2many('task.image', 'task_id', string="Images")


class TaskImage(models.Model):
    _name = 'task.image'
    _description = 'Task Image'

    name = fields.Char(string="Description")
    image = fields.Binary(string="Image")
    image_name = fields.Char(string="Image Name")
    task_id = fields.Many2one('project.task', string="Task")
