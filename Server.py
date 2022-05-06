import socket
import pickle
from _thread import start_new_thread
from ChessGame import ChessGame
from Game import Game


class Server:
    def __init__(self, ip: str = '10.107.0.5', port: int = 5555):
        self.IP: str = ip
        self.PORT: int = port
        self.socket = self.generate_socket()
        self.BYTES: int = 2048

        self.connected: set = set()
        self.games: dict = {}
        self.id_counter: int = 0

        self.alldata: list = [ChessGame, ChessGame]
        self.player: int = 0

    def generate_socket(self):
        _socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            _socket.bind((self.IP, self.PORT))
            _socket.listen()
            print("Waiting for a connection...")
        except socket.error as _error:
            print(str(_error))
        return _socket

    def client(self, connection, player, game_id):
        #connection.send(pickle.dumps(self.alldata[player]))
        connection.send(pickle.dumps(self.alldata[player]))
        while True:
            try:
                data = pickle.loads(connection.recv(self.BYTES))
                self.alldata[player] = data
                if not data:
                    print("Disconnected.")
                    break
                else:
                    reply = self.alldata[0] if player == 1 else self.alldata[1]
                connection.sendall(pickle.dumps(reply))
            except:
                break
        print("Connection terminated.")
        connection.close()

    def start_server(self):
        while True:
            connection, address = self.socket.accept()
            print(f"Connected to address: {address}")

            self.id_counter += 1
            player: int = 0
            game_id = (self.id_counter - 1) // 2
            if self.id_counter % 2 == 1:
                self.games[game_id] = Game(game_id)
                print('Creating a new game...')
            else:
                self.games[game_id].ready = True
                player = 1
            start_new_thread(self.client, (connection, self.player, game_id))
