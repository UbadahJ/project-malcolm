#! /bin/python3

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
    try:
        # Verify number of ports equal the number of servers
        print('Validating server count ... ', end='')
        assert args.number == len(args.ports)
        print('OK')
        print('Validating server ports ... ')
        for port in args.ports:
            print('\t{} ... '.format(port), end='')
            assert netutils.check_sock(netutils.get_local_ip(), port)
            print('OK')
        # Verify a valid file was passed
        print('Validating file ... ', end='')
        assert pathlib.Path(args.file).is_file()
        print('OK')
        return args
    except AssertionError:
        print('FAILED')
        quit(1)

if __name__ == "__main__":
    args = verify(parse_args())