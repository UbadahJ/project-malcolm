import asyncio
import os
import socket
from itertools import groupby
from operator import itemgetter
from typing import List, Optional, Sequence, Tuple, Union, Any

from utils import network
import console as con
from utils.decorators import retry
from utils.collections import flatten, first, empty
from console import print
from utils.file import spilt
from utils.network import Request
from utils.nullsafe import notnone, optional, asserttype


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
        self.data: List[bytes]

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
        self.data = asyncio.run(self.get_data(0, notnone(self.file_size)))
        # Output data
        self.flush_data()

    def generate_connections(self, *, sockets: Optional[Sequence[int]] = None) -> None:
        # Check if there are any working ports
        # If a port is in list, it means it was working previously
        if empty(self.ports):
            # If no port is available, then quit
            # TODO: Add resume here
            quit(1)
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
        self.ports, self.checks = map(list, zip(*[
            (port, str(check))
            for port, check in zip(self.ports, [
                __check
                for __check in flatten(await asyncio.gather(
                    *(self._async_get(soc, Request.CHECKSUM) for soc in self.conns)
                ))
            ])
            if check is not None
        ]))

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
            (port, check)
            for port, check in zip(self.ports, _checks)
            if check == check_selected
        ]))

    @retry(AssertionError)
    def get_file_name(self):
        self.generate_connections(sockets=(0,))
        self.file_name = str(
            notnone(first(notnone(self._get(self.conns[0], Request.FILE_NAME))))
        )

    @retry(AssertionError)
    def get_file_size(self) -> None:
        self.generate_connections(sockets=(0,))
        self.file_size = int(
            notnone(first(notnone(self._get(self.conns[0], Request.FILE_SIZE))))
        )

    async def get_data(self, start: int, end: int) -> List[bytes]:
        def normalize(_tuple: Tuple[int, int]) -> Sequence[str]:
            return [str(start + _tuple[0]), str(start + _tuple[1])]

        self.generate_connections()
        _split: List[Tuple[int, int]] = \
            spilt(file_size=notnone(end - start), parts=len(self.ports) + 1)
        _data: List[Any] = list(await asyncio.gather(*(
            self._async_get(soc, Request.TRANSFER, normalize(tp), decode=False)
            for soc, tp in zip(notnone(self.conns), _split))))

        for index, seg in enumerate(_data):
            if seg is None:
                _data[index] = flatten(await self.get_data(*_split[index]))

        return [asserttype(bytes, d) for d in _data]

    def flush_data(self):
        os.chdir(self.output)
        with open(notnone(self.file_name), 'wb') as f:
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
