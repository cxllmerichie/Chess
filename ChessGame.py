from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QMessageBox
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QFont
from Library import S, FS, new_palette, RetVal, str_time_to_float, text_label
from string import ascii_uppercase
from ChessGUI import ChessGUI
from threading import Thread
from time import sleep


class ChessGame(QWidget):
    def __init__(self, log_file):
        super(ChessGame, self).__init__()
        self.setWindowTitle('Chess')
        self.setFixedSize(QSize(S * 10, S * 10))
        self.setPalette(new_palette('background'))

        self.text_labels()
        self.buttons()

        self.timers: dict = {'w': Timer(text_label('10:00', Qt.AlignHCenter | Qt.AlignVCenter, (0, 0), QSize(S, S), self)),
                             'b': Timer(text_label('10:00', Qt.AlignHCenter | Qt.AlignVCenter, (S * 9, 0), QSize(S, S), self))}

        self.chessgui = ChessGUI(self, log_file)
        self.chessgui.installEventFilter(self.chessgui)
        self.show()
        self.timers['w'].start()

    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Exit', 'Close the application?', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.end_game()
            event.accept()
        else:
            event.ignore()

    def text_labels(self):
        for i in range(1, 9, 1):
            text_label(str(ascii_uppercase[i - 1]), Qt.AlignHCenter | Qt.AlignBottom, (i * S, 0), QSize(S, S), self)#.show()
            text_label(str(ascii_uppercase[i - 1]), Qt.AlignHCenter | Qt.AlignTop, (S * i, S * 9), QSize(S, S), self)#.show()
            text_label(str(9 - i), Qt.AlignVCenter | Qt.AlignLeft, (S * 9 + 0.1 * S, S * i), QSize(0.9 * S, S), self)#.show()
            text_label(str(9 - i), Qt.AlignVCenter | Qt.AlignRight, (0, S * i), QSize(0.9 * S, S), self)#.show()

    def button(self, title: str, geometry: tuple, click) -> QPushButton:
        button = QPushButton(title, self)
        button.setGeometry(geometry[0], geometry[1], geometry[2], geometry[3])
        button.setFont(QFont('Arial', FS / 2))
        button.setStyleSheet('background: #323232')
        button.clicked.connect(click)
        return button

    def buttons(self):
        self.button('Draw by agreement', (S, S * 9 + S / 2, S * 2, S / 4),
                    lambda: self.end_game_message(QMessageBox.Question, 'Draw by agreement', 'Do you agree for a draw?'))#.show()
        self.button('Resign', (S, S * 9 + S / 2 + S / 4, S * 2, S / 4),
                    lambda: self.end_game_message(QMessageBox.Warning, 'Resignation', 'Do you want to resign?'))#.show()
        self.button('VolumeUp', (S * 9, S * 9 + S / 4, S, S / 4),
                    lambda: self.chessgui.player.setVolume(self.chessgui.player.volume() + 10))#.show()
        self.button('VolumeDown', (S * 9, S * 10 - S / 2, S, S / 4),
                    lambda: self.chessgui.player.setVolume(self.chessgui.player.volume() - 10))#.show()
        self.button('Mute', (S * 9, S * 10 - S / 4, S, S / 4),
                    lambda: self.chessgui.player.setVolume(0 if self.chessgui.player.volume() != 0 else 100))#.show()

    def end_game_message(self, icon_type, title: str, text: str) -> None:
        msg = QMessageBox()
        msg.setIcon(icon_type)
        msg.setText(text)
        msg.setWindowTitle(title)
        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        if msg.exec_() == RetVal.Yes.value:
            self.end_game()

    def end_game(self):
        self.chessgui.enable_mouse_click = False
        self.timers['w'].stop()
        self.timers['b'].stop()


class Timer:
    def __init__(self, label: QLabel):
        self.label: QLabel = label
        self.time: str = '10:00:00'
        self.status: bool = False
        self.thread: Thread = Thread(target=lambda: self.countdown(amount=str_time_to_float(self.time), label=self.label))

    def countdown(self, amount: float = 600, label: QLabel = None) -> None:
        period: float = 0.5
        displayable_characters: int = 5
        while amount > 0 and self.status:
            minutes, seconds_milliseconds = divmod(amount, 60)
            seconds, milliseconds = divmod(seconds_milliseconds, 1)
            label.setText('{:02.0f}:{:02.0f}.{:02.0f}'.format(minutes, seconds, milliseconds * 1000)[:displayable_characters])
            sleep(period)
            amount -= period

    def start(self):
        if not self.status:
            self.status = True
            self.thread.start()

    def stop(self):
        if self.status:
            self.status = False
            self.thread.join()

    def pause(self):
        self.time = self.label.text()
        self.stop()

    def resume(self):
        if not self.status:
            self.thread: Thread = Thread(target=lambda: self.countdown(amount=str_time_to_float(self.time), label=self.label))
        self.start()
