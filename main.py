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
#from Network import Network
from time import sleep


if __name__ == '__main__':
    #network = Network()

    app = QApplication(argv)
    white = Application()
    #white.update_game_state(network.get_game_state())

    """while True:
        sleep(0.5)
        black = network.send(white.chessgame)
        if not white.state:
            break"""

    app.exec()
