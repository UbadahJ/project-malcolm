#! /bin/python3

import argparse
import multiprocessing as mp
import pathlib
import time

import consoleutils as con
import fileutils
import netutils
from virserver import Server


def parse_args() -> argparse.Namespace:
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
        # Verify number of ports equal the number of servers
        print("Validating server count ... ", end="")
        assert args.number == len(args.ports)
        con.success("OK")
        print("Validating server ports ... ")
        for port in args.ports:
            print("\t{} ... ".format(port), end="")
            assert netutils.check_sock(netutils.get_local_ip(), port)
            con.success("OK")
        # Verify a valid file was passed
        print("Validating file ... ", end="")
        assert pathlib.Path(args.file).is_file()
        con.success("OK")
        return args
    except AssertionError:
        con.error("FAILED")
        quit(1)


def init(args: argparse.Namespace):
    con.clear()
    con.box_print("Project Malcolm")
    print("Local IP Address:", netutils.get_local_ip())
    print("Public IP Address:", netutils.get_public_ip())
    print("File size:", fileutils.get_size(args.file), "Bytes")
    print("Checksum:", fileutils.gen_checksum(args.file))
    print()
    print("Press any key to start servers")
    con.getch()


if __name__ == "__main__":
    args = verify(parse_args())
    init(args)

    procs = []
    for port in args.ports:
        queue = mp.Queue()
        process = mp.Process(target=Server, args=(args.file,),
                             kwargs={'id': int(port), 'interval': args.interval, 'port': int(port), 'queue': queue})
        process.start()
        procs.append((process, queue))

    while True:
        try:
            for process, queue in procs:
                print(queue.get())
                time.sleep(args.interval)
        except KeyboardInterrupt:
            for process, queue in procs:
                process.close()
        finally:
            break
