from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import QLabel, QMessageBox, QMainWindow, QShortcut
from PyQt5.QtGui import QPixmap, QFont, QKeySequence, QResizeEvent, QIcon
from Common.Constants import BH, BW, SW, SH, MENU_BACKGROUND, GAME_BACKGROUND, FS, ICON
from Common.Library import app_btn, app_label, color, Status, State, Text
from ClientMultipalyer.ChessGame import ChessGame as MChessGame
from ClientSingleplayer.ChessGame import ChessGame as SChessGame
from ServerClient.config import DISCONNECT, RESIGN, SUGGESTDRAW, ACCEPTEDDRAW
from ServerClient.Client import Client
from _thread import start_new_thread
from contextlib import redirect_stdout
with redirect_stdout(None):
    from pygame.time import Clock


class Application(QMainWindow):
    wallpaper: str = MENU_BACKGROUND

    def __init__(self):
        super().__init__()
        self.setWindowTitle('Chess (Pre-Alpha)')
        self.setWindowIcon(QIcon(ICON))

        self.chessgame = SChessGame(self)
        self.chessgame.move(int(self.width() / 2 - self.chessgame.width() / 2), int(self.height() / 2 - self.chessgame.height() / 2))
        self.state: State = State.NoState
        self.status: str = Status.Menu

        self.background: QLabel = self.create_background()
        self.menu_buttons: list = self.menu_btns()
        self.information: dict = self.information_labels()
        self.show_menu_buttons()

        self.setMinimumSize(self.chessgame.width(), self.chessgame.height())
        self.move(SW / 2 - self.width() / 2, SH / 2 - self.height() / 2)
        self.shortcuts()
        self.showNormal()

    def set_status_bar(self):
        self.statusBar().setFont(QFont('Cambria', int(FS / 2)))
        self.statusBar().setStyleSheet('color: white')
        self.statusBar().showMessage(self.status)

    def information_labels(self) -> dict:
        return {
            'waiting': app_label(Text.Waiting, QSize(self.width(), self.height()), color['waiting'], self),
            'opporesign': app_label(Text.OpponentResign, QSize(self.width(), self.height()), color['opporesign'], self),
            'selfresign': app_label(Text.SelfResign, QSize(self.width(), self.height()), color['selfresign'], self),
            'draw': app_label(Text.Draw, QSize(self.width(), self.height()), color['draw'], self),
            'win': app_label(Text.Win, QSize(self.width(), self.height()), color['win'], self),
            'defeat': app_label(Text.Defeat, QSize(self.width(), self.height()), color['defeat'], self)
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
            app_btn('Play vs Player', (self.width() / 2 - BW / 2, self.height() / 2, BW, BH), lambda: self.multiplayer_mode(), self),
            app_btn('Practice', (self.width() / 2 - BW / 2, self.height() / 2 + BH, BW, BH), lambda: self.practice_mode(), self),
            app_btn('Settings', (self.width() / 2 - BW / 2, self.height() / 2 + BH * 2, BW, BH), lambda: None, self),
            app_btn('Exit', (self.width() / 2 - BW / 2, self.height() / 2 + BH * 3, BW, BH), lambda: self.close(), self)
        ]

    def hide_menu_buttons(self):
        for button in self.menu_buttons:
            button.hide()

    def show_menu_buttons(self):
        for button in self.menu_buttons:
            button.show()

    def suggest_draw(self):
        self.state = State.SuggestedDraw

    def timer_control(self):
        if self.state is State.PracticeWithTime:
            self.chessgame.disable_timers()
            self.state = State.PracticeNoTime
        elif self.state is State.PracticeNoTime:
            self.chessgame.enable_timers()
            self.state = State.PracticeWithTime

    def return_to_menu_procedure(self):
        self.hide_information()
        self.change_status_bar(Status.Menu)
        self.hide_information()
        self.state = State.Finished
        self.chessgame.close()
        self.change_background(MENU_BACKGROUND)
        self.statusBar().show()
        self.show_menu_buttons()

    def change_background(self, background: str):
        self.wallpaper = background
        self.resize_background()

    def return_to_menu(self):
        if self.wallpaper != MENU_BACKGROUND:
            if self.message_box_reply('Menu', 'Return to menu?') == QMessageBox.Yes:
                self.return_to_menu_procedure()

    def message_box_reply(self, title: str, question: str):
        return QMessageBox().question(self, title, question, QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

    def end_game_message(self, title: str, question: str, state: State):
        if self.message_box_reply(title, question) == QMessageBox.Yes:
            self.state = state
            self.chessgame.end_game()

    # @DECORATOR
    def closeEvent(self, event):
        if self.message_box_reply('Exit', 'Close the application?') == QMessageBox.Yes:
            self.chessgame.end_game()
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
        self.set_status_bar()

    def resize_information(self):
        for key in self.information:
            was_visible: bool = self.information[key].isVisible()
            previous_text: str = self.information[key].text()
            self.information[key].hide()
            self.information[key] = app_label(previous_text, QSize(self.width(), self.height()), color[key], self)
            if was_visible:
                self.information[key].show()

    def resize_background(self):
        self.background.setPixmap(QPixmap(self.wallpaper).scaled(self.width(), self.height()))
        self.background.resize(self.width(), self.height())

    def resize_buttons(self):
        self.menu_buttons[0].move(self.width() / 2 - BW / 2, self.height() / 2 - BH)
        self.menu_buttons[1].move(self.width() / 2 - BW / 2, self.height() / 2)
        self.menu_buttons[2].move(self.width() / 2 - BW / 2, self.height() / 2 + BH)
        self.menu_buttons[3].move(self.width() / 2 - BW / 2, self.height() / 2 + BH * 2)
        self.menu_buttons[4].move(self.width() / 2 - BW / 2, self.height() / 2 + BH * 3)

    def create_background(self) -> QLabel:
        background = QLabel(self)
        background.resize(self.width(), self.height())
        background.setPixmap(QPixmap(self.wallpaper).scaled(self.width(), self.height()))
        return background

    def change_status_bar(self, status: str):
        self.status = status
        self.resizeEvent(QResizeEvent)

    def practice_mode(self):
        self.change_status_bar(Status.Practice)
        self.state = State.PracticeWithTime
        self.hide_menu_buttons()
        self.change_background(GAME_BACKGROUND)
        self.chessgame = SChessGame(self)
        self.chessgame.move(int(self.width() / 2 - self.chessgame.width() / 2), int(self.height() / 2 - self.chessgame.height() / 2))
        self.chessgame.show()
        self.chessgame.start_game()

    def multiplayer_mode(self):
        client: Client = Client()
        self.state = State.Waiting
        self.show_waiting_screen()
        self.chessgame = MChessGame(self, client.receive()[10])
        self.chessgame.move(int(self.width() / 2 - self.chessgame.width() / 2), int(self.height() / 2 - self.chessgame.height() / 2))
        self.chessgame.show()
        self.change_status_bar(Status.Multiplayer)
        start_new_thread(self.connect_to_server, (client, ))
        # Это просто пиздец а не костыль (строка 199 + строка 205): из-за того что подключение к серверу
        # вызвано в другом треде, при ручном вызове функции ресайза инфо-лейблов в треде с подключением,
        # фреймворк жалуеться на то что родитель в другом треде,
        # но если заресайтить окно так как это обычно происходит после вызова этого треда сразу же,
        # он как-то идентифицирует тред и показывает инфо лейб корректно без доп. ресайза после
        self.resizeEvent(QResizeEvent)

    def show_waiting_screen(self):
        self.hide_menu_buttons()
        self.change_background(GAME_BACKGROUND)
        self.information['waiting'].show()

    def start_multiplayer_game(self):
        self.information['waiting'].hide()
        self.chessgame.start_game()

    def connect_to_server(self, client: Client):
        fps: Clock = Clock()
        network: Client = client
        self.chessgame.chessgui.color = network.receive()[10]
        while True:
            fps.tick(200)
            if self.state is State.Resigned:
                network.send(RESIGN)
                self.hide_information()
                self.information['selfresign'].show()
                self.chessgame.end_game()
            elif self.state is State.SuggestedDraw:
                network.send(SUGGESTDRAW)
            elif self.state is State.Finished:
                network.send(DISCONNECT)
                self.chessgame.end_game()
                break
            l: list = self.chessgame.chessgui.chess.last_move
            # win / lose messages
            if self.chessgame.chessgui.color == 'w' and self.chessgame.chessgui.chess.chessboard[l[1][0]][l[1][1]][0] == self.chessgame.chessgui.color and not self.chessgame.chessgui.enable_mouse_click:
                self.hide_information()
                self.information['win'].show()
            elif self.chessgame.chessgui.color == 'b' and self.chessgame.chessgui.chess.chessboard[l[1][0]][l[1][1]][0] == self.chessgame.chessgui.color and not self.chessgame.chessgui.enable_mouse_click:
                self.hide_information()
                self.information['defeat'].show()
            elif self.chessgame.chessgui.color == 'b' and self.chessgame.chessgui.chess.chessboard[l[1][0]][l[1][1]][0] != self.chessgame.chessgui.color and not self.chessgame.chessgui.enable_mouse_click:
                self.hide_information()
                self.information['win'].show()
            elif self.chessgame.chessgui.color == 'w' and self.chessgame.chessgui.chess.chessboard[l[1][0]][l[1][1]][0] != self.chessgame.chessgui.color and not self.chessgame.chessgui.enable_mouse_click:
                self.hide_information()
                self.information['defeat'].show()
            reply: str = network.send(f'{abs(7-l[0][0])},{abs(7-l[0][1])},{abs(7-l[1][0])},{abs(7-l[1][1])}, , ')
            if reply == RESIGN:
                print('OPPONENT RESIGNED')
                self.chessgame.end_game()
                self.information['opporesign'].show()
                break
            elif reply == SUGGESTDRAW:
                print('OPPONENT SUGGEST DRAW')
                self.resizeEvent(QResizeEvent)
                self.end_game_message('Draw by agreement', 'Do you agree for a draw?', State.AcceptedDraw)
                self.resizeEvent(QResizeEvent)
                if self.state == State.AcceptedDraw:
                    self.state = State.AcceptedDraw
                    network.send(ACCEPTEDDRAW)
                    self.hide_information()
                    self.information['draw'].show()
                    break
            elif reply == ACCEPTEDDRAW:
                print('OPPONENT ACCEPTED DRAW')
                self.chessgame.end_game()
                self.hide_information()
                self.information['draw'].show()
            try:
                op: list = reply.split(',')
                self.chessgame.chessgui.manual_interaction(int(op[0]), int(op[1]), int(op[2]), int(op[3]))
                if op[4] == 'R' and self.state is State.Waiting:
                    self.state = State.Started
                    self.start_multiplayer_game()
                elif op[4] == ' ' and self.state is State.Started:
                    self.return_to_menu_procedure()
                    break
                if self.state == State.AcceptedDraw:
                    print('IT IS A DRAW')
                    self.hide_information()
                    self.information['draw'].show()
                    network.send(ACCEPTEDDRAW)
                    self.chessgame.end_game()
                    # break
            except Exception:
                print('[EXCEPTION] Exception from DRAW or RESIGN.')
        if self.state is State.Resigned:
            self.hide_information()

    def shortcut(self, keys: str, function) -> QShortcut:
        shortcut: QShortcut = QShortcut(QKeySequence(keys), self)
        shortcut.activated.connect(function)
        return shortcut

    def shortcuts(self):
        self.shortcut('F11', (lambda: self.showNormal() if self.isFullScreen() else (self.hide(), self.showFullScreen()))),
        self.shortcut('Ctrl+E', lambda: self.close()),
        self.shortcut('Ctrl+M', lambda: self.return_to_menu()),
        self.shortcut('Ctrl+T', lambda: self.timer_control()),
        self.shortcut('=', lambda: self.chessgame.chessgui.audio_player.setVolume(self.chessgame.chessgui.audio_player.volume() + 10)),
        self.shortcut('-', lambda: self.chessgame.chessgui.audio_player.setVolume(self.chessgame.chessgui.audio_player.volume() - 10)),
        self.shortcut('Ctrl+-', lambda: self.chessgame.chessgui.audio_player.setVolume(0 if self.chessgame.chessgui.audio_player.volume() != 0 else 100)),
        self.shortcut('Ctrl+H', lambda: (self.statusBar().hide() if self.statusBar().isVisible() else self.statusBar().show())),
        self.shortcut('Ctrl+R', lambda: self.end_game_message('Resignation', 'Do you want to resign?', State.Resigned)),
        self.shortcut('Ctrl+D', lambda: self.suggest_draw())
