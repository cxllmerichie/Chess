# ToDo: AI algorithm
# ToDo: multiplayer protocol
# ToDo: voice assistant
# ToDo: main window
# ToDo: winner / loser to log.txt
# ToDo: log.txt to db

from PyQt5.QtWidgets import QApplication
from ChessGame import ChessGame
from Library import time, date, line, duration
from timeit import default_timer
from sys import argv


if __name__ == '__main__':
    file = open('log.txt', "a")
    file.write(line(50))
    file.write(f'Start: {date()} {time()}\n')
    start = default_timer()

    app = QApplication(argv)
    window = ChessGame(file)
    app.exec()

    end = default_timer()
    file.write(f'End: {date()} {time()}\n')
    file.write(f'Duration: {duration(start, end)}\n')
    file.write(line(50))
    file.close()
