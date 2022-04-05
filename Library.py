from PyQt5.QtWidgets import QWidget, QLabel
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from datetime import datetime, timedelta
import operator
from typing import Final

# label size
LS: Final = 80


def opf(v1, v2, _operator: str):
    operators = {'+': operator.add, '-': operator.sub}
    return operators[_operator](v1, v2)


def in_range(coordinate: int, start: int = 0, end: int = 8) -> bool:
    return start <= coordinate < end


def exists(point: tuple, start: int = 0, end: int = 8) -> bool:
    return start <= point[0] < end and start <= point[1] < end


def image(suffix: str) -> str:
    return 'Images/' + suffix + '.png'


def time() -> str:
    return datetime.now().strftime("%H:%M:%S")


def date() -> str:
    return datetime.now().strftime("%Y-%m-%d")


def line(length: int, symbol: str = '-') -> str:
    return symbol * length + '\n'


def duration(start: float, end: float) -> str:
    return str(timedelta(seconds=int(end-start)))


def verify(_set: set) -> set:
    __set = set()
    for _tuple in _set:
        if exists(_tuple):
            __set.add(_tuple)
    return __set


def new_label(x: int, y: int, width: int, height: int, img: str, window: QWidget) -> QLabel:
    label = QLabel(parent=window)
    label.setPixmap(QPixmap(image(img)).scaled(LS, LS, Qt.KeepAspectRatio, Qt.SmoothTransformation))
    label.resize(width, height)
    label.move(x, y)
    return label
