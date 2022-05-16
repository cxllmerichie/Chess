from PyQt5.QtCore import QSize, Qt
from PyQt5.QtWidgets import QLabel, QMessageBox, QMainWindow, QShortcut, QWidget, QCheckBox, QComboBox, QLineEdit, QPushButton
from PyQt5.QtGui import QPixmap, QFont, QKeySequence, QResizeEvent, QIcon, QIntValidator
from Common.Constants import BH, BW, SW, SH, MENU_BACKGROUND, GAME_BACKGROUND, FS, ICON, S, FRAMERATE
from Common.Library import app_btn, app_label, color, Hint, State, StateText, ScreenState, set_pieces, set_chessboard
from ClientMultipalyer.ChessGame import ChessGame as MChessGame
from ClientSingleplayer.ChessGame import ChessGame as SChessGame
from ServerClient.Client import Client, set_ip, set_port
from _thread import start_new_thread
from contextlib import redirect_stdout
with redirect_stdout(None):
    from pygame.time import Clock
from os import listdir
from time import sleep
from sys import exit


class Application(QMainWindow):
    wallpaper: str = MENU_BACKGROUND

    def __init__(self):
        super().__init__()
        self.setWindowTitle('Chess (Alpha v.1.0.2)')
        self.setWindowIcon(QIcon(ICON))

        self.chessgame = SChessGame(self)
        self.state: State = State.NoState
        self.hint: str = Hint.Menu
        self.clock: Clock = Clock()

        self.background: QLabel = self.create_background()
        self.menu_buttons: list = self.create_menu_buttons()
        self.information: dict = self.create_information()
        self.show_menu_buttons()
        self.shortcuts()

        self.setMinimumSize(S*10, S*10)
        self.move(SW / 2 - self.width() / 2, SH / 2 - self.height() / 2)
        self.settings: TransparentScreen = TransparentScreen(self)
        self.last_screen_state: ScreenState = ScreenState.Normal
        self.showNormal()

    # BACKGROUND
    def create_background(self) -> QLabel:
        background = QLabel(self)
        background.resize(self.width(), self.height())
        background.setPixmap(QPixmap(self.wallpaper).scaled(self.width(), self.height()))
        background.lower()
        return background

    def change_background(self, background: str) -> None:
        self.wallpaper = background
        self.resize_background()

    def resize_background(self) -> None:
        self.background.setPixmap(QPixmap(self.wallpaper).scaled(self.width(), self.height()))
        self.background.resize(self.width(), self.height())

    # SHORTCUTS
    def shortcut(self, keys: str, function) -> QShortcut:
        shortcut: QShortcut = QShortcut(QKeySequence(keys), self)
        shortcut.activated.connect(function)
        return shortcut

    def shortcuts(self) -> None:
        self.shortcut('F9', lambda: self.f9()),
        self.shortcut('F10', lambda: self.f10()),
        self.shortcut('F11', lambda: self.f11()),
        self.shortcut('Ctrl+E', lambda: self.close()),
        self.shortcut('Ctrl+M', lambda: self.return_to_menu()),
        self.shortcut('Ctrl+T', lambda: self.timer_control()),
        self.shortcut('=', lambda: self.chessgame.chessgui.audio_player.setVolume(self.chessgame.chessgui.audio_player.volume() + 10)),
        self.shortcut('-', lambda: self.chessgame.chessgui.audio_player.setVolume(self.chessgame.chessgui.audio_player.volume() - 10)),
        self.shortcut('Ctrl+-', lambda: self.chessgame.chessgui.audio_player.setVolume(0 if self.chessgame.chessgui.audio_player.volume() != 0 else 100)),
        self.shortcut('Ctrl+H', lambda: self.statusBar().hide() if self.statusBar().isVisible() else self.statusBar().show()),
        self.shortcut('Ctrl+R', lambda: self.ctrl_r()),
        self.shortcut('Ctrl+D', lambda: self.suggest_draw())
        self.shortcut('Ctrl+S', lambda: self.ctrl_s())

    def ctrl_s(self):
        if self.settings.isVisible():
            self.settings.settings.save()
            self.settings.hide()
        else:
            self.settings.show()

    def f9(self) -> None:
        self.showNormal()
        self.last_screen_state = ScreenState.Normal

    def f10(self) -> None:
        self.showMaximized()
        self.last_screen_state = ScreenState.Maximized

    def f11(self) -> None:
        if not self.isFullScreen():
            self.showFullScreen()
        elif self.last_screen_state is ScreenState.Normal:
            self.showNormal()
        elif self.last_screen_state is ScreenState.Maximized:
            self.f10()

    def ctrl_r(self) -> None:
        if self.state is State.PracticeWithTime or self.state is State.PracticeNoTime:
            self.chessgame.reset_game()
        if self.state is State.Started:
            if self.message_box_reply('Resignation', 'Do you want to resign?', True) == QMessageBox.Yes:
                self.state = State.Defeated

    # STATUS BAR (HINT)
    def change_status_bar(self, status: str) -> None:
        self.hint = status
        self.resizeEvent(QResizeEvent)

    def set_status_bar(self) -> None:
        self.statusBar().setFont(QFont('Cambria', int(FS / 2)))
        self.statusBar().setStyleSheet('color: white')
        self.statusBar().showMessage(self.hint)

    # INFORMATION LABELS
    def create_information(self) -> dict:
        return {
            'waiting': app_label(StateText.Waiting, QSize(self.width(), self.height()), color['waiting'], self),
            'opporesign': app_label(StateText.OppoResign, QSize(self.width(), self.height()), color['opporesign'], self),
            'selfresign': app_label(StateText.SelfResign, QSize(self.width(), self.height()), color['selfresign'], self),
            'draw': app_label(StateText.Draw, QSize(self.width(), self.height()), color['draw'], self),
            'disconnect': app_label(StateText.OppoDisconnect, QSize(self.width(), self.height()), color['disconnect'], self),
            'win': app_label(StateText.Win, QSize(self.width(), self.height()), color['win'], self),
            'defeat': app_label(StateText.Defeat, QSize(self.width(), self.height()), color['defeat'], self),
            'connectionerror': app_label(StateText.ServerConnectError, QSize(self.width(), self.height()), color['connectionerror'], self)
        }

    def resize_information(self) -> None:
        for key in self.information:
            was_visible: bool = self.information[key].isVisible()
            previous_text: str = self.information[key].text()
            self.information[key].hide()
            self.information[key] = app_label(previous_text, QSize(self.width(), self.height()), color[key], self)
            if was_visible:
                self.information[key].show()

    def show_information(self) -> None:
        for key in self.information:
            self.information[key].show()

    def hide_information(self) -> None:
        for key in self.information:
            self.information[key].hide()

    # MENU
    def return_to_menu_procedure(self) -> None:
        self.settings.hide()
        self.hide_information()
        self.change_status_bar(Hint.Menu)
        self.hide_information()
        self.state = State.NoState
        self.chessgame.close()
        self.change_background(MENU_BACKGROUND)
        self.statusBar().show()
        self.show_menu_buttons()

    def return_to_menu(self) -> None:
        if self.wallpaper != MENU_BACKGROUND:
            if self.message_box_reply('Menu', 'Return to menu?', True) == QMessageBox.Yes:
                self.return_to_menu_procedure()

    # MENU BUTTONS
    def create_menu_buttons(self) -> list:
        return [
            app_btn('Play vs Computer', (self.width() / 2 - BW / 2, self.height() / 2 - BH, BW, BH), lambda: None, self),
            app_btn('Play vs Player', (self.width() / 2 - BW / 2, self.height() / 2, BW, BH), lambda: self.gamemode_multiplayer(), self),
            app_btn('Practice', (self.width() / 2 - BW / 2, self.height() / 2 + BH, BW, BH), lambda: self.gamemode_practice(), self),
            app_btn('Settings', (self.width() / 2 - BW / 2, self.height() / 2 + BH * 2, BW, BH), lambda: self.settings.show(), self),
            app_btn('Exit', (self.width() / 2 - BW / 2, self.height() / 2 + BH * 3, BW, BH), lambda: exit(), self)
        ]

    def resize_menu_buttons(self) -> None:
        self.menu_buttons[0].move(self.width() / 2 - BW / 2, self.height() / 2 - BH)
        self.menu_buttons[1].move(self.width() / 2 - BW / 2, self.height() / 2)
        self.menu_buttons[2].move(self.width() / 2 - BW / 2, self.height() / 2 + BH)
        self.menu_buttons[3].move(self.width() / 2 - BW / 2, self.height() / 2 + BH * 2)
        self.menu_buttons[4].move(self.width() / 2 - BW / 2, self.height() / 2 + BH * 3)

    def hide_menu_buttons(self) -> None:
        for button in self.menu_buttons:
            button.hide()

    def show_menu_buttons(self) -> None:
        for button in self.menu_buttons:
            button.show()

    # GAMEMODES
    def gamemode_practice(self) -> None:
        self.change_status_bar(Hint.Practice)
        self.state = State.PracticeWithTime
        self.hide_menu_buttons()
        self.change_background(GAME_BACKGROUND)
        self.chessgame = SChessGame(self)
        self.chessgame.move(int(self.width() / 2 - self.chessgame.width() / 2), int(self.height() / 2 - self.chessgame.height() / 2))
        self.chessgame.show()
        self.chessgame.start_game()

    def connection_error(self, screen):
        sleep(3)
        self.information['connectionerror'].hide()
        screen.hide()

    def gamemode_multiplayer(self) -> None:
        try:
            client: Client = Client()
        except Exception:
            screen = TransparentScreen(self, False)
            self.information['connectionerror'] = app_label(StateText.ServerConnectError, QSize(self.width(), self.height()), color['connectionerror'], self)
            screen.show()
            self.information['connectionerror'].show()
            start_new_thread(self.connection_error, (screen, ))
            return None
        self.state = State.Waiting
        self.show_waiting_screen()
        self.chessgame = MChessGame(self, client.receive()[11])
        self.chessgame.move(int(self.width() / 2 - self.chessgame.width() / 2), int(self.height() / 2 - self.chessgame.height() / 2))
        self.chessgame.show()
        self.change_status_bar(Hint.Multiplayer)
        start_new_thread(self.connect_to_server, (client, ))
        # ВНИМАНИЕ, КОСТЫЛЬ
        self.resizeEvent(QResizeEvent)

    # @DECORATOR
    def closeEvent(self, event):
        if self.message_box_reply('Exit', 'Close the application?', True) == QMessageBox.Yes:
            self.chessgame.end_game()
            event.accept()
        else:
            event.ignore()

    # @DECORATOR
    def resizeEvent(self, event):
        self.resize_menu_buttons()
        self.resize_background()
        self.chessgame.move(int(self.width() / 2 - self.chessgame.width() / 2), int(self.height() / 2 - self.chessgame.height() / 2))
        self.set_status_bar()
        self.resize_information()
        self.settings.resizeEvent(QResizeEvent)

    # PRACTICE PROCEDURES
    def timer_control(self) -> None:
        if self.state is State.PracticeWithTime:
            self.chessgame.disable_timers()
            self.state = State.PracticeNoTime
        elif self.state is State.PracticeNoTime:
            self.chessgame.enable_timers()
            self.state = State.PracticeWithTime

    # MULTIPLAYER PROCEDURES
    def suggest_draw(self) -> None:
        self.state = State.SuggestedDraw

    def show_waiting_screen(self) -> None:
        self.hide_menu_buttons()
        self.change_background(GAME_BACKGROUND)
        self.information['waiting'].show()

    def start_multiplayer_game(self) -> None:
        self.information['waiting'].hide()
        self.chessgame.start_game()

    def message_box_reply(self, title: str, question: str, asking: bool):
        if asking:
            return QMessageBox().question(self, title, question, QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        return QMessageBox.Yes

    def connect_to_server(self, client: Client) -> None:
        while self.state is State.Waiting or self.state is State.Started:
            self.clock.tick(FRAMERATE)
            l: list = self.chessgame.chessgui.chess.last_move
            addon: str = '  '
            if self.chessgame.chessgui.promoted[0] and self.chessgame.chessgui.promoted[1] == '  ':
                addon = 'TT'
            elif self.chessgame.chessgui.promoted[0] and self.chessgame.chessgui.promoted[1] != '  ':
                addon = self.chessgame.chessgui.promoted[1]
                self.chessgame.chessgui.promoted = [False, '  ']
            data: str = f'{abs(7 - l[0][0])},{abs(7 - l[0][1])},{abs(7 - l[1][0])},{abs(7 - l[1][1])},{addon}'
            reply: str = client.send(data)
            # WIN/LOSE control
            if not self.chessgame.chessgui.enable_mouse_click and self.state is State.Started:
                if self.chessgame.chessgui.color == 'w':
                    self.state = State.Won if self.chessgame.chessgui.chess.chessboard[l[1][0]][l[1][1]][0] == self.chessgame.chessgui.color else State.Defeated
                elif self.chessgame.chessgui.color == 'b':
                    self.state = State.Won if self.chessgame.chessgui.chess.chessboard[l[1][0]][l[1][1]][0] != self.chessgame.chessgui.color else State.Defeated
                self.chessgame.end_game()
                self.information[self.state.value].show()
                if self.state is State.Defeated:
                    break
            # SYNCHRONIZE chessboard
            op: list = reply.split(',')
            try:
                self.chessgame.chessgui.manual_interaction(int(op[0]), int(op[1]), int(op[2]), int(op[3]), str(op[4]))
                if op[6] == 'R' and self.state is State.Waiting:
                    self.state = State.Started
                    self.start_multiplayer_game()
            except ValueError:
                self.state = State.Won
                self.chessgame.end_game()
                self.information[self.state.value].show()
        if self.state is State.Defeated:
            self.chessgame.end_game()
            self.information[self.state.value].show()


class TransparentScreen(QWidget):
    def __init__(self, parent, with_object: bool = True):
        super().__init__(parent=parent)
        self.parent = parent
        self.setFixedSize(self.parent.width(), self.parent.height())
        self.background: QLabel = self.create_background()
        self.with_object: bool = with_object
        if self.with_object:
            self.settings: Settings = Settings(self)
        self.hide()

    def create_background(self) -> QLabel:
        background: QLabel = QLabel(self)
        background.resize(self.width(), self.height())
        background.setStyleSheet('background-color: rgba(46, 46, 46, 220);')
        return background

    def resizeEvent(self, event) -> None:
        self.setFixedSize(self.parent.width(), self.parent.height())
        self.background.resize(self.parent.width(), self.parent.height())
        if self.with_object:
            self.settings.move(int(self.width() / 2 - self.settings.width() / 2), int(self.height() / 2 - self.settings.height() / 2))


class Settings(QWidget):
    def __init__(self, parent: TransparentScreen):
        super().__init__(parent=parent)
        self.parent: TransparentScreen = parent
        self.setMinimumSize(S*5, S*4)
        self.move(int(self.parent.width() / 2-self.width() / 2), S + int(self.parent.height() / 2-self.height() / 2))

        self.create_main_label()
        # self.checkbox: QCheckBox = self.create_checkbox()
        self.combobox_pieces: QComboBox = self.create_combobox('Pieces: ', 'Assets/Images/Pieces/', 0)
        self.combobox_pieces.setCurrentText('standard')

        self.combobox_chessboard: QComboBox = self.create_combobox('Chessboard: ', 'Assets/Images/Chessboard/', self.combobox_pieces.height())
        self.combobox_chessboard.setCurrentText('standard')

        self.textbox_ip: QLineEdit = self.create_textbox('Server IP:', '127.0.0.1', self.combobox_chessboard.height()*2)
        self.textbox_ip.setInputMask('000.000.000.000')

        self.textbox_port: QLineEdit = self.create_textbox('Server PORT:', '5555', self.textbox_ip.height()*3)
        self.textbox_port.setValidator(QIntValidator())

        self.button_save: QPushButton = self.create_button_save('Save', 0, S/2, FS, True, lambda: (self.save(), self.parent.hide()))
        self.button_reset: QPushButton = self.create_button_save('Reset', self.button_save.height(), S/4, FS/2, False, lambda: self.reset())
        self.save()

    def create_button_save(self, text: str, height_shift: int, h: int, fs: int, is_border: bool, function) -> QPushButton:
        button: QPushButton = QPushButton(self)
        button.setText(text)
        button.setStyleSheet('background-color: transparent; color: white;')
        if is_border:
            button.setStyleSheet('background-color: transparent; border: 1px solid gray; color: white;')
        button.setFont(QFont('Arial', fs))
        button.setFixedSize(S*4.5, h)
        button.move(self.width()/2-button.width()/2, S*4+height_shift)
        button.clicked.connect(function)
        return button

    def save(self):
        set_pieces(self.combobox_pieces.currentText())
        set_chessboard(self.combobox_chessboard.currentText())
        set_ip(self.textbox_ip.text())
        set_port(self.textbox_port.text())

    def reset(self):
        self.combobox_pieces.setCurrentText('standard')
        self.combobox_chessboard.setCurrentText('standard')
        self.textbox_ip.setText('127.0.0.1')
        self.textbox_port.setText('5555')
        self.save()

    def create_main_label(self) -> None:
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
        self.move(int(self.parent.width() / 2-self.width() / 2), int(self.parent.height() / 2-self.height() / 2))

    def create_checkbox(self) -> QCheckBox:
        checkbox: QCheckBox = QCheckBox(parent=self)
        checkbox.setText('Show coordinates')
        checkbox.setFont(QFont('Arial', FS))
        checkbox.setStyleSheet('color: white;')
        checkbox.setWindowFlag(Qt.WindowStaysOnTopHint)
        checkbox.setLayoutDirection(Qt.RightToLeft)
        checkbox.move(0, self.height()/2-checkbox.height()/2)
        return checkbox

    def create_nearlabel(self, description: str, height_shift: int) -> QLabel:
        textlabel: QLabel = QLabel(self)
        textlabel.setText(description)
        textlabel.setFont(QFont('Arial', FS))
        textlabel.setStyleSheet('color: white;')
        textlabel.move(S / 4, self.height() / 2 - textlabel.height() / 2 + height_shift)
        return textlabel

    def create_combobox(self, description: str, directory: str, height_shift: int) -> QComboBox:
        self.create_nearlabel(description, height_shift)
        combobox: QComboBox = QComboBox(parent=self)
        combobox.setFont(QFont('Arial', 0.8*FS))
        combobox.setStyleSheet('color: black; background-color: white; border: 1px solid gray;')
        combobox.setWindowFlag(Qt.WindowStaysOnTopHint)
        combobox.setFixedSize(QSize(S*2.25, combobox.height()))
        combobox.move(self.width()-combobox.width()-0.25*S, self.height() / 2 - combobox.height() / 2 + height_shift)
        for folder in listdir(directory):
            combobox.addItem(folder)
        return combobox

    def create_textbox(self, description: str, default: str, height_shift: int) -> QLineEdit:
        self.create_nearlabel(description, height_shift)
        textbox: QLineEdit = QLineEdit(self)
        textbox.setStyleSheet('background-color: white; border: 1px solid gray;')
        textbox.setFont(QFont('Arial', 0.7*FS))
        textbox.setText(default)
        textbox.setFixedSize(QSize(S*2.25, textbox.height()))
        textbox.move(self.width()-textbox.width()-0.25*S, self.height() / 2 - textbox.height() / 2 + height_shift)
        return textbox

    # show/hide coordinates
    # show/hide additional button (same as for shortcuts)
    # show/hide position indicator
    # turn on/off sound in the application
