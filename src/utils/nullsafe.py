from functools import wraps
from typing import Union, Optional, TypeVar, Type, Sequence, Callable, Any

__T1 = TypeVar('__T1')
__T2 = TypeVar('__T2')


def ifnotnone(value: Optional[__T1], func: Callable[..., __T2]) -> Callable[..., Optional[__T2]]:
    """ Execute the given function if the given is not None

    Designed to be a replica ?. operator in Kotlin language. Also can be used as a decorator
    based on variable value may or may not execute

    Example:

    file?.open("tmp.txt") => ifnotnone(file, file.open)("tmp.txt")

    :param value: The given value to be tested
    :param func: The function that will be executed
    :return: The function if the value is not None or a function that returns None on call
    """

    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Optional[__T2]:
        if value is not None:
            return func(*args, **kwargs)
        return (lambda: None)()

    return wrapper


def ifnone(value: Optional[__T1], onelse: __T2) -> Union[__T1, __T2]:
    """ Checks if given value is None else return other value

    :param value: The given value that is be checked
    :param onelse: The alternative value
    :return: value if it is not None else onelse
    """
    if value is not None:
        return value
    return onelse


def notnone(value: Optional[__T1]) -> __T1:
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


def assertsequencetype(type_: Type[__T1], sequence: Sequence[__T2]) -> Sequence[__T1]:
    """ Assert data type for every element in a sequence

    :param type_: Given data type
    :param sequence: Given sequence of some data type
    :raises AssertionError: Raise if value is not of type type_
    :return: Sequence with values of given data type
    """
    assert isinstance(sequence, Sequence)
    return [asserttype(type_, item) for item in sequence]


def assertoptionaltype(type_: Type[__T1], value: __T2) -> Optional[__T1]:
    """ Assert the data type of given value (includes None as same data type)

    :param type_: Given data type
    :param value: Given value that is to be asserted
    :raises AssertionError: Raise if value is not of type type_
    :return: value which is of given type
    """
    if value is None:
        return
    return asserttype(type_, value)


def optional(value: __T1) -> Optional[__T1]:
    """Wraps the value in a Optional

    Intended to be used to fix errors reported by static type checkers
    where non-optional value can not be assigned to a optional data type

    :param value: The given value
    :returns: Same value with its data type wrapped in optional
    """
    return value
