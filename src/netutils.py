import socket


def get_ip() -> str:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("10.255.255.255", 1))
        IP = s.getsockname()[0]
    except:
        IP = "127.0.0.1"
    finally:
        s.close()
    return IP


def check_sock(ip: str, port: int) -> bool:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        try:
            sock.bind((ip, port))
        except:
            return False
        else:
            return True


def create_conn(ip: str, port: int) -> socket.socket:
    soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    soc.bind((ip, port))
    soc.listen(1)
    return soc


def recv_bytes(soc: socket.socket, bytes: int) -> bytearray:
    data = bytearray()
    while len(data) < bytes:
        packet = soc.recv(bytes - len(data))
        if not packet:
            return None
        data.extend(packet)
    return data
