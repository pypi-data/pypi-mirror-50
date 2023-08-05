import logging

def _funcname(f):
    return "<Neon.Func: {}>".format(f.__name__)

def _logger(func):
    logger = logging.getLogger("NEON."+_funcname(func))
    logging.basicConfig(level=logging.DEBUG)
    return logger
