from typing import Dict, Union

from utils.collections import first
from utils.nullsafe import notnone


def dump_hook(instance) -> Dict[str, Union[int, str, None]]:
    return {
        "checks":          notnone(first(instance.checks)),
        "unfinished_data": instance.data_unfinished
    }
