from PyQt5.QtWidgets import QWidget, QLabel
from PyQt5.QtGui import QPixmap, QImage, QPalette, QBrush, QFont
from PyQt5.QtCore import Qt, QSize
from datetime import datetime, timedelta
from string import ascii_lowercase
from typing import Final
from enum import Enum
import operator
import os

# label size
S: Final = 90
FS: Final = int(S/4)


def operate(left: int, _operator: str, right: int):
    operators = {'+': operator.add, '-': operator.sub}
    return operators[_operator](left, right)


def exists(coordinate: int, start: int = 0, end: int = 8) -> bool:
    return start <= coordinate < end


def exist(coordinates: tuple, start: int = 0, end: int = 8) -> bool:
    return start <= coordinates[0] < end and start <= coordinates[1] < end


def image(name: str) -> str:
    return 'Images/Standard/' + name + '.png'


def sound(name: str) -> str:
    return os.path.join(os.getcwd() + "/SoundEffects", name + '.mp3')


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


def new_palette(image: str, width: int = S * 10, height: int = S * 10) -> QPalette:
    img = QImage('Images/Standard/'+image+'.png').scaled(QSize(width, height))
    palette = QPalette()
    palette.setBrush(QPalette.Window, QBrush(img))
    return palette


class RetVal(Enum):
    # QMessageBox.exec_() values from buttons Yes & No
    Yes = 16384
    No = 65536


def create_square_names() -> list:
    square_names: list = []
    for row in range(1, 9, 1):
        square_names.append([])
        for letter in ascii_lowercase:
            square_names[row - 1].append(letter + str(9 - row))
    return square_names


def true_list(guy: list) -> bool:
    for _bool in guy:
        if not _bool:
            return False
    return True


def time_to_int(_time: str) -> int:
    return int(_time[:2]) * 60 + int(_time[2:])
