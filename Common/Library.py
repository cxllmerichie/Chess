from PyQt5.QtWidgets import QWidget, QLabel, QPushButton
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtCore import Qt, QSize
from string import ascii_lowercase
from Common.Constants import S, FS, SOUND_PATH, PATH_PREFIX
from os import path, getcwd
from enum import Enum
import operator


CHESSBOARD_STYLE: str = 'standard'
CHESSBOARD_PATH: str = f'{PATH_PREFIX}Assets/Images/Chessboard/{CHESSBOARD_STYLE}/'
# Standard: standard
# Canonical: cardinal chessnut fresca icpieces kosal merida
# Specific: fantasy pirouetti riohacha spatial
# Strange but interesting: horsey letter shapes
PIECE_STYLE: str = 'standard'
PIECE_PATH: str = f'{PATH_PREFIX}Assets/Images/Pieces/{PIECE_STYLE}/'
INDICATOR_STYLE: str = 'standard'
INDICATOR_PATH: str = f'{PATH_PREFIX}Assets/Images/Indicators/{INDICATOR_STYLE}/'


def set_pieces(style: str):
    global PIECE_STYLE, PIECE_PATH
    PIECE_STYLE = style
    PIECE_PATH = f'{PATH_PREFIX}Assets/Images/Pieces/{PIECE_STYLE}/'


def set_chessboard(style: str):
    global CHESSBOARD_STYLE, CHESSBOARD_PATH
    CHESSBOARD_STYLE = style
    CHESSBOARD_PATH = f'{PATH_PREFIX}Assets/Images/Chessboard/{CHESSBOARD_STYLE}/'


def set_indicators(style: str):
    global INDICATOR_STYLE, INDICATOR_PATH
    INDICATOR_STYLE = style
    INDICATOR_PATH = f'{PATH_PREFIX}Assets/Images/Indicators/{INDICATOR_STYLE}/'


def operate(left: int, _operator: str, right: int):
    operators = {'+': operator.add, '-': operator.sub}
    return operators[_operator](left, right)


def exists(coordinate: int, start: int = 0, end: int = 8) -> bool:
    return start <= coordinate < end


def exist(coordinates: tuple, start: int = 0, end: int = 8) -> bool:
    return start <= coordinates[0] < end and start <= coordinates[1] < end


def image(name: str) -> str:
    global PIECE_PATH, CHESSBOARD_PATH, INDICATOR_PATH
    if len(name) == 2:
        if 'standard' in PIECE_PATH:
            return f'{PIECE_PATH}{name}.png'
        return f'{PIECE_PATH}{name}.svg'
    if name == 'dark' or name == 'light':
        return f'{CHESSBOARD_PATH}{name}.svg'
    return f'{INDICATOR_PATH}{name}.svg'


def sound(name: str) -> str:
    return path.join(getcwd() + SOUND_PATH, name + '.mp3')


def set_exists(_set: set) -> set:
    __set = set()
    for _tuple in _set:
        if exist(_tuple):
            __set.add(_tuple)
    return __set


def image_label(x: int, y: int, width: int, height: int, img: str, window) -> QLabel:
    label = QLabel(parent=window)
    label.setPixmap(QPixmap(image(img)).scaled(S, S, Qt.KeepAspectRatio, Qt.SmoothTransformation))
    label.resize(width, height)
    label.move(x, y)
    return label


def text_label(symbol: str, alignment, position: tuple, size: QSize, window: QWidget) -> QLabel:
    label: QLabel = QLabel(parent=window)
    label.setText(symbol)
    label.setFixedSize(size)
    label.setAlignment(alignment)
    label.setFont(QFont('Arial', FS))
    label.setStyleSheet('color: gray')
    label.move(position[0], position[1])
    return label


def app_label(text: str, size: QSize, _color: str, window: QWidget) -> QLabel:
    label: QLabel = QLabel(parent=window)
    label.setText(text)
    label.setFixedSize(size)
    label.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
    label.setFont(QFont('Arial', FS*2))
    label.setStyleSheet(f'color: {_color}')
    label.move(0, 0)
    label.hide()
    return label


def game_btn(title: str, geometry: tuple, click, window: QWidget) -> QPushButton:
    button = QPushButton(title, parent=window)
    button.setGeometry(geometry[0], geometry[1], geometry[2], geometry[3])
    button.setFont(QFont('Arial', FS / 2))
    button.setStyleSheet('background: #323232')
    button.clicked.connect(click)
    button.hide()
    return button


def app_btn(title: str, geometry: tuple, click, window: QWidget, font_size: int = int(FS/1.1)) -> QPushButton:
    button = QPushButton(title, parent=window)
    button.setGeometry(geometry[0], geometry[1], geometry[2], geometry[3])
    button.setStyleSheet('QPushButton {background-color: #323232; color: white; font-weight: bold;}')
    button.setFont(QFont('Helvetica', font_size))
    button.clicked.connect(click)
    button.hide()
    return button


def create_square_names() -> list:
    square_names: list = []
    for row in range(1, 9, 1):
        square_names.append([])
        for letter in ascii_lowercase:
            square_names[row - 1].append(letter + str(9 - row))
    return square_names


def true_list(_list: list) -> bool:
    for _bool in _list:
        if not _bool:
            return False
    return True


def str_time_to_float(_time: str) -> float:
    milliseconds: str = _time[6:]
    return float(_time[:2]) * 60 + float(_time[3:5]) + (float(milliseconds)/1000 if len(milliseconds) != 0 else 0)


def convert(_list: list) -> list:
    return [(abs(7 - _list[0][0]), abs(7 - _list[0][1])), (abs(7 - _list[1][0]), abs(7 - _list[1][1]))]


class Hint:
    # Singleplayer = '[Ctrl+R] start new game, [Ctrl+M] return to menu.'
    Practice = '[Ctrl+R] reset the game, [Ctrl+T] enable timers reseting the game/disable timers, [Ctrl+M] return to menu, [Ctrl+H] show/hide this hint.'
    Multiplayer = '[Ctrl+R] resign, [Ctrl+M] return to menu, [Ctrl+H] show/hide this hint.'
    Menu = '[F9, F10, F11] minimize/maximize/full screen mode, [Ctrl+S] open/close settings, [Ctrl+E] exit, [Ctrl+H] show/hide this hint.'
    Settings = ''


class State(Enum):
    NoState = 'NoState'

    PracticeNoTime = 'PracticeNoTime'
    PracticeWithTime = 'PracticeWithTime'

    Waiting = 'waiting'
    Started = 'Started'
    Won = 'win'
    Defeated = 'defeat'
    SelfResigned = 'selfresign'
    OpponentResigned = 'opporesign'
    SuggestedDraw = 'SuggestedDraw'
    AcceptedDraw = 'draw'
    Draw = 'draw'
    OpponentDisconnected = 'disconnect'
    SelfDisconnected = 'SelfDisconnected'


class StateText:
    Waiting = 'Waiting for another player'
    OppoResign = 'Opponent Resigned!'
    SelfResign = 'You Resigned...'
    Draw = 'It is a Draw.'
    Win = 'You Won!'
    Defeat = 'You Lost...'
    OppoDisconnect = 'Opponent disconnected'
    ServerConnectError = 'Server does not respond.\nMake sure the configuration is correct and try again.'


color: dict = {'waiting': 'red',
               'opporesign': 'green',
               'selfresign': 'red',
               'draw': 'yellow',
               'win': 'green',
               'defeat': 'red',
               'disconnect': 'gray',
               'connectionerror': 'white'}


class ScreenState(Enum):
    Minimized = -1
    Normal = 0
    Maximized = 1
    FullScreen = 2
