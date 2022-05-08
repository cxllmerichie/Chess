# ToDo: AI algorithm
# ToDo: MULTI multiplayer
# ToDo: voice assistant
# ToDo: winner / loser to log.txt
# ToDo: log.txt to db
# ToDo: promotion disables mouse click to avoid unnecessary click but it stops timers
# ToDo: fix buttons (draw, resign)
# ToDo: self-calculating bytes amount for client and server

from PyQt5.QtWidgets import QApplication
from Client.Application import Application
from Server.config import IP, PORT
from Server.Server import server_startup
from _thread import start_new_thread
from socket import socket, AF_INET, SOCK_STREAM
from sys import argv


if __name__ == '__main__':
    is_started_server: socket = socket(AF_INET, SOCK_STREAM)
    if is_started_server.connect_ex((IP, PORT)) != 0:
        start_new_thread(server_startup, ())
    is_started_server.close()

    application: QApplication = QApplication(argv)
    client: Application = Application()
    application.exec()
