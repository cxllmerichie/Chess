from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QMessageBox
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QFont
from Library import S, FS, new_palette, RetVal, time_to_int, text_label
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
        self.timers['w'].start()
        self.timers['b'].start()

        self.chessgui = ChessGUI(self, log_file)
        self.chessgui.installEventFilter(self.chessgui)
        self.show()

    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Exit', 'Close the application?',
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.timers['w'].stop()
            self.timers['b'].stop()
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
                    lambda: self.message(QMessageBox.Question, 'Draw by agreement', 'Do you agree for a draw?'))#.show()
        self.button('Resign', (S, S * 9 + S / 2 + S / 4, S * 2, S / 4),
                    lambda: self.message(QMessageBox.Warning, 'Resignation', 'Do you want to resign?'))#.show()
        self.button('VolumeUp', (S * 9, S * 9 + S / 4, S, S / 4),
                    lambda: self.chessgui.player.setVolume(self.chessgui.player.volume() + 10))#.show()
        self.button('VolumeDown', (S * 9, S * 10 - S / 2, S, S / 4),
                    lambda: self.chessgui.player.setVolume(self.chessgui.player.volume() - 10))#.show()
        self.button('Mute', (S * 9, S * 10 - S / 4, S, S / 4),
                    lambda: self.chessgui.player.setVolume(0 if self.chessgui.player.volume() != 0 else 100))#.show()

        # Timer
        self.button('Pause', (S * 3, S * 9 + S / 2, S, S / 2),
                    lambda: (self.timers['w'].pause(), self.timers['b'].pause())
                    )#.show()
        self.button('Resume', (S * 4, S * 9 + S / 2, S, S / 2),
                    lambda: (self.timers['w'].resume(), self.timers['b'].resume())
                    )#.show()

    def message(self, icon_type, title: str, text: str) -> None:
        msg = QMessageBox()
        msg.setIcon(icon_type)
        msg.setText(text)
        msg.setWindowTitle(title)
        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        if msg.exec_() == RetVal.Yes.value:
            self.chessgui.enable_mouse_click = False


class Timer:
    def __init__(self, label: QLabel):
        self.label: QLabel = label
        self.time: str = '10:00'
        self.status: bool = True
        self.thread: Thread = Thread(target=lambda: self.countdown(amount=time_to_int(self.time), label=self.label))

    def countdown(self, amount: int = 600, label: QLabel = None) -> None:
        while amount:
            if not self.status:
                break
            minutes, seconds = divmod(amount, 60)
            timer: str = '{:02d}:{:02d}'.format(minutes, seconds)
            label.setText(timer)
            sleep(1)
            amount -= 1

    def start(self):
        self.thread.start()

    def stop(self):
        self.status = False
        self.thread.join()

    def pause(self):
        self.time = self.label.text()
        self.status = False
        self.thread.join()

    def resume(self):
        self.thread: Thread = Thread(target=lambda: self.countdown(amount=time_to_int(self.time), label=self.label))
        self.status: bool = True
        self.start()
