from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QMessageBox, QMainWindow
from PyQt5.QtGui import QPixmap, QFont
from Constants import BH, BW, SW, SH, BACKGROUND, FS
from Library import new_button
from ChessGame import ChessGame


class Application(QMainWindow):
    background: QLabel
    singleplayer: QPushButton
    multiplayer: QPushButton
    settings: QPushButton
    exit: QPushButton

    def __init__(self, log_file):
        super().__init__()
        self.setWindowTitle('Chess')

        self.set_background()
        self.create_buttons()
        self.set_status_bar()

        self.chessgame: QWidget = ChessGame(self, log_file)
        self.chessgame.move(self.width() / 2 - self.chessgame.width() / 2,
                            self.height() / 2 - self.chessgame.height() / 2)

        self.setMinimumSize(self.chessgame.width(), self.chessgame.height())
        self.move(SW / 2 - self.width() / 2, SH / 2 - self.height() / 2)
        self.showNormal()

    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Exit', 'Close the application?', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.chessgame.end_game()

    def set_status_bar(self):
        self.statusBar().setFont(QFont('Arial', int(FS / 2)))
        self.statusBar().setStyleSheet('color: white')
        self.statusBar().showMessage('Press F11 to enter fullscreen mode')

    def set_background(self):
        self.background = QLabel(self)
        self.background.resize(self.width(), self.height())
        self.background.setPixmap(QPixmap(BACKGROUND).scaled(self.width(), self.height()))

    def start_game(self):
        self.statusBar().hide()
        self.hide_buttons()
        self.chessgame.show()
        self.chessgame.start_game()

    def hide_buttons(self):
        self.singleplayer.hide()
        self.multiplayer.hide()
        self.settings.hide()
        self.exit.hide()

    def show_buttons(self):
        self.singleplayer.show()
        self.multiplayer.show()
        self.settings.show()
        self.exit.show()

    def resize_buttons(self):
        self.singleplayer.move(self.width() / 2 - 100, self.height() / 2 - 50)
        self.multiplayer.move(self.width() / 2 - 100, self.height() / 2)
        self.settings.move(self.width() / 2 - 100, self.height() / 2 + BH)
        self.exit.move(self.width() / 2 - 100, self.height() / 2 + BH * 2)

    def resizeEvent(self, event):
        self.resize_buttons()
        self.chessgame.move(self.width() / 2 - self.chessgame.width() / 2,
                            self.height() / 2 - self.chessgame.height() / 2)
        self.background.setPixmap(QPixmap(BACKGROUND).scaled(self.width(), self.height()))
        self.background.resize(self.width(), self.height())

    def create_buttons(self):
        self.singleplayer = new_button('Play vs Computer', (self.width() / 2 - 100, self.height() / 2 - BH, BW, BH),
                                       lambda: None, self)
        self.multiplayer = new_button('Play vs Player', (self.width() / 2 - 100, self.height() / 2, BW, BH),
                                      lambda: self.start_game(), self)
        self.settings = new_button('Settings', (self.width() / 2 - 100, self.height() / 2 + BH, BW, BH),
                                   lambda: None, self)
        self.exit = new_button('Exit', (self.width() / 2 - 100, self.height() / 2 + BH * 2, BW, BH),
                               lambda: None, self)
