import base64
from typing import Dict, Union

from utils.collections import first


def dump_hook(instance) -> Dict[str, Union[int, str, None]]:
    _data = list()
    for (start, end), seg in instance.data_unfinished:
        if seg is not None:
            seg = base64.b64encode(seg).decode('utf-8')
        _data.append(((start, end), seg))
    return {
        "checks":          first(instance.checks),
        "unfinished_data": _data
    }
