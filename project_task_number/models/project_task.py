from odoo import models, fields, api
from odoo.osv import expression

class ProjectTask(models.Model):
    _inherit = "project.task"
    _description = "Project task number with sequence"

    task_number = fields.Integer(readonly=True, default=-1)
    @api.model
    def create(self, vals_list):
        vals_list['task_number'] = self.env['ir.sequence'].next_by_code('project.task.number')
        return super(ProjectTask, self).create(vals_list)

    def name_get(self):
        return [(record.id, "[%s]%s - %s" % (record.task_number, record.name, record.project_id.name)) for record in self]

    @api.model
    def _name_search(self, name='', args=None, operator='ilike', limit=100):
        if args is None:
            args = []
        domain = expression.AND(
            [
                args,
                ['|', ('name', operator, name), ('task_number', operator, name)],
            ]
        )
        return super(ProjectTask, self).search(domain, limit=limit).name_get()

    def task_number_hook(self):
        for record in self.search([], order='id'):
            record.task_number = self.env['ir.sequence'].next_by_code('project.task.number')
