from enum import Enum
import netutils
import fileutils

Status = Enum(
    "Status", {"IDLE":      "idle",
               "CHECKSUM":  "checksum",
               "FILE_SIZE": "file_size",
               "TRANSFER":  "transfer",
               "QUITING":   "quiting"
               }
)


class Server:
    def __init__(self, file, *, id: int, interval: int, port: int):
        self.file = file
        self.id = id
        self.interval = interval
        self.port = port
        self.status = Status.IDLE
        soc = netutils.create_server_connection(netutils.get_local_ip(), self.port)
        while self.status != Status.QUITING:
            soc.listen()
            self.status = netutils.parse_parameter(soc)
            if self.status == Status.CHECKSUM:
                netutils.send_parameter(soc, fileutils.gen_checksum(self.file))
            elif self.status == Status.FILE_SIZE:
                pass
            elif self.status == Status.TRANSFER:
                pass
            else:
                pass

    def update(self):
        print("Server {} at port {}: Status {}".format(self.id, self.port, self.status))

    def kill(self):
        self.status = Status.QUITING
