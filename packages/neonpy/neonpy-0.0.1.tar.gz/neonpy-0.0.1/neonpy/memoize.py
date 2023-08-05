import collections
from collections import defaultdict as ddict
from .util import _logger
import inspect
import functools

MEMO = ddict(dict)


def memoize(func):
    """Warning: Use the memoize function at your own risk.
    if the arguments to func can be changed by reference, you might memoize things that you shouldn't
    """
    _logger(func)
    binder = inspect.signature(func).bind
    logger = _logger(func)
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        sig = binder(*args, **kwargs)
        sig.apply_defaults()
        sig = tuple(sig.arguments.items())
        if not all([isinstance(x, collections.Hashable) for w,x in sig]):
            logger.debug("skipping memoization: not all parameters are hashable")
            return func(*args, **kwargs)
        if sig not in MEMO[func]:
            logger.debug("memoizing " + str(func) + str(sig))
            MEMO[func][sig] = func(*args, **kwargs)
        else:
            logger.debug("retrieving " + str(func) + str(sig))
        return MEMO[func][sig]
    return wrapper

def clear_memos(f):
    if f in MEMO:
        del MEMO[f]
