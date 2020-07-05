from typing import Union, Optional, TypeVar

__T1 = TypeVar('__T1')
__T2 = TypeVar('__T2')


def ifnoneorelse(value: Optional[__T1], onelse: __T2) -> Union[__T1, __T2]:
    if value is not None:
        return value
    return onelse


def assertnotnone(value: Optional[__T1]) -> __T1:
    assert value is not None
    return value

