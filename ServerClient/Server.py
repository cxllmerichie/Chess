from socket import AF_INET, SOCK_STREAM, socket, error
from threading import Thread, active_count
from config import ENCODING, DEFAULT, BYTES, CONNECTION_LIMIT
from ServerClient.Client import IP, PORT
import random


class Server:
    def __init__(self):
        self.connections: int = 0
        self.data: dict = {}
        self.server: socket = socket(AF_INET, SOCK_STREAM)
        try:
            self.server.bind((IP, PORT))
            print(f'[SERVER] Server started at {IP, PORT}.')
        except error as socket_error:
            print(f'[SERVER | CLIENT HANDLER] Error. (orig: {str(socket_error)})')

    def client(self, client: socket, player_id: int, pair_id: int, address) -> None:
        client.send(str.encode(self.data[pair_id][player_id]))
        while True:
            try:
                data = client.recv(BYTES).decode(encoding=ENCODING)
                if not data:
                    print('[SERVER | CLIENT HANDLER] No data. Disconnecting.')
                    break
                self.data[pair_id][player_id] = data + self.data[pair_id][player_id][10:13] + 'R'
                reply = self.data[pair_id][0] if player_id == 1 else self.data[pair_id][1]
                # print(f'Received (#{player_id}): {data}')
                # print(f'Sending (#{player_id}): {reply}')
                client.sendall(str.encode(reply))
            except Exception as exception:
                print(f'[SERVER | CLIENT HANDLER] Mainloop exception. (orig: {str(exception)})')
                break
        print(f'[SERVER | CLIENT HANDLER] Closing connection for {address}.')
        try:
            del self.data[pair_id]
            print(f'[SERVER | CLIENT HANDLER] Game(id:{pair_id}) data successfully erased from the server.')
        except Exception:
            print(f'[SERVER | CLIENT HANDLER] Failed attempt to erase game(id:{pair_id}) data. ')
        self.connections -= 1
        client.close()
        print(f'[SERVER | CLIENT HANDLER] Connection with {address} closed.')

    def listener(self) -> None:
        self.server.listen(CONNECTION_LIMIT)
        print(f'[SERVER | LISTENER] Waiting for connections...')
        while True:
            client, address = self.server.accept()
            print(f'[SERVER | LISTENER] Connection with {address} has been established.')

            self.connections += 1
            player_id: int = 0
            pair_id: int = (self.connections - 1) // 2
            colors: tuple = ('w', 'b') if random.choice([1, 2]) == 1 else ('b', 'w')
            if self.connections % 2 == 1:
                self.data[pair_id] = [DEFAULT[:11] + colors[0] + ',', DEFAULT[:11] + colors[1] + ',']
                print(f'[SERVER | LISTENER] New game(id:{pair_id}) created.')
            else:
                print(f'[SERVER | LISTENER] Connected to existing game(id:{pair_id}). ')
                player_id = 1

            Thread(target=self.client, args=(client, player_id, pair_id, address)).start()
            print(f'[SERVER | LISTENER] Active connections (threads): {active_count()-1}).')
            print(f'[SERVER | LISTENER] Active connections (self.connection): {self.connections}.')


def server_startup() -> None:
    server: Server = Server()
    server.listener()
