from socket import AF_INET, SOCK_STREAM, socket, error
from ServerClient.config import ENCODING, BYTES

IP: str = '127.0.0.1'
PORT: int = 5555


def set_ip(ip: str) -> None:
    global IP
    IP = ip


def set_port(port: str) -> None:
    global PORT
    PORT = int(port)


class Client:
    def __init__(self):
        self.client: socket = socket(AF_INET, SOCK_STREAM)
        try:
            self.client.connect((IP, PORT))
            self.data = self.client.recv(BYTES).decode(encoding=ENCODING)
        except error as socket_error:
            return socket_error

    def receive(self):
        try:
            return self.data
        except error as socket_error:
            return socket_error
            # print(f'[CLIENT | Receive] Error: ({socket_error}).')

    def send(self, data):
        try:
            self.client.send(str.encode(data))
            return self.client.recv(BYTES).decode(encoding=ENCODING)
        except error as socket_error:
            return socket_error
            # print(f'[CLIENT | SEND] Error: ({socket_error}).')
