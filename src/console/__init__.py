import platform
import subprocess
import sys
from typing import Any, Callable, Tuple, Sequence

import console._fallback as c

pretty_printing = False
enable_debugging = True

_var_getch = None

_print = c.print
_info = c.info
_debug = c.debug
_success = c.success
_warning = c.warning
_error = c.error


def box_print(*objects: Any, chr: str = "*", sep: str = " ") -> None:
    size = len(sep.join([chr, *objects, chr]))
    print(chr * size)
    print(chr, *objects, chr, sep=sep)
    print(chr * size)


def clear() -> None:
    subprocess.Popen("cls" if platform.system() == "Windows" else "clear", shell=True).communicate()
    sys.stdout.flush()


UNITS_MAPPING: Sequence[Tuple[int, str]] = [
    (1 << 50, ' PB'),
    (1 << 40, ' TB'),
    (1 << 30, ' GB'),
    (1 << 20, ' MB'),
    (1 << 10, ' KB'),
    (1, ' B'),
]


def pretty_size(_bytes: int, units: Sequence[Tuple[int, str]] = UNITS_MAPPING) -> str:
    amount: str = '0B'
    for _factor, _suffix in units:
        if not _bytes >= _factor:
            continue
        amount = str(round(_bytes / _factor, 2)) + _suffix
    return amount


def _find_getch() -> Callable:
    try:
        import termios
    except ImportError:
        # Non-POSIX. Return msvcrt's (Windows') getch.
        import msvcrt

        return msvcrt.getch  # ignore

    # POSIX system. Create and return a getch that manipulates the tty.
    import sys, tty

    def _getch():
        fd = sys.stdin.fileno()
        try:
            old_settings = termios.tcgetattr(fd)
            tty.setraw(fd)
            ch = sys.stdin.read(1)
        except Exception:
            warning("Failed to get a getch() configuration, falling back to input()")
            return input()
        else:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch

    return _getch


def getch() -> str:
    global _var_getch
    if _var_getch is None:
        _var_getch = _find_getch()
    return _var_getch()


def show_error_msg(exception: Exception):
    c.print(
        'Failed to load rich library for formatting, falling back to built-in console formatting')
    c.print('Install pip install -user rich')
    c.print('To get better terminal support')
    c.error(exception)
    c.print()
    c.print('Press any key to continue')
    getch()


def print(*objects: Any, sep: str = " ", end: str = "\n", style: str = None):
    _print(*objects, sep=sep, end=end, style=style)


def info(*objects: Any, sep: str = " ", end: str = "\n") -> None:
    _info(*objects, sep=sep, end=end)


def debug(*objects: Any, sep: str = " ", end: str = "\n") -> None:
    _debug(*objects, sep=sep, end=end)


def success(*objects: Any, sep: str = " ", end: str = "\n") -> None:
    _success(*objects, sep=sep, end=end)


def warning(*objects: Any, sep: str = " ", end: str = "\n") -> None:
    _warning(*objects, sep=sep, end=end)


def error(*objects: Any, sep: str = " ", end: str = "\n") -> None:
    _error(*objects, sep=sep, end=end)
