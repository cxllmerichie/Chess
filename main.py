# CHESS GAME FEATURING
# ToDo: AI algorithm
# ToDo: voice assistant
# ToDo: create and store log.db for singleplayer (and maybe practice/multiplayer)
# MULTIPLAYER
# ToDo: fix promotion
# ToDo: fix draw, resign
# ToDo: fix disconnect
# ToDo: self-calculating bytes amount for client and server
# EXECUTABLE APPLICATION
# ToDo: generate requirements
# ToDo: generate executive
# APPLICATION
# ToDo: configure settings menu (assets, (size))
# ToDo: configure toolbar/menubar (help, about, view(shortcuts), etc.)

# from ServerClient.config import IP, PORT
# from ServerClient.Server import server_startup
# from Common.Library import State
# from _thread import start_new_thread
# from socket import socket, AF_INET, SOCK_STREAM

from PyQt5.QtWidgets import QApplication
from Common.Application import Application
from sys import argv

if __name__ == '__main__':
    # server: socket = socket(AF_INET, SOCK_STREAM)
    # if server.connect_ex((IP, PORT)) is not State.Started.value:
    #     start_new_thread(server_startup, ())
    # server.close()

    application: QApplication = QApplication(argv)
    app: Application = Application()
    application.exec()
