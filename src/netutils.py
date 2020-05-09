import json
import platform
import socket
import struct
import subprocess
from typing import Union
from urllib.request import urlopen


def get_local_ip() -> str:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("10.255.255.255", 1))
        IP = s.getsockname()[0]
    except:
        IP = "127.0.0.1"
    finally:
        s.close()
    return IP


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


def recv_bytes(soc: socket.socket, bytes: int) -> Union[bytearray, None]:
    data = bytearray()
    while len(data) < bytes:
        packet = soc.recv(bytes - len(data))
        if not packet:
            return None
        data.extend(packet)
    return data


def add_parameter(param: str) -> bytes:
    return struct.pack("i", len(param)) + param.encode("utf-8")


def parse_parameter(soc: socket.socket):
    size = recv_bytes(soc, 4)
    return recv_bytes(soc, struct.unpack("I", size)[0])
