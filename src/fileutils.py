from typing import List
import os

def spilt(file: str, parts: int) -> List[int]:
    total = get_size(file)
    return [i for i in range(0, total - 1, round(total / parts))]

def get_size(file: str) -> int: 
    return os.path.getsize(file)