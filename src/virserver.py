from io import BufferedReader
from multiprocessing import Queue
from queue import Empty
from typing import Optional

from utils import file, network
from utils.network import Request
import utils.console as con


class Server:
    def __init__(self, src: str, *, id: int, interval: int, port: int, queue: Queue):
        self.src: str = src
        self.id: int = id
        self.interval: int = interval
        self.port: int = port
        self.queue: Queue = queue
        self.request: Optional[Request] = None

        self._start()

    def _start(self):
        with network.create_server_connection(network.get_local_ip(), self.port) as soc:
            soc.listen()
            while True:
                try:
                    if soc:
                        c_soc, _ = soc.accept()
                        request, *params = network.parse_parameter(c_soc)
                        self.request = Request(request)
                        self.update()
                        if self.request == Request.CHECKSUM:
                            network.send_parameter(c_soc, file.gen_checksum(self.src))
                        elif self.request == Request.FILE_SIZE:
                            # TODO: Add code here
                            pass
                        elif self.request == Request.TRANSFER:
                            # TODO: Add code here
                            pass
                        else:
                            # TODO: Add code here
                            pass
                except Exception as e:
                    # TODO: Add better error handling
                    con.debug(e)

    def update(self):
        try:
            while True:
                self.queue.get_nowait()
        except Empty:
            self.queue.put(
                "Server {} at port {}: Status {}".format(
                    self.id, self.port, self.request
                )
            )
