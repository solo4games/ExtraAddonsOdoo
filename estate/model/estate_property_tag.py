from odoo import models, fields

class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "This is free real estate tags"
    _order = "name"

    name = fields.Char(required=True)
    color = fields.Integer(default=3)

    _sql_constraints = [
        ('unique_property_tag', 'UNIQUE(name)', 'Must be Unique')
    ]