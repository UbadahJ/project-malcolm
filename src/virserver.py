from multiprocessing import Queue
from queue import Empty

from utils import network
from utils.network import Status
from utils import file


class Server:
    def __init__(self, src, *, id: int, interval: int, port: int, queue: Queue):
        self.src = src
        self.id = id
        self.interval = interval
        self.port = port
        self.status = Status.IDLE
        self.queue = queue

        with network.create_server_connection(network.get_local_ip(), self.port) as soc:
            soc.listen()
            while self.status != Status.QUITING:
                if soc:
                    c_soc, addr = soc.accept()
                    self.status = Status(network.parse_parameter(c_soc))
                    self.update()
                    if self.status == Status.CHECKSUM:
                        network.send_parameter(c_soc, file.gen_checksum(self.src))
                    elif self.status == Status.FILE_SIZE:
                        pass
                    elif self.status == Status.TRANSFER:
                        pass
                    else:
                        pass

    def update(self):
        try:
            while True:
                self.queue.get_nowait()
        except Empty:
            self.queue.put("Server {} at port {}: Status {}".format(self.id, self.port, self.status))

    def kill(self):
        self.status = Status.QUITING
