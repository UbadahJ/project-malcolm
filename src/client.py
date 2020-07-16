#! /bin/python3

import argparse
import pathlib

from utils import network
import console as con
from console import print
from virclient import Client


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Launches a client that can connect to multiple servers that includes error handling and file "
        "verification"
    )
    parser.add_argument(
        "-i",
        "--interval",
        help="Time interval in seconds between server status reporting in seconds",
        required=True,
        type=int,
        dest="interval",
    )
    parser.add_argument(
        "-o",
        "--output",
        help="Path to the output directory (either absolute or relative)",
        required=True,
        type=str,
        dest="output",
    )
    parser.add_argument(
        "-a",
        "--address",
        help="The ip address of the server",
        required=True,
        type=str,
        dest="address",
    )
    parser.add_argument(
        "-p",
        "--port",
        nargs="*",
        help="List of ports that must be equal to number of virtual servers",
        required=True,
        type=int,
        dest="port",
    )
    parser.add_argument(
        "-r",
        "--resume",
        help="Flag that tells the client whether to resume the existing download in progress",
        action="store_true",
        default=False,
        dest="resume",
    )
    parser.add_argument(
        "-c",
        "--color-printing",
        help="Enables color printing in the console",
        action="store_true",
        default=False,
        dest="colors",
    )
    return parser.parse_args()


def verify(args: argparse.Namespace):
    con.pretty_printing = args.colors
    try:
        print("Validating IP Address ... ", end="")
        ip = args.address.split(".")
        # Check if IP has 4 decimal point
        assert len(ip) == 4
        # Check if any of them is empty
        for ad in ip:
            assert len(ad) != 0
        assert network.ping(args.address)
        con.success("OK")
        # Verify if the path given is valid directory
        print("Validating directory ... ", end="")
        assert pathlib.Path(args.output).is_dir()
        con.success("OK")
        # Check if resume flag is enabled
        if args.resume:
            # Check if resume.json exists
            print("Validating resume data ... ", end="")
            assert pathlib.Path('resume.pyb').exists()
            con.success("OK")
        return args
    except AssertionError:
        con.error("FAILED")
        quit(1)


if __name__ == "__main__":
    args = verify(parse_args())
    Client(
        address=args.address, output=args.output, ports=args.port, resume=args.resume
    )
