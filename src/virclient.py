import asyncio
import socket

import consoleutils as con
import netutils
from netutils import Status

from typing import Iterable, Optional


class Client:
    def on_create(self):
        con.clear()
        con.box_print("Project Malcolm")
        print("Local IP Address:", netutils.get_local_ip())
        print("Public IP Address:", netutils.get_public_ip())
        print("Server IP Address:", self.address)
        print()
        print("Press any key to continue")
        con.getch()

    def __init__(self, *, address: str, ports: Iterable[str], output: str, resume: bool):
        self.output = output
        self.address = address
        self.ports = ports
        self.resume = resume
        self.conns = None
        self.checks = None

        self.on_create()  # Show launch message to user
        self.generate_connections()  # Generate connections using netutils
        asyncio.run(self.get_checksum())  # Get the checksum of the files
        print(self.checks)

    def generate_connections(self):
        self.conns = [
            netutils.create_connection(self.address, int(port))
            for port in self.ports
        ]

    async def get_checksum(self):
        async def _get(soc: socket.socket) -> str:
            netutils.send_parameter(soc, Status.CHECKSUM.value)
            return netutils.parse_parameter(soc).decode('utf-8')
        self.checks = await asyncio.gather(
            *(_get(soc) for soc in self.conns)
        )


async def _get_checksum(soc: socket.socket):
    return netutils.parse_parameter(soc)
