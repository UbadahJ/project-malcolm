import netutils
import fileutils
from multiprocessing import Queue
from queue import Empty

from netutils import Status


class Server:
    def __init__(self, file, *, id: int, interval: int, port: int, queue: Queue):
        self.file = file
        self.id = id
        self.interval = interval
        self.port = port
        self.status = Status.IDLE
        self.queue = queue

        with netutils.create_server_connection(netutils.get_local_ip(), self.port) as soc:
            soc.listen()
            while self.status != Status.QUITING:
                if soc:
                    c_soc, addr = soc.accept()
                    self.status = Status(netutils.parse_parameter(c_soc).decode("utf-8"))
                    self.update()
                    if self.status == Status.CHECKSUM:
                        netutils.send_parameter(c_soc, fileutils.gen_checksum(self.file))
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
