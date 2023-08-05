import functools
import inspect

def _normalize_values(func, **norms):
    binder = inspect.signature(func).bind
    @functools.wraps(func)
    def inner_wrapper(*args, **kwargs):
        args = binder(*args, **kwargs)
        args.apply_defaults()
        arguments = args.arguments
        for v, n in norms.items():
            if v in arguments:
                arguments[v] = n(arguments[v])
        return func(*args.args, **args.kwargs)
    return inner_wrapper

def normalize_values(**norms):
    return lambda f: _normalize_values(f, **norms)

def auto_assign(*literal):
    def _assign(func):
        binder = inspect.signature(func).bind
        assignable = literal
        @functools.wraps(func)
        def inner_wrapper(self, *args, **kwargs):
            args = binder(self, *args, **kwargs)
            args.apply_defaults()
            arguments = args.arguments
            for v in assignable:
                if v in arguments and v != 'self':
                    setattr(self, v, arguments[v])
            return func(*args.args, **args.kwargs)
        return inner_wrapper
    return _assign

"""
from neon import normalize
class TestClass2:
    @normalize.normalize_values(c=lambda x: x+1)
    @normalize.assign('c', 'b', 'a')
    def __init__(self, a, b, c):
        print("a: {}, b: {}, c: {}".format(a,b,c))
"""
