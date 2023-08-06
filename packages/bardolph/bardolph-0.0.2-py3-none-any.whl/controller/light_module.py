import lib.clock as clock
import lib.log_config as log_config
from lib.i_lib import Settings
from lib.injection import provide

def configure():
    log_config.configure()
    clock.configure()

    settings = provide(Settings)
    if settings.get_value('use_fakes'):
        import tests.fake_light_set as fake_light_set
        fake_light_set.configure()
    else:
        import controller.light_set
        controller.light_set.configure()
