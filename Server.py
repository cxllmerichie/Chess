from socket import AF_INET, SOCK_STREAM, socket, error
# from _thread import start_new_thread
# from pickle import dumps, loads
# from threading import Thread, activeCount
"""


class Server:
    def __init__(self):
        self.CONNECTION_LIMIT: int = 2

        self.server: socket = socket(AF_INET, SOCK_STREAM)
        self.server.bind((IP, PORT))

    def client_handler(self, client: socket):
        while True:
            received = client.recv(BYTES).decode(ENCODING)
            if not received:
                print(f'[SERVER | CLIENT HANDLER] Data was not received.')
                break
            client.send()
        print('[SERVER | CLIENT HANDLER] Closing client connection.')
        client.close()
        print(f'[SERVER | CLIENT HANDLER] Connection closed.')

    def listen(self):
        self.server.listen(self.CONNECTION_LIMIT)
        print(f'[SERVER | LISTEN] Server is listening on {IP}.')
        client, address = self.server.accept()
        print(f'[SERVER | LISTEN] Connection from {address} has been established.')
        Thread(target=self.client_handler, args=(client,)).start()
        print(f'[SERVER | LISTEN] Active connections (threads): {activeCount()-1}.')


class Client:
    def __init__(self):
        self.client: socket = socket(AF_INET, SOCK_STREAM)
        self.client.connect((IP, PORT))

    def send(self, data: str):
        sending = bytes(data, ENCODING)
        self.client.send(sending)
"""
IP: str = '10.107.0.5'
PORT: int = 5555
ENCODING: str = 'utf-8'
BYTES: int = 1024


class Network:
    def __init__(self):
        self.socket = socket(AF_INET, SOCK_STREAM)
        self.socket.connect((IP, PORT))
        self.data = self.socket.recv(BYTES).decode()

    def receive(self):
        return self.data

    def send(self, data):
        try:
            self.socket.send(str.encode(data))
            return self.socket.recv(BYTES).decode()
            # self.socket.send(dumps(data))
            # return loads(self.socket.recv(self.BYTES))
        except error as socket_error:
            print(f'[NETWORK | SEND] Error raised. (orig: {socket_error})')
