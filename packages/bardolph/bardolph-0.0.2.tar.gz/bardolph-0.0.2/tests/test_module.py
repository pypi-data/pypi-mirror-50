import lib.injection as injection
import lib.settings as settings
import tests.fake_clock as fake_clock
import tests.fake_light_set as fake_light_set

def configure():
    injection.configure()
    settings.configure()
    fake_clock.configure()
    fake_light_set.configure()
