from odoo import models
from odoo.exceptions import UserError

class EstateProperty(models.Model):
    _inherit = "estate.property"

    def action_do_sold(self):
        for record in self:
            record.env["account.move"].create(
                {
                    "partner_id": record.buyer_id,
                    "move_type": "out_invoice",
                    "invoice_line_ids": [
                        (
                            0,
                            0,
                            {
                                "name": record.name,
                                "quantity": record.living_area+100,
                                "price_unit": record.expected_price*0.06,
                            },
                        )
                    ],
                }
            )
        return super().action_do_sold()