#! /bin/python3

# TODO: Replace asserts with Exceptions

import pathlib
import argparse

def parse_args():
    parser = argparse.ArgumentParser(
        description="Launches a client that can connect to multiple servers that includes error handling and file verification"
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
        action='store_true',
        default=False,
        dest="resume",
    )
    return parser.parse_args()

def verify(args):
    try:
        print('Validating IP Address ... ', end='')
        ip = args.address.split('.')
        # Check if IP has 4 decimal point
        assert len(ip) == 4
        # Check if any of them is empty
        for ad in ip:
            assert len(ad) != 0
        print('OK')
        # Verify if the path given is valid directory
        print('Validating directory ... ', end='')
        assert pathlib.Path(args.output).is_dir()
        print('OK')
        return args
    except AssertionError:
        print('FAILED')
        quit(1)

if __name__ == "__main__":
    args = verify(parse_args())