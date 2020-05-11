from typing import Any

from rich.console import Console
from rich.theme import Theme
from rich.traceback import install

install()

_theme = Theme(
    {"error": "red", "warning": "yellow", "info": "blue", "success": "green"}
)

_console = Console(theme=_theme)


def print(*objects: Any, sep: str = " ", end: str = "\n", style: str = None):
    _console.print(*objects, sep=sep, end=end, style=style)


def info(*objects: Any, sep: str = " ", end: str = "\n") -> None:
    _console.print(*objects, sep=sep, end=end, style="info")


def debug(*objects: Any, sep: str = " ", end: str = "\n") -> None:
    _console.log(*objects, sep=sep, end=end)


def success(*objects: Any, sep: str = " ", end: str = "\n") -> None:
    _console.print(*objects, sep=sep, end=end, style="success")


def warning(*objects: Any, sep: str = " ", end: str = "\n") -> None:
    _console.print(*objects, sep=sep, end=end, style="warning")


def error(*objects: Any, sep: str = " ", end: str = "\n") -> None:
    _console.print(*objects, sep=sep, end=end, style="error")
