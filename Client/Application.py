from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import QLabel, QMessageBox, QMainWindow, QShortcut
from PyQt5.QtGui import QPixmap, QFont, QKeySequence, QResizeEvent
from Client.Constants import BH, BW, SW, SH, MENU_BACKGROUND, GAME_BACKGROUND, FS, S
from Client.Library import app_btn, game_btn, app_label, State, Info
from Client.ChessGame import ChessGame
from Server.config import DISCONNECT, RESIGN, SUGGESTDRAW, ACCEPTEDDRAW
from Client.Client import Client
from _thread import start_new_thread
from contextlib import redirect_stdout
with redirect_stdout(None):
    from pygame.time import Clock


class Application(QMainWindow):
    wallpaper: str = MENU_BACKGROUND

    def __init__(self):
        super().__init__()
        self.setWindowTitle('Chess (Pre-Alpha)')
        self.set_status_bar()

        self.chessgame: ChessGame = ChessGame(self, '?')
        self.multiplayer_state: State = State.Waiting

        self.background: QLabel = self.create_background()
        self.menu_buttons: list = self.menu_btns()
        self.game_buttons: list = self.game_btns()
        self.shortcut_full_screen, self.shortcut_close_application, self.shortcut_return_to_menu = self.shortcuts()
        self.information: dict = self.information_labels()

        self.setMinimumSize(self.chessgame.width(), self.chessgame.height())
        self.move(SW / 2 - self.width() / 2, SH / 2 - self.height() / 2)
        self.showNormal()

    def information_labels(self) -> dict:
        return {
            'waiting': app_label(Info.Waiting.value, QSize(self.width(), self.height()), self),
            'resign': app_label(Info.Resign.value, QSize(self.width(), self.height()), self),
            'draw': app_label(Info.Draw.value, QSize(self.width(), self.height()), self),
            'win': app_label(Info.Win.value, QSize(self.width(), self.height()), self),
            'defeat': app_label(Info.Defeat.value, QSize(self.width(), self.height()), self)
        }

    def show_information(self):
        for key in self.information:
            self.information[key].show()

    def hide_information(self):
        for key in self.information:
            self.information[key].hide()

    def menu_btns(self) -> list:
        return [
            app_btn('Play vs Computer', (self.width() / 2 - BW / 2, self.height() / 2 - BH, BW, BH), lambda: None, self),
            app_btn('Play vs Player', (self.width() / 2 - BW / 2, self.height() / 2, BW, BH), lambda: self.multiplayer_game(), self),
            app_btn('Settings', (self.width() / 2 - BW / 2, self.height() / 2 + BH, BW, BH), lambda: None, self),
            app_btn('Exit', (self.width() / 2 - BW / 2, self.height() / 2 + BH * 2, BW, BH), lambda: self.close(), self)
        ]

    def hide_menu_buttons(self):
        for button in self.menu_buttons:
            button.hide()

    def show_menu_buttons(self):
        for button in self.menu_buttons:
            button.show()

    def game_btns(self) -> list:
        return [
            game_btn('Draw by agreement', (S, S * 9 + S / 2, S * 2, S / 4),
                     lambda: self.suggest_draw(), self),
            game_btn('Resign', (S, S * 9 + S / 2 + S / 4, S * 2, S / 4),
                     lambda: self.end_game_message(QMessageBox.Warning, 'Resignation', 'Do you want to resign?', State.Resigned), self),
            game_btn('VolumeUp', (S * 9, S * 9 + S / 4, S, S / 4),
                     lambda: self.chessgame.chessgui.audio_player.setVolume(self.chessgui.audio_player.volume() + 10), self),
            game_btn('VolumeDown', (S * 9, S * 10 - S / 2, S, S / 4),
                     lambda: self.chessgame.chessgui.audio_player.setVolume(self.chessgui.audio_player.volume() - 10), self),
            game_btn('Mute', (S * 9, S * 10 - S / 4, S, S / 4),
                     lambda: self.chessgame.chessgui.audio_player.setVolume(0 if self.chessgui.audio_player.volume() != 0 else 100), self)
        ]

    def hide_game_buttons(self):
        for button in self.game_buttons:
            button.hide()

    def show_game_buttons(self):
        for button in self.game_buttons:
            button.show()

    def suggest_draw(self):
        self.multiplayer_state = State.SuggestedDraw

    def end_game_message(self, icon_type, title: str, text: str, state: State) -> None:
        msg = QMessageBox()
        msg.setIcon(icon_type)
        msg.setText(text)
        msg.setWindowTitle(title)
        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        if msg.exec_() == QMessageBox.Yes:
            self.multiplayer_state = state
            self.chessgame.end_game()

    def shortcuts(self) -> tuple:
        # full screen
        full_screen_mode: QShortcut = QShortcut(QKeySequence('F11'), self)
        full_screen_mode.activated.connect(lambda: (self.showNormal() if self.isFullScreen() else self.showFullScreen()))
        # close the application
        close_application: QShortcut = QShortcut(QKeySequence('Ctrl+E'), self)
        close_application.activated.connect(lambda: self.close())
        # return to menu
        return_to_menu: QShortcut = QShortcut(QKeySequence('Ctrl+M'), self)
        return_to_menu.activated.connect(lambda: self.return_to_menu())
        return full_screen_mode, close_application, return_to_menu

    def return_to_menu_procedure(self):
        self.multiplayer_state = State.Finished
        self.hide_game_buttons()
        self.hide_information()
        self.chessgame.close()
        self.change_background(MENU_BACKGROUND)
        self.statusBar().show()
        self.show_menu_buttons()

    def change_background(self, background: str):
        self.wallpaper = background
        self.resize_background()

    def return_to_menu(self, with_reply: bool = True):
        if with_reply:
            if self.wallpaper != MENU_BACKGROUND:
                if self.message_box_reply('Menu', 'Return to menu?') == QMessageBox.Yes:
                    self.return_to_menu_procedure()
        else:
            self.return_to_menu_procedure()

    def message_box_reply(self, title: str, question: str):
        return QMessageBox.question(self, title, question, QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

    # @DECORATOR
    def closeEvent(self, event):
        if self.message_box_reply('Exit', 'Close the application?') == QMessageBox.Yes:
            self.chessgame.end_game()
            self.return_to_menu(False)
            event.accept()
        else:
            event.ignore()

    # @DECORATOR
    def resizeEvent(self, event):
        self.resize_buttons()
        self.resize_information()
        self.chessgame.move(int(self.width() / 2 - self.chessgame.width() / 2), int(self.height() / 2 - self.chessgame.height() / 2))
        self.resize_buttons()
        self.resize_background()

    def resize_information(self):
        for key in self.information:
            was_visible: bool = self.information[key].isVisible()
            previous_text: str = self.information[key].text()
            self.information[key].hide()
            self.information[key] = app_label(previous_text, QSize(self.width(), self.height()), self)
            if was_visible:
                self.information[key].show()

    def resize_background(self):
        self.background.setPixmap(QPixmap(self.wallpaper).scaled(self.width(), self.height()))
        self.background.resize(self.width(), self.height())

    def resize_buttons(self):
        # menu buttons
        self.menu_buttons[0].move(self.width() / 2 - BW / 2, self.height() / 2 - BH)
        self.menu_buttons[1].move(self.width() / 2 - BW / 2, self.height() / 2)
        self.menu_buttons[2].move(self.width() / 2 - BW / 2, self.height() / 2 + BH)
        self.menu_buttons[3].move(self.width() / 2 - BW / 2, self.height() / 2 + BH * 2)
        # game buttons
        self.game_buttons[0].move(self.chessgame.x() + S, self.chessgame.y() + S * 10 + S / 2)
        self.game_buttons[1].move(self.chessgame.x() + S, self.chessgame.y() + S * 10 + S / 2 + S / 4)
        self.game_buttons[2].move(self.chessgame.x() + S * 8, self.chessgame.y() + S * 10 + S / 4)
        self.game_buttons[3].move(self.chessgame.x() + S * 8, self.chessgame.y() + S * 11 - S / 2)
        self.game_buttons[4].move(self.chessgame.x() + S * 8, self.chessgame.y() + S * 11 - S / 4)

    def set_status_bar(self):
        self.statusBar().setFont(QFont('Arial', int(FS / 2)))
        self.statusBar().setStyleSheet('color: white')
        self.statusBar().showMessage('Press F11 to enter fullscreen mode')

    def create_background(self) -> QLabel:
        background = QLabel(self)
        background.resize(self.width(), self.height())
        background.setPixmap(QPixmap(self.wallpaper).scaled(self.width(), self.height()))
        return background

    def multiplayer_game(self):
        self.multiplayer_state = State.Waiting
        self.show_waiting_screen()
        network: Client = Client()
        color = network.receive()[10]
        self.chessgame = ChessGame(self, color)
        self.chessgame.move(int(self.width() / 2 - self.chessgame.width() / 2), int(self.height() / 2 - self.chessgame.height() / 2))
        self.chessgame.show()
        del network
        start_new_thread(self.connect_to_server, ())
        # Это просто пиздец а не костыль (строка 199 + строка 205): из-за того что подключение к серверу
        # вызвано в другом треде, при ручном вызове функции ресайза инфо-лейблов в треде с подключением,
        # фреймворк жалуеться на то что родитель в другом треде,
        # но если заресайтить окно так как это обычно происходит после вызова этого треда сразу же,
        # он как-то идентифицирует тред и показывает инфо лейб корректно без доп. ресайза после
        self.resizeEvent(QResizeEvent)

    def show_waiting_screen(self):
        self.statusBar().hide()
        self.hide_menu_buttons()
        self.change_background(GAME_BACKGROUND)
        self.information['waiting'] = app_label(Info.Waiting.value, QSize(self.width(), self.height()), self)
        self.information['waiting'].show()

    def start_game(self):
        self.information['waiting'].hide()
        self.chessgame.start_game()
        self.show_game_buttons()

    def connect_to_server(self):
        fps: Clock = Clock()
        network: Client = Client()
        self.chessgame.chessgui.color = network.receive()[10]
        while True:
            fps.tick(200)
            if self.multiplayer_state is State.Resigned:
                network.send(RESIGN)
            elif self.multiplayer_state is State.SuggestedDraw:
                network.send(SUGGESTDRAW)
            elif self.multiplayer_state is State.Finished:
                network.send(DISCONNECT)
            l: list = self.chessgame.chessgui.chess.last_move
            reply: str = network.send(f'{abs(7-l[0][0])},{abs(7-l[0][1])},{abs(7-l[1][0])},{abs(7-l[1][1])}, , ')
            if reply == RESIGN:
                print('OPPONENT RESIGNED')
                self.chessgame.end_game()
                self.information['resign'].show()
                break
            elif reply == SUGGESTDRAW:
                print('OPPONENT SUGGEST DRAW')
                self.end_game_message(QMessageBox.Question, 'Draw by agreement', 'Do you agree for a draw?', State.AcceptedDraw)
                if self.multiplayer_state == State.AcceptedDraw:
                    self.multiplayer_state = State.AcceptedDraw
                    network.send(ACCEPTEDDRAW)
                    self.information['draw'].show()
                    break
            elif reply == DISCONNECT:
                print('OPPONENT DISCONNECTED')
                self.chessgame.end_game()
                break
            elif reply == ACCEPTEDDRAW:
                print('OPPONENT ACCEPTED DRAW')
                self.chessgame.end_game()
                self.information['draw'].show()
            op: list = reply.split(',')
            try:
                self.chessgame.chessgui.manual_interaction(int(op[0]), int(op[1]), int(op[2]), int(op[3]))
                if op[4] == 'R' and self.multiplayer_state is State.Waiting:
                    self.multiplayer_state = State.Started
                    self.start_game()
                elif op[4] == ' ' and self.multiplayer_state is State.Started:
                    self.return_to_menu_procedure()
                    break
                if self.multiplayer_state == State.AcceptedDraw:
                    print('IT IS A DRAW')
                    network.send(ACCEPTEDDRAW)
                    self.chessgame.end_game()
                    break
            except ValueError or IndexError:
                print('Draw works properly')
