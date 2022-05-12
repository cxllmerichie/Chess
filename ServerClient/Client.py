from socket import AF_INET, SOCK_STREAM, socket, error
from ServerClient.config import IP, PORT, ENCODING, BYTES


class Client:
    def __init__(self):
        self.client: socket = socket(AF_INET, SOCK_STREAM)
        try:
            self.client.connect((IP, PORT))
            self.data = self.client.recv(BYTES).decode(ENCODING)
        except error as socket_error:
            print(f'[CLIENT] Error. (orig: {socket_error})')

    def receive(self):
        try:
            return self.data
        except error as socket_error:
            print(f'[CLIENT | SEND] Error. (orig: {socket_error})')

    def send(self, data):
        try:
            self.client.send(str.encode(data))
            return self.client.recv(BYTES).decode(ENCODING)
        except error as socket_error:
            print(f'[CLIENT | SEND] Error. (orig: {socket_error})')
