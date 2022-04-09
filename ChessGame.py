from PyQt5.QtWidgets import QWidget, QLabel
from PyQt5.QtCore import QSize
from Library import S, FS
from ChessGUI import ChessGUI
from PyQt5.QtGui import QImage, QPalette, QBrush, QFont
from string import ascii_uppercase


class ChessGame(QWidget):
    def __init__(self, log_file):
        super(ChessGame, self).__init__()
        self.setWindowTitle('Chess')
        self.setFixedSize(QSize(S * 10, S * 10))
        img = QImage('Images/Standard/background.png').scaled(QSize(S*10, S*10))
        palette = QPalette()
        palette.setBrush(QPalette.Window, QBrush(img))
        self.setPalette(palette)

        self.coordinates()
        self.chessgui = ChessGUI(self, log_file)
        self.show()

    def coordinates(self):
        for number in range(1, 9, 1):
            label = QLabel(self)
            label.setText(str(ascii_uppercase[number-1]))
            label.move(number*S + S/2 - FS/3, S-1.5*FS)
            label.setFont(QFont('Arial', FS))
            label.setStyleSheet('color: gray')
            label.show()
        for number in range(1, 9, 1):
            label = QLabel(self)
            label.setText(str(ascii_uppercase[number-1]))
            label.move(number*S + S/2 - FS/3, S*9)
            label.setFont(QFont('Arial', FS))
            label.setStyleSheet('color: gray')
            label.show()


