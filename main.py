# ToDo: player1 & player2 control (sequence 1,2,1,2,1,2...)
# ToDo: AI algorithm
# ToDo: multiplayer protocol
# ToDo: vocal assistant
# ToDo: fix refactor check/checkmate/stalemate

from PyQt5.QtWidgets import QApplication
from ChessGUI import Window
from Library import time, date, line, duration
from timeit import default_timer
from sys import argv

if __name__ == '__main__':
    file = open('log.txt', "a")
    file.write(line(50))
    file.write('Start: ' + date() + ' ' + time() + '\n')
    start = default_timer()

    app = QApplication(argv)
    window = Window(file)
    window.installEventFilter(window)
    app.exec()

    end = default_timer()
    file.write('End: ' + date() + ' ' + time() + '\n')
    file.write('Duration: ' + duration(start, end) + '\n')
    file.write(line(50))
    file.close()
