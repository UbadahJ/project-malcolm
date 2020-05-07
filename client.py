#! /bin/python3

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
        type=bool,
        default=False,
        dest="resume",
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()

