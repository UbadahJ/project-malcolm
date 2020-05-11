#! /bin/python3

import argparse
import multiprocessing as mp
from queue import Empty
import pathlib
import time

from utils import console as con, file, network
from utils.console import print
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
            assert network.check_sock(network.get_local_ip(), port)
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
    print("Local IP Address:", network.get_local_ip())
    print("Public IP Address:", network.get_public_ip())
    print("File size:", file.get_size(args.file), "Bytes")
    print("Checksum:", file.gen_checksum(args.file))
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

    status = ["" for i in procs]
    while True:
        try:
            for i, (process, queue) in enumerate(procs):
                con.clear()
                try:
                    status[i] = queue.get_nowait()
                    con.debug(locals())
                except Empty:
                    pass
                print(status[i])
        except KeyboardInterrupt as e:
            for process, queue in procs:
                process.close()
            break
        except Exception as e:
            con.error(e)
        else:
            time.sleep(args.interval)
