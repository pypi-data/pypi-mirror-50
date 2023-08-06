import re
from functools import wraps

ANSI_ESCAPE_PROG = re.compile(r'\x1b(?:\[|\()([0-9,A-Z]{1,2}(;[0-9]{1,2})?(;[0-9]{3})?)?[m|K]?')


def ansi_clean(string):
    return ANSI_ESCAPE_PROG.sub('', string)


def identity(value):
    return value


def decorator_with_args(func):
    @wraps(func)
    def inner(*args, **kwargs):
        if len(args) == 1 and len(kwargs) == 0 and callable(args[0]):
            return func(args[0])
        else:
            return lambda f: func(f, *args, **kwargs)
    return inner
