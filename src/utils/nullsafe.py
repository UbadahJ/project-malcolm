from typing import Union, Optional, TypeVar

__T1 = TypeVar('__T1')
__T2 = TypeVar('__T2')


class NoneException(Exception):
    pass


def ifnoneorelse(value: Optional[__T1], onelse: __T2) -> Union[__T1, __T2]:
    if value is not None:
        return value
    return onelse


def ifnoneelsethrow(value: Optional[__T1], exception: Exception) -> __T1:
    if value is not None:
        return value
    raise exception
