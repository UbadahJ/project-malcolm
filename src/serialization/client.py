import pickle
from dataclasses import dataclass
from typing import Tuple, Optional, MutableSequence, IO


@dataclass
class ClientInfo:
    checks: str
    data: MutableSequence[Tuple[Tuple[int, int], Optional[bytes]]]


def dump(instance: ClientInfo, file: IO[bytes]) -> None:
    pickle.dump(instance, file)


def load(file: IO[bytes]) -> ClientInfo:
    return pickle.load(file)
