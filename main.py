# ToDo: AI algorithm
# ToDo: voice assistant
# ToDo: log.db
# FOR MULTIPLAYER
# ToDo: loser&winner, starting messages etc.
# ToDo: MULTI multiplayer
# ToDo: fix promotion
# ToDo: fix buttons draw (if we wait too long after draw was suggested the responding client crashes)
# ToDo: self-calculating bytes amount for client and server
# ToDo: generate requirements
# ToDo: generate executive

# from ServerClient.config import IP, PORT
# from ServerClient.ServerClient import server_startup
# from ClientMultipalyer.Library import State
# from _thread import start_new_thread
# from socket import socket, AF_INET, SOCK_STREAM
# from time import sleep

from PyQt5.QtWidgets import QApplication
from Common.Application import Application
from sys import argv

if __name__ == '__main__':
    # server: socket = socket(AF_INET, SOCK_STREAM)
    # if server.connect_ex((IP, PORT)) is not State.Started.value:
    #     start_new_thread(server_startup, ())
    # server.close()
    # sleep(600)

    application: QApplication = QApplication(argv)
    app: Application = Application()
    application.exec()
