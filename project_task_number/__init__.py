from . import models
from odoo import api, SUPERUSER_ID

def _initialize_task_number(cr, registry):
    env = api.Environment(cr, SUPERUSER_ID, {})
    env['project.task'].task_number_hook()