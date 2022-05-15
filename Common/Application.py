from PyQt5.QtCore import QSize, Qt
from PyQt5.QtWidgets import QLabel, QMessageBox, QMainWindow, QShortcut, QWidget, QCheckBox, QComboBox
from PyQt5.QtGui import QPixmap, QFont, QKeySequence, QResizeEvent, QIcon
from Common.Constants import BH, BW, SW, SH, MENU_BACKGROUND, GAME_BACKGROUND, FS, ICON, S, set_piece_style, set_chessboard_style, FRAMERATE
from Common.Library import app_btn, app_label, color, Status, State, Text
from ClientMultipalyer.ChessGame import ChessGame as MChessGame
from ClientSingleplayer.ChessGame import ChessGame as SChessGame
from ServerClient.config import DISCONNECT, RESIGN, SUGGESTDRAW, ACCEPTEDDRAW
from ServerClient.Client import Client
from _thread import start_new_thread
from contextlib import redirect_stdout
with redirect_stdout(None):
    from pygame.time import Clock
from os import listdir


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
        self.background.lower()
        self.menu_buttons: list = self.menu_btns()
        self.information: dict = self.information_labels()
        self.show_menu_buttons()

        self.setMinimumSize(S*10, S*10)
        self.move(SW / 2 - self.width() / 2, SH / 2 - self.height() / 2)
        self.shortcuts()
        self.settings: AHugeLie = AHugeLie(self)
        self.showNormal()

    def shortcut(self, keys: str, function) -> QShortcut:
        shortcut: QShortcut = QShortcut(QKeySequence(keys), self)
        shortcut.activated.connect(function)
        return shortcut

    def ctrl_r_shortcut(self):
        if self.state is State.PracticeWithTime or self.state is State.Practice or self.state is State.PracticeNoTime:
            self.chessgame.reset_game()
        elif self.state is State.Started:
            self.end_game_message('Resignation', 'Do you want to resign?', State.Resigned)

    def shortcuts(self):
        self.shortcut('F9', lambda: self.showNormal()),
        self.shortcut('F10', lambda: self.showMaximized()),
        self.shortcut('F11', lambda: self.showNormal() if self.isFullScreen() else (self.hide(), self.showFullScreen())),
        self.shortcut('Ctrl+E', lambda: self.close()),
        self.shortcut('Ctrl+M', lambda: self.return_to_menu()),
        self.shortcut('Ctrl+T', lambda: self.timer_control()),
        self.shortcut('=', lambda: self.chessgame.chessgui.audio_player.setVolume(self.chessgame.chessgui.audio_player.volume() + 10)),
        self.shortcut('-', lambda: self.chessgame.chessgui.audio_player.setVolume(self.chessgame.chessgui.audio_player.volume() - 10)),
        self.shortcut('Ctrl+-', lambda: self.chessgame.chessgui.audio_player.setVolume(0 if self.chessgame.chessgui.audio_player.volume() != 0 else 100)),
        self.shortcut('Ctrl+H', lambda: self.statusBar().hide() if self.statusBar().isVisible() else self.statusBar().show()),
        self.shortcut('Ctrl+R', lambda: self.ctrl_r_shortcut()),
        self.shortcut('Ctrl+D', lambda: self.suggest_draw())
        self.shortcut('Ctrl+S', lambda: self.settings.hide() if self.settings.isVisible() else self.settings.show())

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
            'disconnect': app_label(Text.OpponentDisconnect, QSize(self.width(), self.height()), color['disconnect'], self),
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
            app_btn('Play vs Player', (self.width() / 2 - BW / 2, self.height() / 2, BW, BH), lambda: self.gamemode_multiplayer(), self),
            app_btn('Practice', (self.width() / 2 - BW / 2, self.height() / 2 + BH, BW, BH), lambda: self.gamemode_practice(), self),
            app_btn('Settings', (self.width() / 2 - BW / 2, self.height() / 2 + BH * 2, BW, BH), lambda: self.settings.show(), self),
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
        self.state = State.SelfDisconnected
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
        self.settings.manual_resize(self.width(), self.height())

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

    def gamemode_practice(self):
        self.change_status_bar(Status.Practice)
        self.state = State.PracticeWithTime
        self.hide_menu_buttons()
        self.change_background(GAME_BACKGROUND)
        self.chessgame = SChessGame(self)
        self.chessgame.move(int(self.width() / 2 - self.chessgame.width() / 2), int(self.height() / 2 - self.chessgame.height() / 2))
        self.chessgame.show()
        self.chessgame.start_game()

    def gamemode_multiplayer(self):
        client: Client = Client()
        self.state = State.Waiting
        self.show_waiting_screen()
        self.chessgame = MChessGame(self, client.receive()[11])
        self.chessgame.move(int(self.width() / 2 - self.chessgame.width() / 2), int(self.height() / 2 - self.chessgame.height() / 2))
        self.chessgame.show()
        self.change_status_bar(Status.Multiplayer)
        start_new_thread(self.connect_to_server, (client, ))
        # Это просто пиздец а не костыль (строка 199 + строка 205): из-за того что подключение к серверу
        # вызвано в другом треде, при ручном вызове функции ресайза инфо-лейблов в треде с подключением,
        # фреймворк жалуется на то что родитель в другом треде,
        # но если заресайpить окно так как это обычно происходит после вызова этого треда сразу же,
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
        clock: Clock = Clock()
        while self.state is not State.Finished:
            clock.tick(FRAMERATE)
            # STATE control
            if self.state is State.Resigned:
                client.send(RESIGN)
                self.information['selfresign'].show()
                self.chessgame.end_game()
            elif self.state is State.SuggestedDraw:
                client.send(SUGGESTDRAW)
            elif self.state is State.SelfDisconnected:
                client.send(DISCONNECT)
                self.state = State.Finished
                self.chessgame.end_game()
            elif self.state == State.AcceptedDraw:
                print('IT IS A DRAW BY AGREEMENT')
                client.send(ACCEPTEDDRAW)
                self.state = State.Draw
                self.information['draw'].show()
                self.chessgame.end_game()
            l: list = self.chessgame.chessgui.chess.last_move
            data: str = f'{abs(7 - l[0][0])},{abs(7 - l[0][1])},{abs(7 - l[1][0])},{abs(7 - l[1][1])},{self.chessgame.chessgui.promoted[1]}'
            reply: str = client.send(data)
            # REPLY control
            if reply == DISCONNECT:
                self.state = State.OpponentDisconnected
                self.information['disconnect'].show()
                self.chessgame.end_game()
            if reply == RESIGN:
                print('OPPONENT RESIGNED')
                self.state = State.Won
                self.chessgame.end_game()
                self.information['opporesign'].show()
            elif reply == SUGGESTDRAW:
                print('OPPONENT SUGGESTED DRAW')
                self.end_game_message('Draw by agreement', 'Do you agree for a draw?', State.AcceptedDraw)
                if self.state == State.AcceptedDraw:
                    client.send(ACCEPTEDDRAW)
                    self.state = State.Draw
                    self.information['draw'].show()
            elif reply == ACCEPTEDDRAW:
                print('OPPONENT ACCEPTED DRAW')
                self.state = State.Draw
                self.chessgame.end_game()
                self.information['draw'].show()
            # WIN/LOSE control
            if not self.chessgame.chessgui.enable_mouse_click and self.state is State.Started:
                if self.chessgame.chessgui.color == 'w':
                    if self.chessgame.chessgui.chess.chessboard[l[1][0]][l[1][1]][0] == self.chessgame.chessgui.color:
                        self.information['win'].show()
                        self.state = State.Won
                    else:
                        self.information['defeat'].show()
                        self.state = State.Defeated
                elif self.chessgame.chessgui.color == 'b':
                    if self.chessgame.chessgui.chess.chessboard[l[1][0]][l[1][1]][0] != self.chessgame.chessgui.color:
                        self.information['win'].show()
                        self.state = State.Won
                    else:
                        self.information['defeat'].show()
                        self.state = State.Defeated
            # SYNCHRONIZE chessboard
            try:
                op: list = reply.split(',')
                self.chessgame.chessgui.manual_interaction(int(op[0]), int(op[1]), int(op[2]), int(op[3]), str(op[4]))
                if op[6] == 'R' and self.state is State.Waiting:
                    self.state = State.Started
                    self.start_multiplayer_game()
            except Exception as exception:
                print(f'[EXCEPTION] {self.state} Exception raised during synchronization.')
        self.hide_information()


class AHugeLie(QWidget):
    def __init__(self, parent: Application):
        super().__init__(parent=parent)
        self.parent: Application = parent
        self.setFixedSize(self.parent.width(), self.parent.height())
        self.background: QLabel = QLabel(self)
        self.background.resize(self.width(), self.height())
        self.background.setStyleSheet("background-color: rgba(46, 46, 46, 220);")
        self.settings: Settings = Settings(self)
        self.settings.show()
        self.hide()

    def manual_resize(self, width: int, height: int):
        self.setFixedSize(width, height)
        self.background.resize(width, height)
        self.settings.move(int(self.width()/2-self.settings.width()/2), int(self.height()/2-self.settings.height()/2))


class Settings(QWidget):
    def __init__(self, parent: AHugeLie):
        super().__init__(parent=parent)
        self.parent: AHugeLie = parent
        self.setMinimumSize(S*5, S*4)
        self.move(int(self.parent.width() / 2-self.width() / 2), S+ int(self.parent.height() / 2-self.height() / 2))
        self.hide()

        self.create_main_label()
        # self.checkbox: QCheckBox = self.create_checkbox()
        self.combobox_pieces: QComboBox = self.create_combobox('Pieces: ', 'Assets/Images/Pieces/', 0)
        self.combobox_pieces.currentTextChanged.connect(lambda: set_piece_style(self.combobox_pieces.currentText()))
        self.combobox_pieces.setCurrentText('standardhd')
        self.combobox_chessboard: QComboBox = self.create_combobox('Chessboard: ', 'Assets/Images/Chessboard/', self.combobox_pieces.height())
        self.combobox_chessboard.currentTextChanged.connect(lambda: set_chessboard_style(self.combobox_chessboard.currentText()))
        self.combobox_chessboard.setCurrentText('standard')

    def create_main_label(self):
        main: QLabel = QLabel(self)
        main.setText('Settings')
        main.setFont(QFont('Arial', FS*2))
        main.setStyleSheet('color: white;')
        main.show()
        main.move(self.width()/2-main.width()/2, S/4)
        message: QLabel = QLabel(self)
        message.setText('[press Ctrl+S to close settings menu]')
        message.setFont(QFont('Helvetica', 0.5*FS))
        # font = message.font()
        # message.setFont(font.setItalic(True))
        message.setStyleSheet('color: white;')
        message.show()
        message.move(self.width() / 2 - message.width() / 2, main.height()+message.height())

    def resizeEvent(self, event) -> None:
        self.move(int(self.parent.width() / 2-self.width() / 2), S+int(self.parent.height() / 2-self.height() / 2))

    def create_checkbox(self) -> QCheckBox:
        checkbox: QCheckBox = QCheckBox(parent=self)
        checkbox.setText('Show coordinates')
        checkbox.setFont(QFont('Arial', FS))
        checkbox.setStyleSheet('color: white;')
        checkbox.setWindowFlag(Qt.WindowStaysOnTopHint)
        checkbox.setLayoutDirection(Qt.RightToLeft)
        checkbox.move(0, self.height()/2-checkbox.height()/2)
        return checkbox

    def create_combobox(self, description: str, directory: str, height_shift: int) -> QComboBox:
        textlabel: QLabel = QLabel(self)
        textlabel.setText(description)
        textlabel.setFont(QFont('Arial', FS))
        textlabel.setStyleSheet('color: white;')
        textlabel.move(S/4, self.height() / 2 - textlabel.height() / 2 + height_shift)
        combobox: QComboBox = QComboBox(parent=self)
        combobox.setFont(QFont('Arial', 0.8*FS))
        combobox.setStyleSheet('color: black;')
        combobox.setWindowFlag(Qt.WindowStaysOnTopHint)
        combobox.setFixedSize(QSize(S*2, combobox.height()))
        combobox.move(self.width()-combobox.width()-0.25*S, self.height() / 2 - combobox.height() / 2 + height_shift)
        for folder in listdir(directory):
            combobox.addItem(folder)
        return combobox

    # show/hide coordinates
    # show/hide additional button (same as for shortcuts)
    # show/hide position indicator
    # turn on/off sound in the application
