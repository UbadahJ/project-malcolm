import os
from hashlib import sha1
from os.path import basename
from typing import List


def spilt(file: str, parts: int) -> List[int]:
    total = get_size(file)
    return [i for i in range(0, total - 1, round(total / parts))]


def get_size(file: str) -> int:
    return os.path.getsize(file)


def gen_checksum(file: str) -> str:
    with open(file, "rb") as f:
        return (
            sha1(basename(file).encode("utf-8")).hexdigest()
            + sha1(f.read()).hexdigest()
        )
