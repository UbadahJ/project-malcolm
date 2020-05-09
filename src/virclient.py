import asyncio
import socket

import consoleutils as con
import netutils

from typing import Iterable

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

    def __init__(self, address: str, ports: Iterable[str], output: str, resume: bool):
        self.output = output
        self.address = address
        self.ports = ports
        self.resume = resume
        self.conns = None
        self.checks = None

        self.on_create()  # Show launch message to user
        self.generate_connections()  # Generate connections using netutils
        asyncio.run(self.get_checksum())  # Get the checksum of the files

    def generate_connections(self):
        self.conns = [
            netutils.create_connection(self.address, int(port))
            for port in self.ports
        ]

    async def get_checksum(self):
        self.checks = await asyncio.gather(
            *(netutils.parse_parameter(soc) for soc in self.conns)
        )


async def _get_checksum(soc: socket.socket):
    return netutils.parse_parameter(soc)
