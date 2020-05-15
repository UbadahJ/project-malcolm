import asyncio
import socket
from itertools import groupby
from operator import itemgetter
from typing import Iterable, Optional

from utils import console as con, network
from utils.console import print
from utils.network import Request


class Client:
    def on_create(self):
        con.clear()
        con.box_print("Project Malcolm")
        print("Local IP Address:", network.get_local_ip())
        print("Public IP Address:", network.get_public_ip())
        print("Server IP Address:", self.address)
        print()
        print("Press any key to continue")
        con.getch()

    def __init__(self, *, address: str, ports: Iterable[str], output: str, resume: bool):
        self.output: str = output
        self.address: str = address
        self.ports: Iterable[str] = ports
        self.resume: bool = resume
        self.conns: Optional[Iterable[socket.socket]] = None
        self.checks: Optional[Iterable[str]] = None

        self.on_create()  # Show launch message to user
        self.generate_connections()  # Generate connections using netutils
        asyncio.run(self.get_checksum())  # Get the checksum of the files
        self.verify_checksum()  # Verify files and remove the unmatched servers

    def generate_connections(self):
        self.conns = [
            network.create_connection(self.address, int(port))
            for port in self.ports
        ]

    async def get_checksum(self):
        async def _get(soc: socket.socket) -> str:
            network.send_parameter(soc, Request.CHECKSUM.value)
            return network.parse_parameter(soc)

        self.checks = await asyncio.gather(*(_get(soc) for soc in self.conns))

    def verify_checksum(self):
        self.checks = sorted(self.checks)
        check_count = []
        # Group the same checksum ad make tuple with there count
        for _, g_iter in groupby(self.checks):
            tmp = list(g_iter)
            check_count.append((len(tmp), tmp[0]))
        # Find the max number of same checksum and return the checksum
        check_selected = max(check_count, key=itemgetter(0))[1]
        # Filter the ports whose checksum doesn't match
        self.ports, self.checks = map(list, zip(*[
            pair
            for pair in zip(self.ports, self.checks)
            if pair[1] == check_selected
        ]))


async def _get_checksum(soc: socket.socket):
    return network.parse_parameter(soc)
