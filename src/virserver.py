from enum import Enum
import netutils
import fileutils
from multiprocessing import Queue
from queue import Empty

Status = Enum(
    "Status", {"IDLE":      "idle",
               "CHECKSUM":  "checksum",
               "FILE_SIZE": "file_size",
               "TRANSFER":  "transfer",
               "QUITING":   "quiting"
               }
)


class Server:
    def __init__(self, file, *, id: int, interval: int, port: int, queue: Queue):
        self.file = file
        self.id = id
        self.interval = interval
        self.port = port
        self.status = Status.IDLE
        self.queue = queue

        with netutils.create_server_connection(netutils.get_local_ip(), self.port) as soc:
            while self.status != Status.QUITING:
                soc.listen()
                self.status = netutils.parse_parameter(soc)
                self.update()
                if self.status == Status.CHECKSUM:
                    netutils.send_parameter(soc, fileutils.gen_checksum(self.file))
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
