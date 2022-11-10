# CHESS GAME FEATURING
# ToDo: AI algorithm
# ToDo: voice assistant
# ToDo: create and store log.db for singleplayer (and maybe practice/multiplayer)
# MULTIPLAYER
# ToDo: modify practice_movetracker for multiplayer (currently show incorrect data)
# ToDo: disconnect, draw, resign (server&client)
# SERVER & CLIENT
# ToDo: self-calculating bytes amount for client and server
# APPLICATION
# ToDo: merge multiplayer and singleplayer clients to one (a lot of work)
# ToDo: animation: pieces, end-game (after merging)
# ToDo: configure toolbar/menubar (help, about, view(shortcuts), etc.)

from PyQt5.QtWidgets import QApplication
from src.Common.Application import Application
from sys import argv


if __name__ == '__main__':
    application: QApplication = QApplication(argv)
    app: Application = Application()
    application.exec()
