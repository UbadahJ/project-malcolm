import asyncio
import socket
from itertools import groupby
from operator import itemgetter
from typing import List, Optional

from utils import console as con, network
from utils.console import print
from utils.network import Request


class Client:
    def on_create(self) -> None:
        con.clear()
        con.box_print("Project Malcolm")
        print("Local IP Address:", network.get_local_ip())
        print("Public IP Address:", network.get_public_ip())
        print("Server IP Address:", self.address)
        print()
        print("Press any key to continue")
        con.getch()

    def __init__(self, *, address: str, ports: List[str], output: str, resume: bool):
        self.output: str = output
        self.address: str = address
        self.ports: List[str] = ports
        self.resume: bool = resume
        self.conns: Optional[List[socket.socket]] = None
        self.checks: Optional[List[str]] = None
        self.file_size: Optional[int] = None

        self.on_create()  # Show launch message to user
        asyncio.run(self.get_checksum())  # Get the checksum of the files
        self.verify_checksum()  # Verify files and remove the unmatched servers
        self.get_file_size()

    def generate_connections(self) -> None:
        if self.conns is not None:
            for soc in self.conns:
                soc.close()
        self.conns = [
            network.create_connection(self.address, int(port))
            for port in self.ports
        ]

    async def get_checksum(self) -> None:
        async def _get(soc: socket.socket) -> str:
            network.send_parameter(soc, Request.CHECKSUM.value)
            return network.parse_parameter(soc)[0]

        self.generate_connections()
        self.checks = await asyncio.gather(*(_get(soc) for soc in self.conns))

    def verify_checksum(self) -> None:
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

    def get_file_size(self) -> None:
        self.generate_connections()
        network.send_parameter(self.conns[0], Request.FILE_SIZE.value)
        self.file_size = int(network.parse_parameter(self.conns[0])[0])
