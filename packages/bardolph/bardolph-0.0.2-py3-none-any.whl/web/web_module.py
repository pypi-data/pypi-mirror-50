import logging

from lib import settings
from lib import injection

import controller.config_values as config_values
from controller import light_module
from web.web_app import WebApp

debug = False

def configure():
    injection.configure()
    settings.using_base(config_values.functional).configure()
    
    global debug
    if debug:
        settings.specialize({
                            'use_fakes': True,
                            'log_level': logging.DEBUG
                            })
    light_module.configure()
    injection.bind_instance(WebApp()).to(WebApp)
