from socket import AF_INET, SOCK_STREAM, socket, error
# from pickle import dumps, loads


class Network:
    def __init__(self, ip: str = '10.107.0.5', port: int = 5555, _bytes: int = 1024):
        self.IP: str = ip
        self.PORT: int = port
        self.BYTES: int = _bytes

        self.socket = socket(AF_INET, SOCK_STREAM)
        self.address = (self.IP, self.PORT)
        self.data = self.connect()

    def get_data(self):
        return self.data

    def connect(self):
        try:
            self.socket.connect(self.address)
            return self.socket.recv(self.BYTES).decode()
            # return loads(self.socket.recv(self.BYTES))
        except:
            print('[NETWORK | CONNECT] Connection failed.')
            pass

    def send(self, data):
        try:
            self.socket.send(str.encode(data))
            return self.socket.recv(self.BYTES).decode()
            # self.socket.send(dumps(data))
            # return loads(self.socket.recv(self.BYTES))
        except BrokenPipeError:
            print('[NETWORK | SEND] Server is down. (orig: [Errno 32] Broken pipe)')
        except error as socket_error:
            print(f'[NETWORK | SEND] Error raised. (orig: {socket_error})')
