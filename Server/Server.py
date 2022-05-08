from socket import AF_INET, SOCK_STREAM, socket, error
from threading import Thread, activeCount
from Server.config import IP, PORT, ENCODING, BYTES, DEFAULT, CONNECTION_LIMIT


class Server:
    def __init__(self):
        self.startup_allowed: bool = True
        self.connection: int = 0
        self.server: socket = socket(AF_INET, SOCK_STREAM)
        try:
            self.server.bind((IP, PORT))
            print(f'[SERVER] Server started at {IP, PORT}.')
        except error as socket_error:
            self.startup_allowed: bool = False
            print(f'[SERVER | CLIENT HANDLER] Error. (orig: {str(socket_error)})')
        self.alldata: list = [DEFAULT, DEFAULT]

    def client(self, client: socket, connection: int, address) -> None:
        client.send(str.encode(self.alldata[connection]))
        while True:
            try:
                data = client.recv(BYTES).decode(ENCODING)
                self.alldata[connection] = data[:-1] + 'R'
                if not data:
                    print('[SERVER | CLIENT HANDLER] No data. Disconnecting.')
                    break
                elif data == 'DISCONN':
                    print('[SERVER | CLIENT HANDLER] Disconnecting.')
                    break
                else:
                    reply = self.alldata[0] if connection == 1 else self.alldata[1]
                    # print(f'Received (#{connection}): {data}')
                    # print(f'Sending (#{connection}): {reply}')
                    client.sendall(str.encode(reply))
            except error as socket_error:
                print(f'[SERVER | CLIENT HANDLER] Mainloop error. (orig: {str(socket_error)})')
                break
        print(f'[SERVER | CLIENT HANDLER] Closing connection for {address}.')
        self.alldata[connection] = DEFAULT
        self.connection -= 1
        client.close()
        print(f'[SERVER | CLIENT HANDLER] Connection closed.')

    def listener(self) -> None:
        if not self.startup_allowed:
            return None
        self.server.listen(CONNECTION_LIMIT)
        print(f'[SERVER | LISTENER] Waiting for connections...')
        while True:
            client, address = self.server.accept()
            print(f'[SERVER | LISTENER] Connection with {address} has been established.')
            Thread(target=self.client, args=(client, self.connection, address)).start()
            print(f'[SERVER | LISTENER] Active connections (threads): {activeCount()-1} (or {activeCount()-2}).')
            print(f'[SERVER | LISTENER] Active connections (self.connection): {self.connection+1}.')
            self.connection += 1


def server_startup() -> None:
    server: Server = Server()
    server.listener()
