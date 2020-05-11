from enum import Enum
from typing import Any
import builtins

Colors = Enum(
    "Colors",
    {
        "ERROR": "\033[0;31m",
        "WARNING": "\033[0;33m",
        "DEBUG": "\033[0;37m",
        "INFO": "\033[0;34m",
        "SUCCESS": "\033[0;32m",
        "DEFAULT": "\033[0m",
    },
)


def print(*objects: Any, sep: str = " ", end: str = "\n", style: str = None):
    builtins.print(*objects, sep=sep, end=end)


def info(*objects: Any, sep: str = " ", end: str = "\n") -> None:
    builtins.print(Colors.INFO.value, *objects, Colors.DEFAULT.value, sep=sep, end=end)


def debug(*objects: Any, sep: str = " ", end: str = "\n") -> None:
    builtins.print(Colors.DEBUG.value, *objects, Colors.DEFAULT.value, sep=sep, end=end)


def success(*objects: Any, sep: str = " ", end: str = "\n") -> None:
    builtins.print(Colors.SUCCESS.value, *objects, Colors.DEFAULT.value, sep=sep, end=end)


def warning(*objects: Any, sep: str = " ", end: str = "\n") -> None:
    builtins.print(Colors.WARNING.value, *objects, Colors.DEFAULT.value, sep=sep, end=end)


def error(*objects: Any, sep: str = " ", end: str = "\n") -> None:
    builtins.print(Colors.ERROR.value, *objects, Colors.DEFAULT.value, sep=sep, end=end)
