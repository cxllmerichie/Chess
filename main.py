# ToDo: AI algorithm
# ToDo: MULTI multiplayer
# ToDo: voice assistant
# ToDo: winner / loser to log.txt
# ToDo: log.txt to db
# ToDo: promotion disables mouse click to avoid unnecessary click but it stops timers
# ToDo: en passant position should be marked as capturing but not position
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
    check_port: socket = socket(AF_INET, SOCK_STREAM)
    if check_port.connect_ex((IP, PORT)) != 0:
        start_new_thread(server_startup, ())
    check_port.close()

    application: QApplication = QApplication(argv)
    client: Application = Application()
    application.exec()
