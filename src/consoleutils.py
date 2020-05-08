import platform
import subprocess
import sys
from enum import Enum

pretty_printing = False
enable_debugging = True

_var_getch = None

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


def box_print(*objects, chr="*", sep=" ", file=sys.stdout, flush=False):
    size = len(sep.join([chr, *objects, chr]))
    print(chr * size)
    print(chr, *objects, chr, sep=sep, file=file, flush=flush)
    print(chr * size)


def clear():
    if platform.system() == "Windows":
        subprocess.Popen("cls", shell=True).communicate()
    else:
        print("\033c", end="")


def _find_getch():
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
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch

    return _getch


def getch():
    global _var_getch
    if _var_getch is None:
        _var_getch = _find_getch()
    _var_getch()

def info(*objects, sep=" ", end="\n", file=sys.stdout, flush=False):
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


def debug(*objects, sep=" ", end="\n", file=sys.stdout, flush=False):
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


def success(*objects, sep=" ", end="\n", file=sys.stdout, flush=False):
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


def warning(*objects, sep=" ", end="\n", file=sys.stdout, flush=False):
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


def error(*objects, sep=" ", end="\n", file=sys.stdout, flush=False):
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
