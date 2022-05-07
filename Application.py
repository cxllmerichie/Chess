from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import QLabel, QMessageBox, QMainWindow, QShortcut
from PyQt5.QtGui import QPixmap, QFont, QKeySequence
from Constants import BH, BW, SW, SH, MENU_BACKGROUND, GAME_BACKGROUND, FS, S
from Library import app_btn, awaiting_label, State  # , time, date, line, duration
from ChessGame import ChessGame
# from timeit import default_timer
from Server import Network
from _thread import start_new_thread
from contextlib import redirect_stdout
with redirect_stdout(None):
    from pygame.time import Clock
from time import sleep


class Application(QMainWindow):
    wallpaper: str = MENU_BACKGROUND
    background: QLabel
    singleplayer, multiplayer, settings, exit = None, None, None, None  # QPushButton
    full_screen_mode, close_application, back_to_menu = None, None, None  # QShortcut
    # log = open('log.txt', "a")

    def __init__(self):
        super().__init__()
        self.setWindowTitle('Chess (Pre-Alpha)')

        self.chessgame = ChessGame(self)
        self.chessgame.move(int(self.width() / 2 - self.chessgame.width() / 2), int(self.height() / 2 - self.chessgame.height() / 2))
        self.multiplayer_state: State = State.Waiting

        self.set_background()
        self.create_buttons()
        self.set_status_bar()
        self.set_shortcuts()

        self.setMinimumSize(S*10, S*10)
        self.move(SW / 2 - self.width() / 2, SH / 2 - self.height() / 2)
        self.awaiting: QLabel = awaiting_label(QSize(self.width(), self.height()), self)

        self.showNormal()

    """def start_log(self):
        global start
        self.log.write(line(50))
        self.log.write(f'Start: {date()} {time()}\n')
        start = default_timer()"""

    """def end_log(self):
        global end
        end = default_timer()
        self.log.write(f'End: {date()} {time()}\n')
        self.log.write(f'Duration: {duration(start, end)}\n')
        self.log.write(line(50))"""

    def set_shortcuts(self):
        self.full_screen_mode = QShortcut(QKeySequence('F11'), self)
        self.full_screen_mode.activated.connect(lambda: self.go_full_screen_mode())

        self.close_application = QShortcut(QKeySequence('Ctrl+E'), self)
        self.close_application.activated.connect(lambda: self.close())

        self.back_to_menu = QShortcut(QKeySequence('Ctrl+M'), self)
        self.back_to_menu.activated.connect(lambda: self.go_back_to_menu())

    def go_back_to_menu_procedure(self):
        # self.end_log()
        self.chessgame.close()
        self.wallpaper = MENU_BACKGROUND
        self.resize_background()
        self.statusBar().show()
        self.show_buttons()

    def go_back_to_menu(self, with_reply: bool = True):
        if with_reply:
            if self.wallpaper != MENU_BACKGROUND:
                reply = QMessageBox.question(self, 'Menu', 'Return to menu?', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
                if reply == QMessageBox.Yes:
                    self.go_back_to_menu_procedure()
        else:
            self.go_back_to_menu_procedure()

    def go_full_screen_mode(self):
        self.showNormal() if self.isFullScreen() else self.showFullScreen()

    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Exit', 'Close the application?', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            if self.chessgame is not None:
                self.chessgame.end_game()
                self.go_back_to_menu(False)
                # self.log.close()
            event.accept()
        else:
            event.ignore()

    def resizeEvent(self, event):
        self.resize_buttons()
        self.resize_awaiting()
        if self.chessgame is not None:
            self.chessgame.move(int(self.width() / 2 - self.chessgame.width() / 2), int(self.height() / 2 - self.chessgame.height() / 2))
        self.resize_background()

    def resize_awaiting(self):
        was_visible: bool = self.awaiting.isVisible()
        self.awaiting.hide()
        self.awaiting = awaiting_label(QSize(self.width(), self.height()), self)
        if was_visible:
            self.awaiting.show()

    def set_status_bar(self):
        self.statusBar().setFont(QFont('Arial', int(FS / 2)))
        self.statusBar().setStyleSheet('color: white')
        self.statusBar().showMessage('Press F11 to enter fullscreen mode')

    def resize_background(self):
        self.background.setPixmap(QPixmap(self.wallpaper).scaled(self.width(), self.height()))
        self.background.resize(self.width(), self.height())

    def set_background(self):
        self.background = QLabel(self)
        self.background.resize(self.width(), self.height())
        self.background.setPixmap(QPixmap(self.wallpaper).scaled(self.width(), self.height()))

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
        self.singleplayer.move(self.width() / 2 - BW/2, self.height() / 2 - BH)
        self.multiplayer.move(self.width() / 2 - BW/2, self.height() / 2)
        self.settings.move(self.width() / 2 - BW/2, self.height() / 2 + BH)
        self.exit.move(self.width() / 2 - BW/2, self.height() / 2 + BH * 2)

    def create_buttons(self):
        self.singleplayer = app_btn('Play vs Computer', (self.width() / 2 - BW / 2, self.height() / 2 - BH, BW, BH), lambda: None, self)
        self.multiplayer = app_btn('Play vs Player', (self.width() / 2 - BW / 2, self.height() / 2, BW, BH), lambda: self.multiplayer_game(), self)
        self.settings = app_btn('Settings', (self.width() / 2 - BW / 2, self.height() / 2 + BH, BW, BH), lambda: None, self)
        self.exit = app_btn('Exit', (self.width() / 2 - BW / 2, self.height() / 2 + BH * 2, BW, BH), lambda: self.close(), self)

    def multiplayer_game(self):
        self.show_awaiting_screen()
        start_new_thread(self.connect_to_server, ())
        start_new_thread(self.start_game, ())

    def show_awaiting_screen(self):
        self.wallpaper = GAME_BACKGROUND
        self.resize_background()
        self.statusBar().hide()
        self.hide_buttons()
        self.new_game()
        self.chessgame.show()
        self.awaiting = awaiting_label(QSize(self.width(), self.height()), self)
        self.awaiting.show()

    def start_game(self):
        while True:
            if self.multiplayer_state is State.Started:
                break
        self.awaiting.hide()
        self.chessgame.start_game()

    def new_game(self):
        # self.start_log()
        # self.chessgame = ChessGame(self, self.log)
        self.chessgame = ChessGame(self)
        self.chessgame.move(int(self.width() / 2 - self.chessgame.width() / 2), int(self.height() / 2 - self.chessgame.height() / 2))

    def connect_to_server(self):
        fps: Clock = Clock()
        network: Network = Network()
        while True:
            fps.tick(1)
            me: str = network.receive()

            opponent: str = network.send(network.receive())
            print(me)
            #print(sent)
            if opponent[0] == 'R' and self.multiplayer_state is not State.Started:
                self.multiplayer_state = State.Started
