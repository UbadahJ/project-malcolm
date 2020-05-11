import json
import platform
import socket
import struct
import subprocess
from enum import Enum
from time import sleep
from typing import Optional
from urllib.request import urlopen


def get_local_ip() -> str:
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        try:
            s.connect(("10.255.255.255", 1))
            ip = s.getsockname()[0]
        except:
            ip = "127.0.0.1"
    return ip


def get_public_ip() -> str:
    try:
        return json.loads(urlopen("https://api.myip.com").read())["ip"]
    except:
        return ""


def ping(url: str) -> bool:
    param = "-n" if platform.system().lower() == "windows" else "-c"
    command = ["ping", param, "1", url]
    return subprocess.call(command) == 0


def check_sock(ip: str, port: int) -> bool:
    with socket.socket() as sock:
        try:
            sock.bind((ip, port))
        except:
            return False
        else:
            return True


def create_server_connection(ip: str, port: int) -> socket.socket:
    return socket.create_server((ip, port))


def create_connection(ip: str, port: int) -> socket.socket:
    soc = socket.socket()
    soc.connect((ip, port))
    return soc


def recv_bytes(soc: socket.socket, bytes: int, wait: bool = True) -> Optional[bytearray]:
    data = bytearray()
    while len(data) < bytes:
        try:
            packet = soc.recv(bytes - len(data))
        except OSError as e:
            if wait:
                sleep(1)
                continue
            else:
                raise e
        if not packet:
            return None
        data.extend(packet)
    return data


def add_parameter(param: str) -> bytes:
    return struct.pack("I", len(param)) + param.encode("utf-8")


def parse_parameter(soc: socket.socket) -> str:
    size = recv_bytes(soc, 4)
    return recv_bytes(soc, struct.unpack("I", size)[0]).decode('utf-8')


def send_parameter(soc: socket.socket, param: str) -> None:
    soc.sendall(add_parameter(param))


class Request(Enum):
    CHECKSUM, FILE_SIZE, TRANSFER = range(3)

