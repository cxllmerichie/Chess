# ToDo: AI algorithm
# ToDo: voice assistant
# ToDo: log.db
# FOR MULTIPLAYER
# ToDo: loser&winner, starting messages etc.
# ToDo: MULTI multiplayer
# ToDo: show the chessboard correctly for black player too
# ToDo: fix promotion
# ToDo: fix buttons draw
# ToDo: self-calculating bytes amount for client and server

from PyQt5.QtWidgets import QApplication
from Client.Application import Application
from Server.config import IP, PORT
from Server.Server import server_startup
from Client.Library import State
from _thread import start_new_thread
from socket import socket, AF_INET, SOCK_STREAM
from sys import argv


if __name__ == '__main__':
    server: socket = socket(AF_INET, SOCK_STREAM)
    if server.connect_ex((IP, PORT)) is not State.Started.value:
        start_new_thread(server_startup, ())
    server.close()

    application: QApplication = QApplication(argv)
    Application()
    application.exec()
