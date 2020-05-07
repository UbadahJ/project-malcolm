#! /bin/python3

# TODO: Replace asserts with Exceptions

import pathlib
import argparse
import netutils

def parse_args():
    parser = argparse.ArgumentParser(
        description="Launches multiple virtual servers and display there status after certain interval"
    )
    parser.add_argument(
        "-i",
        "--interval",
        help="Time interval in seconds between server status reporting in seconds",
        type=int,
        required=True,
        dest="interval",
    )
    parser.add_argument(
        "-n",
        "--number",
        help="Total number of virtual server",
        type=int,
        required=True,
        dest="number",
    )
    parser.add_argument(
        "-f",
        "--file",
        help="Path to the file (either absolute or relative)",
        required=True,
        dest="file",
    )
    parser.add_argument(
        "-p",
        "--port",
        nargs="*",
        help="List of ports that must be equal to number of virtual servers",
        type=int,
        required=True,
        dest="ports",
    )
    return parser.parse_args()


def verify(args):
    # Verify number of ports equal the number of servers
    assert args.number == len(args.ports)
    for port in args.ports:
        assert netutils.check_sock(netutils.get_ip(), port)
    # Verify a valid file was passed
    assert pathlib.Path(args.file).is_file()
    return args


if __name__ == "__main__":
    args = verify(parse_args())

