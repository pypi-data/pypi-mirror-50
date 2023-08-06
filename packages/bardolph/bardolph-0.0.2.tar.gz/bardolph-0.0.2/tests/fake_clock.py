from lib.i_lib import Clock
import lib.injection as injection

def configure():
    """ Bind empty instance to itself; complete no-op. """
    injection.bind(Clock).to(Clock)
