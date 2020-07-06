from typing import Union, Optional, TypeVar, Type

__T1 = TypeVar('__T1')
__T2 = TypeVar('__T2')


def ifnoneorelse(value: Optional[__T1], onelse: __T2) -> Union[__T1, __T2]:
    """ Checks if given value is None else return other value

    :param value: The given value that is be checked
    :param onelse: The alternative value
    :return: value if it is not None else onelse
    """
    if value is not None:
        return value
    return onelse


def assertnotnone(value: Optional[__T1]) -> __T1:
    """ Assert if the given value is not None

    :param value: the value to be asserted
    :raises AssertionError: Raise if value is not of type type_
    :return: the value which is no longer Optional
    """
    assert value is not None
    return value


def asserttype(type_: Type[__T1], value: __T2) -> __T1:
    """ Assert the data type of given value

    :param type_: Given data type
    :param value: Given value that is to be asserted
    :raises AssertionError: Raise if value is not of type type_
    :return: value which is of given type
    """
    assert isinstance(value, type_)
    return value


def optional(value: __T1) -> Optional[__T1]:
    """Wraps the value in a Optional

    Intended to be used to fix errors reported by static type checkers
    where non-optional value can not be assigned to a optional data type

    :param value: The given value
    :returns: Same value with its data type wrapped in optional
    """
    return value
