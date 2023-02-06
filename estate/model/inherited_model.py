from odoo import models, fields

class InheritedModel(models.Model):
    _inherit = "res.users"

    property_ids = fields.One2many('estate.property', 'user_id', domain="['|', ('state', '=', ('new', 'New')), ('state', '=', ('offer received', 'Offer received'))]")