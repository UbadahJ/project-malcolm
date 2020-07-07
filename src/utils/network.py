import json
import platform
import socket
import struct
import subprocess
from enum import Enum
from time import sleep
from typing import Optional, Sequence
from urllib.request import urlopen

from utils.console import debug
from utils.nullsafe import notnone


def get_local_ip() -> str:
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        try:
            s.connect(("10.255.255.255", 1))
            ip = s.getsockname()[0]
        except Exception as e:
            debug(e)
            ip = "127.0.0.1"
    return ip


def get_public_ip() -> str:
    try:
        return json.loads(urlopen("https://api.myip.com").read())["ip"]
    except Exception as e:
        debug(e)
        return ""


def ping(url: str) -> bool:
    param = "-n" if platform.system().lower() == "windows" else "-c"
    command = ["ping", param, "1", url]
    return subprocess.call(command) == 0


def check_sock(ip: str, port: int) -> bool:
    with socket.socket() as sock:
        try:
            sock.bind((ip, port))
        except Exception as e:
            debug(e)
            return False
        else:
            return True


def create_server_connection(ip: str, port: int) -> socket.socket:
    return socket.create_server((ip, port))


def create_connection(ip: str, port: int) -> Optional[socket.socket]:
    soc = socket.socket()
    try:
        soc.connect((ip, port))
    except ConnectionRefusedError as e:
        debug(e)
        return None
    return soc


def recv_bytes(
        soc: socket.socket, size: int, wait: bool = True, retries: int = 3
) -> Optional[bytearray]:
    data = bytearray()
    while len(data) < size:
        packet: Optional[bytes] = None
        try:
            packet = soc.recv(size - len(data))
        except OSError as e:
            if wait:
                retries -= 1
                sleep(0.1)
            else:
                raise e
        if packet is None or retries <= 0:
            return None
        data.extend(packet)
    return data


def encode_parameter(*param: str) -> bytes:
    return "::".join(param).encode("utf-8")


def decode_parameter(param: bytes) -> Sequence[str]:
    return param.decode("utf-8").split("::")


def get_request(soc: socket.socket) -> Optional[bytes]:
    try:
        size = struct.unpack("I", notnone(recv_bytes(soc, 4)))
        return bytes(notnone(recv_bytes(soc, size[0])))
    except (TypeError, AssertionError):
        return None


def send_request(soc: socket.socket, param: bytes) -> None:
    try:
        soc.sendall(struct.pack("I", len(param)) + param)
    except OSError:
        pass


class Request(Enum):
    CHECKSUM, FILE_NAME, FILE_SIZE, TRANSFER = (str(i) for i in range(4))
