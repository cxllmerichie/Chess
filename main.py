# ToDo: AI algorithm
# ToDo: multiplayer protocol
# ToDo: voice assistant
# ToDo: winner / loser to log.txt
# ToDo: log.txt to db

from PyQt5.QtWidgets import QApplication
from Application import Application
from sys import argv


if __name__ == '__main__':
    app = QApplication(argv)
    window = Application()
    app.exec()
