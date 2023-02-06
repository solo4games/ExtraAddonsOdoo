from odoo import models, fields, api
from dateutil.relativedelta import relativedelta
from datetime import timedelta
from odoo.exceptions import UserError

class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "This is free real estate types"
    _order = "price desc"

    price = fields.Float()
    status = fields.Selection(selection = [('accepted', 'Accepted'), ('refused', 'Refused')], copy=False)
    partner_id = fields.Many2one('res.partner', string='Partner', index=True, tracking=True, required=True)
    property_id = fields.Many2one('estate.property', required=True)
    validity = fields.Integer(default=7)
    property_type_id = fields.Many2one(related="property_id.property_type_id", store=True)

    date_deadline = fields.Date(compute="_compute_date_deadline", inverse="_inverse_date_deadline")
    @api.depends("validity", "property_id.create_date")
    def _compute_date_deadline(self):
        for record in self:
            record.date_deadline = record.property_id.date_availability + relativedelta(days=record.validity)

    @api.model
    def create(self, vals_list):
        if (self.price < self.env['estate.property'].browse(vals_list['partner_id']).best_price):
            raise UserError('Price must be more higher')
        return super().create(vals_list)

    def _inverse_date_deadline(self):
        for record in self:
            record.validity = (record.date_deadline - record.property_id.date_availability) / timedelta(days=1)
            record.property_id.date_availability = record.date_deadline - relativedelta(days=record.validity)

    def action_accept(self):
        for record in self:
            if (record.status == 'accepted'):
                raise UserError('It is already accepted, try something another')
            record.status = 'accepted'
            lowest = record.property_id.expected_price * 0.9
            if (lowest > record.price):
                raise UserError('Offer must be higher than 90%% of expected price')
            record.property_id.selling_price = record.price
            record.property_id.state = 'offer accepted'
            record.property_id.buyer_id = record.partner_id
        return True

    def action_refuse(self):
        for record in self:
            record.status = 'refused'
        return True

    
    _sql_constraints = [
        ('check_offer_price', 'CHECK(price > 0)', 'must be strictly positive')
    ]
    

