from socket import AF_INET, SOCK_STREAM, socket, error
from _thread import start_new_thread
# from pickle import dumps, loads


class Server:
    def __init__(self, ip: str = '10.107.0.5', port: int = 5555, _bytes: int = 1024):
        self.IP: str = ip
        self.PORT: int = port
        self.BYTES: int = _bytes
        self.CONNECTIONS_LIMIT: int = 2

        self.socket = self.generate_socket()
        self.alldata: list = ['\t[DATA] user #1.', '\t[DATA] user #2.']
        self.player: int = 0

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
        connection.send(str.encode(self.alldata[player]))
        # connection.send(dumps(self.alldata[player]))
        while True:
            try:
                data = connection.recv(self.BYTES).decode()
                # data = loads(connection.recv(self.BYTES))
                self.alldata[player] = data
                if not data:
                    print('[SERVER | CLIENT] No data. Disconnecting.')
                    break
                else:
                    reply = self.alldata[0] if player == 1 else self.alldata[1]
                    print(f'Received: {data}')
                    print(f'Sending: {reply}')
                    connection.sendall(str.encode(reply))
                    # connection.sendall(dumps(reply))
            except:
                print('[SERVER | CLIENT] Mainloop raised error.')
                break
        print('[SERVER | CLIENT] Connection terminated.')
        connection.close()

    def listener(self) -> None:
        print(f'[SERVER | LISTENER] Listening stated. Awaiting for connections...')
        while True:
            connection, address = self.socket.accept()
            print(f'[SERVER | LISTENER] Connected to {address}')
            start_new_thread(self.client, (connection, self.player))
            self.player += 1


def server_startup(ip: str = '10.107.0.5', port: int = 5555, _bytes: int = 1024) -> None:
    server: Server = Server(ip, port, _bytes)
    server.listener()
