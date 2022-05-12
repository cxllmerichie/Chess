from PyQt5.QtWidgets import QWidget, QLabel, QPushButton
from PyQt5.QtGui import QPixmap, QImage, QPalette, QBrush, QFont
from PyQt5.QtCore import Qt, QSize
from datetime import datetime, timedelta
from string import ascii_lowercase
from Common.Constants import S, FS, IMAGE_PATH, SOUND_PATH
from os import path, getcwd
from enum import Enum
import operator


def operate(left: int, _operator: str, right: int):
    operators = {'+': operator.add, '-': operator.sub}
    return operators[_operator](left, right)


def exists(coordinate: int, start: int = 0, end: int = 8) -> bool:
    return start <= coordinate < end


def exist(coordinates: tuple, start: int = 0, end: int = 8) -> bool:
    return start <= coordinates[0] < end and start <= coordinates[1] < end


def image(name: str) -> str:
    return IMAGE_PATH + name + '.png'


def sound(name: str) -> str:
    return path.join(getcwd() + SOUND_PATH, name + '.mp3')


def time() -> str:
    return datetime.now().strftime("%H:%M:%S")


def date() -> str:
    return datetime.now().strftime("%Y-%m-%d")


def duration(start: float, end: float) -> str:
    return str(timedelta(seconds=int(end-start)))


def line(length: int, symbol: str = '-') -> str:
    return symbol * length + '\n'


def set_exists(_set: set) -> set:
    __set = set()
    for _tuple in _set:
        if exist(_tuple):
            __set.add(_tuple)
    return __set


def image_label(x: int, y: int, width: int, height: int, img: str, window: QWidget) -> QLabel:
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


def app_label(text: str, size: QSize, color: str, window: QWidget) -> QLabel:
    label: QLabel = QLabel(parent=window)
    label.setText(text)
    label.setFixedSize(size)
    label.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
    label.setFont(QFont('Arial', FS*2))
    label.setStyleSheet(f'color: {color}')
    label.move(0, 0)
    label.hide()
    return label


def new_palette(img: str, width: int = S * 10, height: int = S * 10) -> QPalette:
    img = QImage(IMAGE_PATH + img).scaled(QSize(width, height))
    palette = QPalette()
    palette.setBrush(QPalette.Window, QBrush(img))
    return palette


def game_btn(title: str, geometry: tuple, click, window: QWidget) -> QPushButton:
    button = QPushButton(title, parent=window)
    button.setGeometry(geometry[0], geometry[1], geometry[2], geometry[3])
    button.setFont(QFont('Arial', FS / 2))
    button.setStyleSheet('background: #323232')
    button.clicked.connect(click)
    button.hide()
    return button


def app_btn(title: str, geometry: tuple, click, window: QWidget) -> QPushButton:
    button = QPushButton(title, parent=window)
    button.setGeometry(geometry[0], geometry[1], geometry[2], geometry[3])
    button.setStyleSheet('QPushButton {background-color: #323232; color: white; font-weight: bold;}')
    button.setFont(QFont('Helvetica', int(FS/1.1)))
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


def convert(l: list) -> list:
    return [(abs(7-l[0][0]), abs(7-l[0][1])), (abs(7-l[1][0]), abs(7-l[1][1]))]


class Status:
    Singleplayer = '[Ctrl+R] start new game, [Ctrl+M] return to menu.'
    Practice = '[Ctrl+T] enable/disable timers, [Ctrl+M] return to menu, [Ctrl+H] show/hide this hint.'
    Multiplayer = '[Ctrl+R] resign, [Ctrl+D] suggest draw, [Ctrl+M] return to menu, [Ctrl+H] show/hide this hint.'
    Menu = '[F11] enter/exit full screen mode, [Ctrl+E] exit, [Ctrl+H] show/hide this hint.'
    Settings = ''


class State(Enum):
    NoState = -1
    Waiting = 2
    Resigned = 4
    SuggestedDraw = 6
    AcceptedDraw = 5
    Defeated = 7
    Won = 8
    Started = 0
    Finished = 1
    Proceeding = 3
    Practice = 9
    PracticeNoTime = 10
    PracticeWithTime = 11


class Text:
    Waiting = 'Waiting for another player'
    OpponentResign = 'Opponent Resigned!'
    SelfResign = 'You Resigned...'
    Draw = 'It is a Draw.'
    Win = 'You Win!'
    Defeat = 'You Lost...'


color: dict = {'waiting': 'red', 'opporesign': 'green', 'selfresign': 'red', 'draw': 'gray', 'win': 'green', 'defeat': 'red'}
