import datetime
from multiprocessing import Queue
from queue import Empty
from typing import Optional

import utils.console as con
from utils import file, network
from utils.network import Request


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
            while True:
                self.request = None
                try:
                    soc.listen()
                    if soc:
                        c_soc, _ = soc.accept()
                        request, *params = network.decode_parameter(network.get_request(c_soc))
                        self.request = Request(request)
                        self.update()
                        if self.request == Request.CHECKSUM:
                            network.send_request(
                                c_soc, network.encode_parameter(file.gen_checksum(self.src))
                            )
                        elif self.request == Request.FILE_NAME:
                            network.send_request(
                                c_soc, network.encode_parameter(file.get_file_name(self.src))
                            )
                        elif self.request == Request.FILE_SIZE:
                            network.send_request(
                                c_soc, network.encode_parameter(str(file.get_size(self.src)))
                            )
                        elif self.request == Request.TRANSFER:
                            start, end = int(params[0]), int(params[1])
                            with open(self.src, 'rb') as f:
                                f.seek(start)
                                data = f.read(end-start)
                                network.send_request(c_soc, data)
                except OSError as e:
                    con.error("Error occurred by OS: {}\nArgument provided: {}".format(e, e.args))
                    with open('log_server.log', 'a+') as f:
                        f.write('[{}] ERROR {}'.format(datetime.datetime.now(), e))
                finally:
                    c_soc.close()

    def update(self):
        try:
            while True:
                self.queue.get_nowait()
        except Empty:
            status = self.request
            if self.request is None:
                status = 'ALIVE'
            self.queue.put(
                "Server {} at port {}: Status {}".format(self.id, self.port, status)
            )
