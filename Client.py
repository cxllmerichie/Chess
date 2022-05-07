from socket import AF_INET, SOCK_STREAM, socket, error

IP: str = '10.107.0.5'
PORT: int = 5555
ENCODING: str = 'utf-8'
BYTES: int = 1024


class Client:
    def __init__(self):
        self.client: socket = socket(AF_INET, SOCK_STREAM)
        self.client.connect((IP, PORT))
        self.data = self.client.recv(BYTES).decode()

    def receive(self):
        return self.data

    def send(self, data):
        try:
            self.client.send(str.encode(data))
            return self.client.recv(BYTES).decode()
        except error as socket_error:
            print(f'[CLIENT | SEND] Error. (orig: {socket_error})')
