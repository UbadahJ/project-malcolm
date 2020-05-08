from enum import Enum
import sys

pretty_printing = False
enable_debugging = True

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
