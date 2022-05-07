# ToDo: AI algorithm
# ToDo: multiplayer protocol
# ToDo: voice assistant
# ToDo: winner / loser to log.txt
# ToDo: log.txt to db
# ToDo: promotion disables mouse click to avoid unnecessary click but it stops timers
# ToDo: en passant position should be marked as capturing but not position

from PyQt5.QtWidgets import QApplication
from Application import Application
from sys import argv
from _thread import start_new_thread
from Server import server_startup


if __name__ == '__main__':
    start_new_thread(server_startup, ())

    app = QApplication(argv)
    application = Application()
    app.exec()
