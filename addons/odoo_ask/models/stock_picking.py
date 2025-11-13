from odoo import models, fields, api
from odoo.exceptions import ValidationError

class StockPicking(models.Model):
    _inherit = 'stock.picking'

    def button_validate(self):
        """
        Override to check for ask reservations before validating.
        This is the 'conservative' approach.
        """
        for picking in self:
            if picking.picking_type_code == 'outgoing':
                for move in picking.move_lines:
                    # Find reservations for the product in this move
                    reservations = self.env['ask.reservation'].search([
                        ('product_id', '=', move.product_id.id),
                        ('status', '=', 'reserved')
                    ])
                    if reservations:
                        # Check if the current user is allowed to release the reservation
                        allowed_sales_users = reservations.mapped('reserved_to_sales_id')
                        if self.env.user not in allowed_sales_users:
                            # A more granular check could be to see if the move's quantity
                            # is covered by a non-reserved portion of stock.
                            # For MVP, we do a simple lock.
                            raise ValidationError(
                                f"Product {move.product_id.display_name} is reserved. "
                                f"The delivery can only be validated by the designated salesperson(s) or an administrator. "
                                f"Please contact {', '.join(allowed_sales_users.mapped('name'))}."
                            )
        return super(StockPicking, self).button_validate()