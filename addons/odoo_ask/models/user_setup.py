from odoo import models, api
import logging

_logger = logging.getLogger(__name__)

class UserSetup(models.Model):
    _name = 'ask.user_setup'
    _description = 'Ask User Setup'

    @api.model
    def setup_nio_user(self):
        """Setup nio@sjfood.us user with Ask Management permissions"""
        try:
            # Find or create the user
            user = self.env['res.users'].search([('login', '=', 'nio@sjfood.us')], limit=1)
            if not user:
                # Create the user if it doesn't exist
                user = self.env['res.users'].create({
                    'name': 'Nio User',
                    'login': 'nio@sjfood.us',
                    'email': 'nio@sjfood.us',
                    'active': True,
                })
                _logger.info(f"Created user: {user.name} ({user.login})")
            else:
                _logger.info(f"Found existing user: {user.name} ({user.login})")
            
            # Add user to Ask Management groups
            ask_admin_group = self.env.ref('odoo_ask.group_ask_admin', raise_if_not_found=False)
            if ask_admin_group:
                # Use sudo() to write groups field, or use groups_id field
                user.sudo().write({'groups_id': [(4, ask_admin_group.id)]})
                _logger.info(f"Added {user.name} to Ask Management Administrator group")
            else:
                _logger.warning("Ask Management Administrator group not found")
                
        except Exception as e:
            _logger.error(f"Error setting up nio user: {e}")

    def _auto_setup_nio_user(self):
        """Automatically setup nio user when module is installed"""
        self.setup_nio_user()
