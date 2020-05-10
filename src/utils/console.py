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

Colors = Enum(
    "Colors",
    {
        "ERROR":   "\033[0;31m",
        "WARNING": "\033[0;33m",
        "DEBUG":   "\033[0;37m",
        "INFO":    "\033[0;34m",
        "SUCCESS": "\033[0;32m",
        "DEFAULT": "\033[0m",
    },
)


def box_print(*objects: Any, chr: str = "*", sep: str = " ", file: TextIO = sys.stdout, flush: bool = False) -> None:
    size = len(sep.join([chr, *objects, chr]))
    print(chr * size)
    print(chr, *objects, chr, sep=sep, file=file, flush=flush)
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


def info(*objects: Any, sep: str = " ", end: str = "\n", file: TextIO = sys.stdout, flush: bool = False) -> None:
    if pretty_printing:
        print(
            Colors.INFO.value,
            *objects,
            Colors.DEFAULT.value,
            sep=sep,
            end=end,
            file=file,
            flush=flush
        )
    else:
        print(*objects, sep=sep, end=end, file=file, flush=flush)


def debug(*objects: Any, sep: str = " ", end: str = "\n", file: TextIO = sys.stdout, flush: bool = False) -> None:
    if enable_debugging:
        if pretty_printing:
            print(
                Colors.DEBUG,
                *objects,
                Colors.DEFAULT,
                sep=sep,
                end=end,
                file=file,
                flush=flush
            )
        else:
            print(*objects, sep=sep, end=end, file=file, flush=flush)


def success(*objects: Any, sep: str = " ", end: str = "\n", file: TextIO = sys.stdout, flush: bool = False) -> None:
    if pretty_printing:
        print(
            Colors.SUCCESS.value,
            *objects,
            Colors.DEFAULT.value,
            sep=sep,
            end=end,
            file=file,
            flush=flush
        )
    else:
        print(*objects, sep=sep, end=end, file=file, flush=flush)


def warning(*objects: Any, sep: str = " ", end: str = "\n", file: TextIO = sys.stdout, flush: bool = False) -> None:
    if pretty_printing:
        print(
            Colors.WARNING.value,
            *objects,
            Colors.DEFAULT.value,
            sep=sep,
            end=end,
            file=file,
            flush=flush
        )
    else:
        print(*objects, sep=sep, end=end, file=file, flush=flush)


def error(*objects: Any, sep: str = " ", end: str = "\n", file: TextIO = sys.stdout, flush: bool = False) -> None:
    if pretty_printing:
        print(
            Colors.ERROR.value,
            *objects,
            Colors.DEFAULT.value,
            sep=sep,
            end=end,
            file=file,
            flush=flush
        )
    else:
        print(*objects, sep=sep, end=end, file=file, flush=flush)
