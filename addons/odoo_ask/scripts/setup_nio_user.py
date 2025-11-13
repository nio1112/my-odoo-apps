#!/usr/bin/env python3
"""
Script to setup nio@sjfood.us user with Ask Management permissions
"""
import sys
import os

# Add Odoo to path
sys.path.insert(0, '/usr/lib/python3/dist-packages')

import odoo
from odoo import api, SUPERUSER_ID

def setup_nio_user():
    """Setup nio@sjfood.us user with Ask Management permissions"""
    
    # Initialize Odoo
    odoo.cli.server.main()
    
    # Get database connection
    db_name = 'odoo'
    registry = odoo.registry(db_name)
    
    with registry.cursor() as cr:
        env = api.Environment(cr, SUPERUSER_ID, {})
        
        # Find or create the user
        user = env['res.users'].search([('login', '=', 'nio@sjfood.us')], limit=1)
        if not user:
            # Create the user if it doesn't exist
            user = env['res.users'].create({
                'name': 'Nio User',
                'login': 'nio@sjfood.us',
                'email': 'nio@sjfood.us',
                'active': True,
            })
            print(f"Created user: {user.name} ({user.login})")
        else:
            print(f"Found existing user: {user.name} ({user.login})")
        
        # Set password
        user.password = 'nio@sjfood.us'
        print("Password set to: nio@sjfood.us")
        
        # Add user to Ask Management groups
        try:
            ask_admin_group = env.ref('odoo_ask.group_ask_admin', raise_if_not_found=False)
            if ask_admin_group:
                # Use groups_id field instead of groups
                user.write({'groups_id': [(4, ask_admin_group.id)]})
                print(f"Added {user.name} to Ask Management Administrator group")
            else:
                print("Ask Management Administrator group not found")
        except Exception as e:
            print(f"Error adding user to group: {e}")
        
        cr.commit()
        print("User setup completed successfully!")

if __name__ == '__main__':
    setup_nio_user()
