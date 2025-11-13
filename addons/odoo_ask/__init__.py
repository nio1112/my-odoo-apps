from . import models
from . import wizard

def post_init_hook(env):
    """Post-install hook to setup nio user"""
    user_setup = env['ask.user_setup']
    user_setup.setup_nio_user()