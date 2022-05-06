import socket
import pickle


class Network:
    def __init__(self, ip: str = '10.107.0.5', port: int = 5555, _bytes: int = 2048):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.IP: str = ip
        self.PORT: int = port
        self.BYTES: int = _bytes
        self.address = (self.IP, self.PORT)
        self.game_state = self.connect()

    def get_game_state(self):
        return self.game_state

    def connect(self):
        try:
            self.client.connect(self.address)
            return pickle.loads(self.client.recv(self.BYTES))
        except:
            pass

    def send(self, data):
        try:
            self.client.send(pickle.dumps(data))
            return pickle.loads(self.client.recv(self.BYTES))
        except BrokenPipeError:
            print('Server is down. (orig: [Errno 32] Broken pipe)')
        except socket.error as socket_error:
            print(str(socket_error))
