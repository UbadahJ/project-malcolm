import os
from hashlib import sha1
from os.path import basename
from typing import List, Tuple


def spilt(file_size: int = None, *, file: str = None, parts: int) -> List[Tuple[int, int]]:
    if file_size is None:
        file_size = get_size(file)
    offsets = [i for i in range(0, file_size - 1, file_size // parts)]
    offsets[-1] = file_size
    return [(f, s) for f, s in zip(offsets, offsets[1:])]


def get_size(file: str) -> int:
    return os.path.getsize(file)


def gen_checksum(file: str) -> str:
    with open(file, "rb") as f:
        return (
                sha1(basename(file).encode("utf-8")).hexdigest()
                + sha1(f.read()).hexdigest()
        )


def get_file_name(file: str) -> str:
    return os.path.basename(file)
