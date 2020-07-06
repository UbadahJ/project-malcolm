import functools
from collections import Callable


def debug(func: Callable):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        print('{}() => args: {}, kwargs: {}'.format(func.__name__, args, kwargs))
        _tmp = func(*args, **kwargs)
        print('{}() => return: {}'.format(func.__name__, _tmp))
        return _tmp

    return wrapper
