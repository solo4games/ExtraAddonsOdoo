from odoo import models, fields, api

class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "This is free real estate types"
    _order = "name"

    name = fields.Char(required=True)
    property_ids = fields.One2many('estate.property', 'property_type_id')
    sequence = fields.Integer('Sequence', default=1, help="Used to order types")
    offer_ids = fields.One2many('estate.property.offer', 'property_id')
    bullshit = fields.Integer(default=1)

    offer_count = fields.Integer(compute="_compute_number_offers")
    @api.depends("offer_ids")
    def _compute_number_offers(self):
        n = 0
        for record in self:
            for line in record.property_ids:
                for sub_line in line.offer_ids:
                    n += 1
            record.offer_count = n

    _sql_constraints = [
        ('unique_property_type', 'UNIQUE(name)', 'Must be Unique')
    ]