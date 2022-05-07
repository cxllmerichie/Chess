from socket import AF_INET, SOCK_STREAM, socket, error
from _thread import start_new_thread
# from pickle import dumps, loads

connections: int = 0


class Network:
    def __init__(self, ip: str = '10.107.0.5', port: int = 5555, _bytes: int = 1024):
        self.IP: str = ip
        self.PORT: int = port
        self.BYTES: int = _bytes

        self.socket = socket(AF_INET, SOCK_STREAM)
        self.address = (self.IP, self.PORT)
        self.data = self.connect()

    @staticmethod
    def noc():
        return connections

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


class Server:
    def __init__(self, ip: str = '10.107.0.5', port: int = 5555, _bytes: int = 1024):
        self.IP: str = ip
        self.PORT: int = port
        self.BYTES: int = _bytes
        self.CONNECTIONS_LIMIT: int = 2

        self.socket = self.generate_socket()
        self.data: str = '[DATA]'

    def generate_socket(self) -> socket:
        _socket: socket = socket(AF_INET, SOCK_STREAM)
        try:
            _socket.bind((self.IP, self.PORT))
        except error as socket_error:
            print(f'[SERVER | SOCKET] socket.bind((IP, PORT)) raised: {socket_error}')
        _socket.listen(2)
        print('[SERVER | SOCKET] Socket generated. Listening might be stated.')
        return _socket

    def client(self, connection, player) -> None:
        connection.send(str.encode(self.data))
        # connection.send(dumps(self.alldata[player]))
        while True:
            try:
                data = connection.recv(self.BYTES).decode()
                # data = loads(connection.recv(self.BYTES))
                self.data = data
                if not data:
                    print('[SERVER | CLIENT] No data. Disconnecting.')
                    break
                else:
                    print(f'Received (#{player}): {data}')
                    print(f'Sending (#{player}): {data}')
                    connection.sendall(str.encode(data))
                    # connection.sendall(dumps(reply))
            except:
                print('[SERVER | CLIENT] Mainloop raised error.')
                break
        print('[SERVER | CLIENT] Connection terminated.')
        connection.close()

    def listener(self) -> None:
        global connections
        print(f'[SERVER | LISTENER] Listening stated. Awaiting for connections...')
        while True:
            connection, address = self.socket.accept()
            print(f'[SERVER | LISTENER] Connected to {address}')
            connections += 1
            start_new_thread(self.client, (connection, connections))


def server_startup(ip: str = '10.107.0.5', port: int = 5555, _bytes: int = 1024) -> None:
    server: Server = Server(ip, port, _bytes)
    server.listener()
