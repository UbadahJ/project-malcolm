import functools
import logging
from collections import Callable

logging.basicConfig(level=logging.DEBUG)


def truncate(string: str) -> str:
    return (string[:120] + '...') if len(string) > 123 else string


def debug(func: Callable):
    log = logging.getLogger(func.__name__)

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        p_args = [truncate(arg.__repr__()) for arg in args]
        p_kwargs = {key: truncate(value.__repr__()) for key, value in kwargs.items()}
        log.debug(f'args: {p_args}, kwargs: {p_kwargs}')
        _tmp = func(*args, **kwargs)
        log.debug(f'return: {truncate(_tmp.__repr__())}')
        return _tmp

    return wrapper
