import asyncio
import os
import socket
from itertools import groupby
from json import dumps
from operator import itemgetter
from typing import List, Optional, Sequence, Tuple, Union, MutableSequence

import console as con
from console import print
from serialization.client import dump_hook
from utils import network
from utils.collections import flatten, first, empty
from utils.decorators import retry
from utils.file import spilt
from utils.network import Request
from utils.nullsafe import notnone, optional, assertsequencetype, assertoptionaltype


class Client:
    output: str
    address: str
    ports: List[str]
    resume: bool
    file_name: str
    conns: Sequence[socket.socket]
    checks: Sequence[str]
    file_size: int
    data_unfinished: MutableSequence[Tuple[Tuple[int, int], Optional[bytes]]]
    data: Sequence[bytes]

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
        self.output = output
        self.address = address
        self.ports = ports
        self.resume = resume

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
        _conns: Optional[MutableSequence[Optional[socket.socket]]] = None
        try:
            for soc in self.conns:
                soc.close()
            # Check if only selected sockets needs to be recreated
            _conns = None if self.conns is None else [optional(c) for c in self.conns]
        except AttributeError:
            pass
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
        # Check if there are any working ports
        # If a port is in list, it means it was working previously
        if empty(self.ports):
            # If no port is available, then quit
            print('All connections refused ...')
            # Call resume method to make sure data is stored for resume
            self.dump_resume()
            quit(1)

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

    async def get_data(self) -> None:
        def normalize(_tuple: Tuple[int, int], start: int = 0) -> Sequence[str]:
            # Return the data return by file.split to str to be sent as parameter
            return [str(start + _tuple[0]), str(start + _tuple[1])]

        async def fetch(start: int, end: int) \
                -> MutableSequence[Tuple[Tuple[int, int], Optional[bytes]]]:
            # Regenerate the connections
            self.generate_connections()
            # Split the data into parts for connections
            _split: Sequence[Tuple[int, int]] = \
                spilt(file_size=notnone(end - start), parts=len(self.ports) + 1)
            # Fetch the data for each connection
            _data: Sequence[Optional[bytes]] = [
                # Assert if the type of element is bytes or None
                assertoptionaltype(bytes, data) for data in
                # Use high-level co-routine to fetch data
                await asyncio.gather(*(
                    self._async_get(soc, Request.TRANSFER, normalize(tp), decode=False)
                    for soc, tp in zip(notnone(self.conns), _split)
                ))
            ]
            return list(zip(_split, _data))

        async def verify(list_: MutableSequence[Tuple[Tuple[int, int], Optional[bytes]]]) \
                -> Sequence[bytes]:
            # Enumerate is required since we are updating the list contents
            # Basically compensating for pass-by-value
            for i, ((start, end), seg) in enumerate(list_):
                try:
                    # If the segment is None
                    if seg is None:
                        list_[i] = (
                            (start, end),
                            bytes(b"".join(
                                # Assert if all the contents of sequence are bytes
                                # Recursive call itself until the content has been resolved
                                # Or all the connections have been refused
                                assertsequencetype(
                                    bytes, flatten(await verify(await fetch(start, end)))
                                )
                            ))
                        )
                except AssertionError:
                    # If this exception occurs, all connections have been closed
                    await self.get_data()
                    # This should never be returned since self-call will quit the program
                    return []
            return [notnone(seg) for (_, _), seg in list_]

        # Store the data in unverified (error-prone) data in tmp variable
        self.data_unfinished = await fetch(0, notnone(self.file_size))
        # Verify the data integrity
        self.data = await verify(self.data_unfinished)

    def dump_resume(self):
        # Check if the data exists
        save_resume_data: bool = False
        try:
            # Destructive unpacking of the tuple
            # Discarding start and end since they are not required
            for (_, _), data in self.data_unfinished:
                # Check if there is any element is None
                # Since there is no need to create resume file otherwise
                if data is not None:
                    save_resume_data = True
        except (NameError, ValueError, AttributeError):
            # Exists if the variable doesn't exists or data is incompatible
            pass
        # If there is data
        if save_resume_data:
            print('Saving resume data ...')
            with open('resume.json', 'w') as f:
                # Dump the data using serialization hook
                f.write(dumps(self, default=dump_hook))
        else:
            print('No data was fetched ...')

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
