from odoo import models, fields, api
from dateutil.relativedelta import relativedelta
from odoo.exceptions import UserError
from odoo.tools.float_utils import *

class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "This is free real estate"
    _order = "id desc"

    name = fields.Char(required=True)
    tag_ids = fields.Many2many("estate.property.tag")
    property_type_id = fields.Many2one("estate.property.type")
    user_id = fields.Many2one('res.users', string='Salesperson', index=True, tracking=True, default=lambda self: self.env.user)
    buyer_id = fields.Many2one('res.partner', string='Buyer', index=True, tracking=True, copy=False)
    offer_ids = fields.One2many('estate.property.offer', 'property_id')
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(copy=False, default=lambda self:fields.Datetime.today() + relativedelta(month=3))
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(
    selection = [('north', 'North'), ('south', 'South'), ('east', 'East'), ('west', 'West')])
    active = fields.Boolean(default=True)
    state = fields.Selection(
        selection=[('new', 'New'), ('offer received', 'Offer received'), ('offer accepted', 'Offer accepted'), ('sold', 'Sold'), ('canceled', 'Canceled')],
        required=True, copy=False, default='new'
    )

    total_area = fields.Float(compute="_compute_total_area")
    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.garden_area + record.living_area

    best_price = fields.Float(compute="_compute_best_price")
    @api.depends("offer_ids.price")
    def _compute_best_price(self):
        for record in self:
            record.best_price = max(record.offer_ids.mapped('price'), default=0)

    @api.onchange("garden")
    def _onchange_garden(self):
        if (self.garden == True):
            self.garden_area = 10
            self.garden_orientation = 'north'
        else:
            self.garden_area = 0
            self.garden_orientation = ''

    @api.model
    def unlink(self):
        if (self.state == 'new') or (self.state == 'canceled'):
            raise UserError('Can not be deleted')
        return super().unlink()

    @api.model
    def create(self, vals_list):
        vals_list['state'] = 'offer received'
        return super().create(vals_list)

    def action_do_sold(self):
        for record in self:
            if (record.state == 'canceled'):
                raise UserError('It is already canceled, try something another')
            record.state = 'sold'
        return True

    def action_do_cancel(self):
        for record in self:
            if (record.state == 'sold'):
                raise UserError('It is already sold, try something another')
            record.state = 'canceled'
        return True
    
    _sql_constraints = [
        (
            'check_expected_price',
            'CHECK(expected_price > 0)',
            'must be strictly positive'
        ),
        (
            'check_selling_price',
            'CHECK(selling_price >= 0)',
            'must be positive'
        )
    ]

    

    