from typing import Callable, Any, Type
from functools import wraps


def retry(*exceptions: Type[Exception]) -> Callable:
    """ Calls itself again and again if the given exception occurs

    :param exceptions: Given exceptions
    :return: Wrapped function
    """
    def _retry(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            def _call():
                return True, func(*args, **kwargs)

            check = False
            res = None
            while not check:
                try:
                    check, res = _call()
                except exceptions:
                    pass
            return res

        return wrapper

    return _retry
