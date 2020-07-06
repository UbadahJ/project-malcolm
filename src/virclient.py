import asyncio
import os
import socket
from itertools import groupby
from operator import itemgetter
from typing import List, Optional, Sequence, Tuple, Union

from utils import console as con, network
from utils.collections import flatten, first
from utils.console import print
from utils.file import spilt
from utils.network import Request
from utils.nullsafe import assertnotnone, asserttype, optional


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
        self.file_name: Optional[str] = None
        self.conns: Optional[List[socket.socket]] = None
        self.checks: Optional[List[str]] = None
        self.file_size: Optional[int] = None
        self.data: Optional[List[bytes]] = None

        # Show launch message to user
        self.on_create()
        # Get the checksum of the files
        asyncio.run(self.get_checksum())
        # Verify files and remove the unmatched servers
        self.verify_checksum()
        # Fetch the file name from any server
        self.get_file_name()
        # Fetch the file size from any server
        self.get_file_size()
        # Get the data from server
        asyncio.run(self.get_data())
        # Output data
        self.flush_data()

    def generate_connections(self, *, sockets: Optional[Sequence[int]] = None) -> None:
        # Close all the existing sockets
        if self.conns is not None:
            for soc in self.conns:
                soc.close()
        # Check if only selected sockets needs to be recreated
        _conns: Optional[List[Optional[socket.socket]]] = \
            None if self.conns is None else [optional(c) for c in self.conns]
        if _conns is None or sockets is None:
            # Recreate all the sockets
            _conns = [
                network.create_connection(self.address, int(port))
                for port in self.ports
            ]
        else:
            # Recreate the sockets given in sockets sequence parameter
            for sock in sockets:
                _conns[sock] = network.create_connection(self.address, int(self.ports[sock]))
        # Remove all the ports that have None as a connection
        self.ports = [port for port, conn in zip(self.ports, _conns) if conn is not None]
        # Remove all the None connections
        self.conns = [conn for conn in _conns if conn is not None]

    async def get_checksum(self) -> None:
        self.generate_connections()
        self.checks = [str(check) for check in flatten(await asyncio.gather(
            *(self._async_get(soc, Request.CHECKSUM) for soc in self.conns)
        ))]

    def verify_checksum(self) -> None:
        assert self.checks is not None
        _checks = sorted(self.checks)
        check_count = []
        # Group the same checksum ad make tuple with there count
        for _, g_iter in groupby(_checks):
            tmp = list(g_iter)
            check_count.append((len(tmp), tmp[0]))
        # Find the max number of same checksum and return the checksum
        check_selected = max(check_count, key=itemgetter(0))[1]
        # Filter the ports whose checksum doesn't match
        self.ports, self.checks = map(list, zip(*[
            pair
            for pair in zip(self.ports, _checks)
            if pair[1] == check_selected
        ]))

    def get_file_name(self):
        self.generate_connections(sockets=(0,))
        self.file_name = str(
            assertnotnone(first(assertnotnone(self._get(self.conns[0], Request.FILE_NAME))))
        )

    def get_file_size(self) -> None:
        self.generate_connections(sockets=(0,))
        self.file_size = int(
            assertnotnone(first(assertnotnone(self._get(self.conns[0], Request.FILE_SIZE))))
        )

    async def get_data(self) -> None:
        def normalize(_tuple: Tuple[int, int]) -> Sequence[str]:
            return [str(_tuple[0]), str(_tuple[1])]

        self.generate_connections()
        self.data = [
            asserttype(bytes, elem)
            for elem in await asyncio.gather(
                *(self._async_get(soc, Request.TRANSFER, normalize(tp), decode=False)
                  for soc, tp in zip(
                    assertnotnone(self.conns),
                    spilt(file_size=assertnotnone(self.file_size), parts=len(self.ports) + 1)
                ))
            )
        ]

    def flush_data(self):
        os.chdir(self.output)
        with open(assertnotnone(self.file_name), 'wb') as f:
            for d in self.data:
                f.write(d)

    @staticmethod
    def _get(soc: socket.socket,
             request: Request,
             parameters: Sequence[str] = ('',),
             *,
             decode: bool = True) -> Optional[Union[Sequence[str], bytes]]:
        return asyncio.run(Client._async_get(soc, request, parameters, decode=decode))

    @staticmethod
    async def _async_get(soc: socket.socket,
                         request: Request,
                         parameters: Sequence[str] = ('',),
                         *,
                         decode: bool = True) -> Optional[Union[Sequence[str], bytes]]:
        network.send_request(soc, network.encode_parameter(request.value, *parameters))
        data: Optional[bytes] = network.get_request(soc)
        if data is not None and decode:
            return network.decode_parameter(data)
        return data
