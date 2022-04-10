from PyQt5.QtWidgets import QWidget, QLabel
from PyQt5.QtGui import QPixmap, QImage, QPalette, QBrush
from PyQt5.QtCore import Qt, QSize
from datetime import datetime, timedelta
from typing import Final
from enum import Enum
import operator
import os

# label size
S: Final = 90
FS: Final = int(S/4)


def opf(v1, v2, _operator: str):
    operators = {'+': operator.add, '-': operator.sub}
    return operators[_operator](v1, v2)


def exist(coordinate: int, start: int = 0, end: int = 8) -> bool:
    return start <= coordinate < end


def exists(coordinates: tuple, start: int = 0, end: int = 8) -> bool:
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
        if exists(_tuple):
            __set.add(_tuple)
    return __set


def new_label(x: int, y: int, width: int, height: int, img: str, window: QWidget) -> QLabel:
    label = QLabel(parent=window)
    label.setPixmap(QPixmap(image(img)).scaled(S, S, Qt.KeepAspectRatio, Qt.SmoothTransformation))
    label.resize(width, height)
    label.move(x, y)
    return label


def background(image: str) -> QPalette:
    img = QImage('Images/Standard/'+image+'.png').scaled(QSize(S * 10, S * 10))
    palette = QPalette()
    palette.setBrush(QPalette.Window, QBrush(img))
    return palette


class RetVal(Enum):
    # from QMessageBox.exec_():
    Yes = 16384
    No = 65536
