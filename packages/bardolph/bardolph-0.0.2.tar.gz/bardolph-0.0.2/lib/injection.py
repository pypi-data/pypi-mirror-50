class Injection:
    providers = {}


class Binder:
    def __init__(self, implementation):
        self.implementation = implementation
        
    def to(self, interface):
        Injection.providers[interface] = self.implementation
        

class ObjectBinder:
    def __init__(self, implementor):
        self.implementor = implementor
        
    def to(self, interface):
        Injection.providers[interface] = lambda: self.implementor
        

def inject(*interfaces):
    def fn_wrapper(fn):
        def param_wrapper(*args):
            injected_args = []
            for interface in interfaces:
                if interface in Injection.providers:
                    obj = Injection.providers[interface]()
                else:
                    obj = interface()
                injected_args.append(obj)
            args = args + tuple(injected_args)
            return fn(*args)
        return param_wrapper
    return fn_wrapper


def provide(interface):
    creator = Injection.providers.get(interface, interface)
    return creator()

def configure(): Injection.providers = {}

def bind(implementation): return Binder(implementation)

def bind_instance(implementor): return ObjectBinder(implementor)
