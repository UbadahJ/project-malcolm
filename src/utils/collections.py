from typing import Sequence, TypeVar, Optional, List, Union, Sized, Any

from utils.nullsafe import asserttype

__T = TypeVar('__T')
__V = TypeVar('__V')


def first(data: Sequence[__T]) -> Optional[__T]:
    try:
        return data[0]
    except IndexError:
        return None


def last(data: Sequence[__T]) -> Optional[__T]:
    try:
        return data[-1]
    except IndexError:
        return None


def empty(data: Sequence[__T]) -> bool:
    if isinstance(data, Sized):
        return len(asserttype(Sized, data)) == 0
    try:
        for _ in data:
            return True
    except (TypeError, IndexError):
        pass
    return False


def contains(sequence: List[__T], item: __V, *, recursive=False) -> bool:
    if recursive:
        return _contains_recursive(sequence, item)
    for i in sequence:
        if i == item:
            return True
    return False


def _contains_recursive(sequence: List[Any], item: __V) -> bool:
    _contains: bool = False
    for i in sequence:
        if isinstance(i, List):
            _contains = _contains_recursive(i, item)
        else:
            _contains = i == item
        if _contains:
            break
    return _contains


def flatten(data: Sequence[Union[Sequence[__T], __T]]) -> Sequence[__T]:
    _list: List[__T] = list()
    for item in data:
        if isinstance(item, Sequence):
            _list.extend(item)
        else:
            _list.append(item)
    return _list
