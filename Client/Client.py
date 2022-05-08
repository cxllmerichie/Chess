from socket import AF_INET, SOCK_STREAM, socket, error
from Server.config import IP, PORT, ENCODING, BYTES


class Client:
    def __init__(self):
        self.client: socket = socket(AF_INET, SOCK_STREAM)
        try:
            self.client.connect((IP, PORT))
        except error as socket_error:
            print(f'[CLIENT | SEND] Error. (orig: {socket_error})')
        self.data = self.client.recv(BYTES).decode(ENCODING)

    def receive(self):
        return self.data

    def send(self, data):
        try:
            self.client.send(str.encode(data))
            return self.client.recv(BYTES).decode(ENCODING)
        except error as socket_error:
            print(f'[CLIENT | SEND] Error. (orig: {socket_error})')
