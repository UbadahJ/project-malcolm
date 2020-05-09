from enum import Enum

Status = Enum(
    "Status", {"IDLE": "idle", "PROCESSING": "processing", "QUITING": "quiting"}
)


class Server:
    def __init__(self, file, *, id: int, interval: int, port: int):
        self.file = file
        self.id = id
        self.interval = interval
        self.port = port
        self.status = Status.IDLE
        while self.status != Status.QUITING:
            pass

    def update(self):
        print("Server {} at port {}: Status {}".format(self.id, self.port, self.status))

    def kill(self):
        self.status = Status.QUITING
