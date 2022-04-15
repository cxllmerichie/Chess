from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QMessageBox
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QFont
from Library import S, FS, new_palette, RetVal, countdown
from string import ascii_uppercase
from ChessGUI import ChessGUI
from threading import Thread


class ChessGame(QWidget):
    def __init__(self, log_file):
        super(ChessGame, self).__init__()
        self.setWindowTitle('Chess')
        self.setFixedSize(QSize(S * 10, S * 10))
        self.setPalette(new_palette('background'))

        self.hints()
        self.buttons()

        self.chessgui = ChessGUI(self, log_file)
        self.chessgui.installEventFilter(self.chessgui)
        self.show()

        # Timers
        self.white_timer = self.hint("00:00", Qt.AlignHCenter | Qt.AlignVCenter, (0, 0), QSize(S, S))
        self.black_timer = self.hint("00:00", Qt.AlignHCenter | Qt.AlignVCenter, (S * 9, 0), QSize(S, S))
        self.white_timer.show()
        self.black_timer.show()
        self.timer()

    def hint(self, symbol: str, alignment, position: tuple, size: QSize) -> QLabel:
        label = QLabel(self)
        label.setText(symbol)
        label.setFixedSize(size)
        label.setAlignment(alignment)
        label.setFont(QFont('Arial', FS))
        label.setStyleSheet('color: gray')
        label.move(position[0], position[1])
        return label

    def hints(self):
        for i in range(1, 9, 1):
            self.hint(str(ascii_uppercase[i - 1]), Qt.AlignHCenter | Qt.AlignBottom, (i * S, 0), QSize(S, S)).show()
            self.hint(str(ascii_uppercase[i - 1]), Qt.AlignHCenter | Qt.AlignTop, (S * i, S * 9), QSize(S, S)).show()
            self.hint(str(9 - i), Qt.AlignVCenter | Qt.AlignLeft, (S * 9 + 0.1 * S, S * i), QSize(0.9 * S, S)).show()
            self.hint(str(9 - i), Qt.AlignVCenter | Qt.AlignRight, (0, S * i), QSize(0.9 * S, S)).show()

    def button(self, title: str, geometry: tuple, click) -> QPushButton:
        button = QPushButton(title, self)
        button.setGeometry(geometry[0], geometry[1], geometry[2], geometry[3])
        button.setFont(QFont('Arial', FS / 2))
        button.setStyleSheet('background: #323232')
        button.clicked.connect(click)
        return button

    def buttons(self):
        self.button('Draw by agreement', (S, S * 9 + S / 2, S * 2, S / 4),
                    lambda: self.message(QMessageBox.Question, "Draw by agreement", "Do you agree for a draw?")).show()
        self.button('Resign', (S, S * 9 + S / 2 + S / 4, S * 2, S / 4),
                    lambda: self.message(QMessageBox.Warning, "Resignation", "Do you want to resign?")).show()
        self.button('VolumeUp', (S * 9, S * 9 + S / 4, S, S / 4),
                    lambda: self.chessgui.player.setVolume(self.chessgui.player.volume() + 10)).show()
        self.button('VolumeDown', (S * 9, S * 10 - S / 2, S, S / 4),
                    lambda: self.chessgui.player.setVolume(self.chessgui.player.volume() - 10)).show()
        self.button('Mute', (S * 9, S * 10 - S / 4, S, S / 4),
                    lambda: self.chessgui.player.setVolume(0 if self.chessgui.player.volume() != 0 else 100)).show()

    def message(self, icon_type, title: str, text: str) -> None:
        msg = QMessageBox()
        msg.setIcon(icon_type)
        msg.setText(text)
        msg.setWindowTitle(title)
        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        if msg.exec_() == RetVal.Yes.value:
            self.chessgui.enable_mouse_click = False

    def timer(self) -> None:
        Thread(target=lambda: countdown(amount=600, label=self.white_timer)).start()
        Thread(target=lambda: countdown(amount=600, label=self.black_timer)).start()
