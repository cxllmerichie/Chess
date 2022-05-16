# CHESS GAME FEATURING
# ToDo: AI algorithm
# ToDo: voice assistant
# ToDo: create and store log.db for singleplayer (and maybe practice/multiplayer)
# MULTIPLAYER
# ToDo: disconnect, draw, resign (server&client)
# SERVER & CLIENT
# ToDo: self-calculating bytes amount for client and server
# APPLICATION
# ToDo: merge multiplayer and singleplayer clients to one (a lot of work)
# ToDo: configure toolbar/menubar (help, about, view(shortcuts), etc.)

from PyQt5.QtWidgets import QApplication
from Common.Application import Application
from sys import argv


if __name__ == '__main__':
    application: QApplication = QApplication(argv)
    app: Application = Application()
    application.exec()
