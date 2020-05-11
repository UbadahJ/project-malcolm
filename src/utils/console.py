import platform
import subprocess
import sys
from enum import Enum
from typing import Any
from typing import Callable
from typing import TextIO

pretty_printing = False
enable_debugging = True

_var_getch = None

try:
    import rich
except ImportError:
    import utils.fallbackconsole as c
else:
    import utils.richconsole as c
finally:
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
    if platform.system() == "Windows":
        subprocess.Popen("cls", shell=True).communicate()
    else:
        print("\033c", end="")


def _find_getch() -> Callable:
    try:
        import termios
    except ImportError:
        # Non-POSIX. Return msvcrt's (Windows') getch.
        import msvcrt

        return msvcrt.getch

    # POSIX system. Create and return a getch that manipulates the tty.
    import sys, tty

    def _getch():
        fd = sys.stdin.fileno()
        try:
            old_settings = termios.tcgetattr(fd)
            tty.setraw(fd)
            ch = sys.stdin.read(1)
        except:
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
