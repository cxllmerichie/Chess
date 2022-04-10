from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QMessageBox
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QFont
from Library import S, FS, new_palette, RetVal
from string import ascii_uppercase
from ChessGUI import ChessGUI


class ChessGame(QWidget):
    def __init__(self, log_file):
        super(ChessGame, self).__init__()
        self.setWindowTitle('Chess')
        self.setFixedSize(QSize(S * 10, S * 10))
        self.setPalette(new_palette('background'))

        self.hints()
        self.chessgui = ChessGUI(self, log_file)
        self.chessgui.installEventFilter(self.chessgui)
        self.show()

        self.buttons()

    def hint(self, symbol: str, alignment, position: tuple) -> QLabel:
        label = QLabel(self)
        label.setText(symbol)
        label.setFixedSize(QSize(S, S))
        label.setAlignment(alignment)
        label.setFont(QFont('Arial', FS))
        label.setStyleSheet('color: gray')
        label.move(position[0], position[1])
        return label

    def hints(self):
        for i in range(1, 9, 1):
            self.hint(str(ascii_uppercase[i-1]), Qt.AlignHCenter | Qt.AlignBottom, (i*S, 0)).show()
            self.hint(str(ascii_uppercase[i-1]), Qt.AlignHCenter | Qt.AlignTop, (S*i, S*9)).show()
            self.hint(str(9-i), Qt.AlignVCenter | Qt.AlignLeft, (S*9, S*i)).show()
            self.hint(str(9-i), Qt.AlignVCenter | Qt.AlignRight, (0, S*i)).show()

    def button(self, title: str, geometry: tuple, click) -> QPushButton:
        button = QPushButton(title, self)
        button.setGeometry(geometry[0], geometry[1], geometry[2], geometry[3])
        button.setFont(QFont('Arial', FS / 2))
        button.setStyleSheet('background: #323232')
        button.clicked.connect(click)
        return button

    def buttons(self):
        self.button("Draw by agreement", (S, S*9+S/2, S*2, S/4),
                    lambda: self.message(QMessageBox.Question, "Draw by agreement", "Do you agree for a draw?")
                    ).show()
        self.button("Resign", (S*7, S * 9 + S / 2, S * 2, S / 4),
                    lambda: self.message(QMessageBox.Warning, "Resignation", "Do you want to resign?")
                    ).show()

    def message(self, icon_type, title: str, text: str):
        msg = QMessageBox()
        msg.setIcon(icon_type)
        msg.setText(text)
        msg.setWindowTitle(title)
        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        if msg.exec_() == RetVal.Yes.value:
            self.chessgui.enable_mouse_click = False
