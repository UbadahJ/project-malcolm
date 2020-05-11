from multiprocessing import Queue
from queue import Empty

from utils import file
from utils import network
from utils.network import Request
from utils.console import print

class Server:
    def __init__(self, src, *, id: int, interval: int, port: int, queue: Queue):
        self.src = src
        self.id = id
        self.interval = interval
        self.port = port
        self.queue = queue
        self.request = None

        self._start()

    def _start(self):
        with network.create_server_connection(network.get_local_ip(), self.port) as soc:
            soc.listen()
            while True:
                if soc:
                    c_soc, _ = soc.accept()
                    self.request = Request(network.parse_parameter(c_soc))
                    self.update()
                    if self.request == Request.CHECKSUM:
                        network.send_parameter(c_soc, file.gen_checksum(self.src))
                    elif self.request == Request.FILE_SIZE:
                        pass
                    elif self.request == Request.TRANSFER:
                        pass
                    else:
                        pass

    def update(self):
        try:
            while True:
                self.queue.get_nowait()
        except Empty:
            self.queue.put("Server {} at port {}: Status {}".format(self.id, self.port, self.request))
