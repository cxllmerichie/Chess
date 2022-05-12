from PyQt5.QtCore import QSize, Qt
from PyQt5.QtWidgets import QLabel, QMessageBox, QMainWindow, QShortcut
from PyQt5.QtGui import QPixmap, QFont, QKeySequence, QResizeEvent, QIcon
from Common.Constants import BH, BW, SW, SH, MENU_BACKGROUND, GAME_BACKGROUND, FS, ICON
from Common.Library import app_btn, app_label, State, Text, clr, Status
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

        self.chessgame = MChessGame(self, '?')
        self.chessgame.move(int(self.width() / 2 - self.chessgame.width() / 2), int(self.height() / 2 - self.chessgame.height() / 2))
        self.state: State = State.Waiting
        self.status: str = Status.Menu.value

        self.background: QLabel = self.create_background()
        self.menu_buttons: list = self.menu_btns()
        self.shortcuts: list = self.create_shortcuts()
        self.information: dict = self.information_labels()

        self.setMinimumSize(self.chessgame.width(), self.chessgame.height())
        self.move(SW / 2 - self.width() / 2, SH / 2 - self.height() / 2)
        self.show_menu_buttons()
        self.showNormal()

    def set_status_bar(self):
        self.statusBar().setFont(QFont('Cambria', int(FS / 2)))
        self.statusBar().setStyleSheet('color: white')
        self.statusBar().showMessage(self.status)

    def information_labels(self) -> dict:
        return {
            'waiting': app_label(Text.Waiting.value, QSize(self.width(), self.height()), clr['waiting'], self),
            'opporesign': app_label(Text.OpponentResign.value, QSize(self.width(), self.height()), clr['opporesign'], self),
            'selfresign': app_label(Text.SelfResign.value, QSize(self.width(), self.height()), clr['selfresign'], self),
            'draw': app_label(Text.Draw.value, QSize(self.width(), self.height()), clr['draw'], self),
            'win': app_label(Text.Win.value, QSize(self.width(), self.height()), clr['win'], self),
            'defeat': app_label(Text.Defeat.value, QSize(self.width(), self.height()), clr['defeat'], self)
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
            app_btn('Play vs Player', (self.width() / 2 - BW / 2, self.height() / 2, BW, BH), lambda: self.multiplayer(), self),
            app_btn('Practice', (self.width() / 2 - BW / 2, self.height() / 2 + BH, BW, BH), lambda: self.singleplayer(), self),
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
        self.change_status_bar(Status.Menu.value)
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
            self.information[key] = app_label(previous_text, QSize(self.width(), self.height()), clr[key], self)
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
        self.menu_buttons[4].move(self.width() / 2 - BW / 2, self.height() / 2 + BH * 3)

    def create_background(self) -> QLabel:
        background = QLabel(self)
        background.resize(self.width(), self.height())
        background.setPixmap(QPixmap(self.wallpaper).scaled(self.width(), self.height()))
        return background

    def change_status_bar(self, status: str):
        self.status = status
        self.resizeEvent(QResizeEvent)

    def singleplayer(self):
        self.change_status_bar(Status.Practice.value)
        self.state = State.PracticeWithTime
        self.hide_menu_buttons()
        self.change_background(GAME_BACKGROUND)
        self.chessgame = SChessGame(self)
        self.chessgame.move(int(self.width() / 2 - self.chessgame.width() / 2), int(self.height() / 2 - self.chessgame.height() / 2))
        self.chessgame.show()
        self.chessgame.start_game()

    def multiplayer(self):
        try:
            client: Client = Client()
        except:
            print('[APPLICATION | CLIENT] ServerClient is down.\nThe connection was not established because the destination computer rejected the connection request.')
            return None
        self.state = State.Waiting
        self.show_waiting_screen()
        self.chessgame = MChessGame(self, client.receive()[10])
        self.chessgame.move(int(self.width() / 2 - self.chessgame.width() / 2), int(self.height() / 2 - self.chessgame.height() / 2))
        self.chessgame.show()
        start_new_thread(self.connect_to_server, (client, ))
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
        self.information['waiting'] = app_label(Text.Waiting.value, QSize(self.width(), self.height()), clr['waiting'], self)
        self.information['waiting'].show()

    def start_game(self):
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
            elif self.state is State.SuggestedDraw:
                network.send(SUGGESTDRAW)
            elif self.state is State.Finished:
                network.send(DISCONNECT)
            l: list = self.chessgame.chessgui.chess.last_move
            if self.chessgame.chessgui.color == 'w' and self.chessgame.chessgui.chess.chessboard[l[1][0]][l[1][1]][0] == self.chessgame.chessgui.color and not self.chessgame.chessgui.enable_mouse_click:
                self.hide_information()
                self.information['win'].show()
            elif self.state is not State.Resigned and self.chessgame.chessgui.color == 'b' and self.chessgame.chessgui.chess.chessboard[l[1][0]][l[1][1]][0] == self.chessgame.chessgui.color and not self.chessgame.chessgui.enable_mouse_click:
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
            elif reply == DISCONNECT:
                print('OPPONENT DISCONNECTED')
                self.chessgame.end_game()
                break
            elif reply == ACCEPTEDDRAW:
                print('OPPONENT ACCEPTED DRAW')
                self.chessgame.end_game()
                self.hide_information()
                self.information['draw'].show()
            op: list = reply.split(',')
            try:
                self.chessgame.chessgui.manual_interaction(int(op[0]), int(op[1]), int(op[2]), int(op[3]))
                if op[4] == 'R' and self.state is State.Waiting:
                    self.state = State.Started
                    self.start_game()
                elif op[4] == ' ' and self.state is State.Started:
                    self.return_to_menu_procedure()
                    break
                elif self.state is State.Resigned:
                    self.hide_information()
                    self.information['selfresign'].show()
                    self.chessgame.end_game()
                if self.state is State.Finished:
                    self.chessgame.end_game()
                    break
                if self.state == State.AcceptedDraw:
                    print('IT IS A DRAW')
                    self.hide_information()
                    self.information['draw'].show()
                    network.send(ACCEPTEDDRAW)
                    self.chessgame.end_game()
                    # break
            except ValueError or IndexError:
                print('[EXCEPTION] Exception from draw.')

    def create_shortcut(self, keys: str, function) -> QShortcut:
        shortcut: QShortcut = QShortcut(QKeySequence(keys), self)
        shortcut.activated.connect(lambda: function)
        return shortcut

    def create_shortcuts(self) -> tuple:
        # full screen
        full_screen_mode: QShortcut = QShortcut(QKeySequence('F11'), self)
        full_screen_mode.activated.connect(lambda: (self.showNormal() if self.isFullScreen() else (self.hide(), self.showFullScreen())))
        # close the application
        close_application: QShortcut = QShortcut(QKeySequence('Ctrl+E'), self)
        close_application.activated.connect(lambda: self.close())
        # return to menu
        return_to_menu: QShortcut = QShortcut(QKeySequence('Ctrl+M'), self)
        return_to_menu.activated.connect(lambda: self.return_to_menu())
        # enable/disable singleplayer timer
        enable_disable_singleplayer_timer: QShortcut = QShortcut(QKeySequence('Ctrl+T'), self)
        enable_disable_singleplayer_timer.activated.connect(lambda: self.timer_control())
        # volume up
        volume_up: QShortcut = QShortcut(QKeySequence(Qt.Key_Equal), self)
        volume_up.activated.connect(lambda: self.chessgame.chessgui.audio_player.setVolume(self.chessgame.chessgui.audio_player.volume() + 10))
        # volume down
        volume_down: QShortcut = QShortcut(QKeySequence(Qt.Key_Minus), self)
        volume_down.activated.connect(lambda: self.chessgame.chessgui.audio_player.setVolume(self.chessgame.chessgui.audio_player.volume() - 10))
        # volume mute
        volume_mute: QShortcut = QShortcut(QKeySequence('Ctrl+-'), self)
        volume_mute.activated.connect(lambda: self.chessgame.chessgui.audio_player.setVolume(0 if self.chessgame.chessgui.audio_player.volume() != 0 else 100))
        # show / hide hints on the left bottom corner
        show_hide_hints: QShortcut = QShortcut(QKeySequence('Ctrl+H'), self)
        show_hide_hints.activated.connect(lambda: (self.statusBar().hide() if self.statusBar().isVisible() else self.statusBar().show()))
        # resign
        resign: QShortcut = QShortcut(QKeySequence('Ctrl+R'), self)
        resign.activated.connect(lambda: self.end_game_message('Resignation', 'Do you want to resign?', State.Resigned))
        # draw
        draw: QShortcut = QShortcut(QKeySequence('Ctrl+D'), self)
        draw.activated.connect(lambda: self.suggest_draw())
        return full_screen_mode, close_application, return_to_menu, enable_disable_singleplayer_timer, volume_up, volume_down, volume_mute, show_hide_hints, resign, draw
