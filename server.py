#! /bin/python3

import argparse


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
    )
    parser.add_argument(
        "-n", "--number", help="Total number of virtual server", type=int, required=True
    )
    parser.add_argument(
        "-f",
        "--file",
        help="Path to the file (either absolute or relative)",
        required=True,
    )
    parser.add_argument(
        "-p",
        "--port",
        nargs="*",
        help="List of ports that must be equal to number of virtual servers",
        type=int,
        required=True,
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    