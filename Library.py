import operator
from datetime import datetime
from datetime import timedelta


def opf(v1, v2, _operator: str):
    operators = {'+': operator.add, '-': operator.sub}
    return operators[_operator](v1, v2)


def in_range(coordinate: int, start: int = 0, end: int = 8) -> bool:
    return start <= coordinate < end


def exists(point: tuple, start: int = 0, end: int = 8) -> bool:
    return start <= point[0] < end and start <= point[1] < end


def image(suffix: str) -> str:
    return 'Figures/' + suffix + '.png'


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
