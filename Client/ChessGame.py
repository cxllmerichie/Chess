from PyQt5.QtWidgets import QWidget, QLabel
from PyQt5.QtCore import QSize, Qt
from Client.Library import str_time_to_float, text_label
from Client.Constants import TICK_PERIOD, GAME_TIME, S, TIME_FORMAT
from string import ascii_uppercase
from Client.ChessGUI import ChessGUI
from threading import Thread
from time import sleep


class ChessGame(QWidget):
    def __init__(self, parent: QWidget, color: str):
        super().__init__(parent=parent)
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setFixedSize(QSize(S * 10, S * 10))
        self.color: str = color
        self.text_labels()
        self.timers: dict = {'w': Timer(text_label(GAME_TIME, Qt.AlignHCenter | Qt.AlignBottom, (S * 4, S * 9), QSize(S * 2, S), self)),
                             'b': Timer(text_label(GAME_TIME, Qt.AlignHCenter | Qt.AlignTop, (S * 4, 0), QSize(S * 2, S), self))}
        self.chessgui: ChessGUI = ChessGUI(self, self.color)
        self.chessgui.installEventFilter(self.chessgui)
        self.hide()

    def closeEvent(self, event):
        self.end_game()
        event.accept()

    def start_game(self):
        Thread(target=lambda: self.timer_control()).start()

    def timer_control(self):
        while self.chessgui.enable_mouse_click and str_time_to_float(self.timers['b'].time) > 0 and str_time_to_float(self.timers['w'].time) > 0:
            if self.color == 'w' and self.chessgui.chess.chessboard[self.chessgui.chess.last_move[1][0]][self.chessgui.chess.last_move[1][1]][0] == 'b':
                self.timers['b'].pause()
                self.timers['w'].resume()
            elif self.color == 'b' and self.chessgui.chess.chessboard[self.chessgui.chess.last_move[1][0]][self.chessgui.chess.last_move[1][1]][0] == 'b':
                self.timers['w'].pause()
                self.timers['b'].resume()
            sleep(TICK_PERIOD / 2)
        self.end_game()

    def text_labels(self):
        for i in range(1, 9, 1):
            letter: str = str(ascii_uppercase[i - 1]) if self.color == 'w' else str(ascii_uppercase[8-i])
            text_label(letter, Qt.AlignHCenter | Qt.AlignBottom, (i * S, 0), QSize(S, S), self)
            text_label(letter, Qt.AlignHCenter | Qt.AlignTop, (S * i, S * 9), QSize(S, S), self)
            digit: str = str(9 - i) if self.color == 'w' else str(i)
            text_label(digit, Qt.AlignVCenter | Qt.AlignLeft, (S * 9 + 0.1 * S, S * i), QSize(0.9 * S, S), self)
            text_label(digit, Qt.AlignVCenter | Qt.AlignRight, (0, S * i), QSize(0.9 * S, S), self)

    def end_game(self):
        self.chessgui.enable_mouse_click = False
        self.timers['w'].stop()
        self.timers['b'].stop()


class Timer:
    def __init__(self, label: QLabel):
        self.label: QLabel = label
        self.time: str = label.text()
        self.status: bool = False
        self.thread: Thread = Thread(target=lambda: self.countdown(amount=str_time_to_float(self.time)))

    def countdown(self, amount: float = 600) -> None:
        while amount > 0 and self.status:
            minutes, seconds_milliseconds = divmod(amount, 60)
            seconds, milliseconds = divmod(seconds_milliseconds, 1)
            self.label.setText('{:02.0f}:{:02.0f}.{:02.0f}'.format(minutes, seconds, milliseconds * 1000)[:TIME_FORMAT])
            sleep(TICK_PERIOD)
            amount -= TICK_PERIOD
            if amount <= 0:
                self.label.setText('00:00.00')
                self.time = '00:00.00'
                self.stop()

    def start(self):
        if not self.status:
            self.status = True
            self.thread.start()

    def stop(self):
        if self.status:
            self.status = False
            try:
                self.thread.join()
            except RuntimeError:
                pass

    def pause(self):
        self.time = self.label.text()
        self.stop()

    def resume(self):
        if not self.status:
            self.thread: Thread = Thread(target=lambda: self.countdown(amount=str_time_to_float(self.time)))
        self.start()
