from Library import in_range, exists, opf, verify
from string import ascii_lowercase


class Chess:
    def __init__(self):
        self.square_names: list = self.create_square_names()
        self.chessboard: list = [
            ['bR', 'bN', 'bB', 'bQ', 'bK', 'bB', 'bN', 'bR'],
            ['bp', 'bp', 'bp', 'bp', 'bp', 'bp', 'bp', 'bp'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['wp', 'wp', 'wp', 'wp', 'wp', 'wp', 'wp', 'wp'],
            ['wR', 'wN', 'wB', 'wQ', 'wK', 'wB', 'wN', 'wR']]

    @staticmethod
    def create_square_names() -> list:
        square_names: list = []
        for row in range(1, 9, 1):
            square_names.append([])
            for letter in ascii_lowercase:
                square_names[row-1].append(letter+str(8-row+1))
        return square_names

    def pos(self, piece: str) -> tuple:
        for row in range(len(self.chessboard)):
            for col in range(len(self.chessboard)):
                if self.chessboard[row][col] == piece:
                    return row, col
        return -1, -1

    def no_position(self, color: str) -> bool:
        _ams = set()
        for r in range(len(self.chessboard)):
            for c in range(len(self.chessboard)):
                if self.chessboard[r][c][0] == color:
                    tmp: set = Position(self.chessboard, r, c, self.chessboard[r][c]).move_set()
                    tmp = self.verify_position(r, c, tmp, self.chessboard)
                    _ams.update(tmp)
        return len(_ams) == 0

    def wms(self) -> set:
        _wms = set()
        for r in range(len(self.chessboard)):
            for c in range(len(self.chessboard)):
                if self.chessboard[r][c][0] == 'w':
                    _wms.update(Position(self.chessboard, r, c, self.chessboard[r][c]).move_set())
        return _wms

    def bms(self) -> set:
        _bms = set()
        for r in range(len(self.chessboard)):
            for c in range(len(self.chessboard)):
                if self.chessboard[r][c][0] == 'b':
                    _bms.update(Position(self.chessboard, r, c, self.chessboard[r][c]).move_set())
        return _bms

    def check(self, color: str) -> bool:
        return self.pos(color + 'K') in (self.bms() if color == 'w' else self.wms())

    def verify_position(self, x, y, ms: set, chessboard: list):
        vms = set()
        for move in ms:
            p1, p2 = chessboard[x][y], chessboard[move[0]][move[1]]
            if p2 == '--':
                chessboard[x][y], chessboard[move[0]][move[1]] = chessboard[move[0]][move[1]], chessboard[x][y]
            else:
                chessboard[move[0]][move[1]] = chessboard[x][y]
                chessboard[x][y] = '--'
            if not self.check(chessboard[move[0]][move[1]][0]):
                vms.add(move)
            chessboard[x][y], chessboard[move[0]][move[1]] = p1, p2
        return vms


class Position:
    def __init__(self, chessboard, x: int = 0, y: int = 0, _piece: str = ""):
        self.chessboard = chessboard
        self.x: int = x
        self.y: int = y
        self.piece_name: str = _piece[1]
        self.color: str = _piece[0]

    def move_set(self) -> set:
        _set = set()
        if self.piece_name == 'p':
            _set = self.pawn()
        elif self.piece_name == 'R':
            _set = self.rook()
        elif self.piece_name == 'N':
            _set = self.knight()
        elif self.piece_name == 'B':
            _set = self.bishop()
        elif self.piece_name == 'Q':
            _set = self.queen()
        elif self.piece_name == 'K':
            _set = self.king()
        return verify(_set)

    def pawn(self) -> set:
        ms = set()
        opposite = 'b'
        op = '-'
        if self.color == 'b':
            opposite = 'w'
            op = '+'

        if in_range(opf(self.x, 1, op)):
            if self.chessboard[opf(self.x, 1, op)][self.y] == '--':
                ms.add((opf(self.x, 1, op), self.y))
            if in_range(opf(self.x, 1, op)) and in_range(self.y - 1):
                if self.chessboard[opf(self.x, 1, op)][self.y - 1][0] == opposite:
                    ms.add((opf(self.x, 1, op), self.y - 1))
            if in_range(opf(self.x, 1, op)) and in_range(self.y + 1):
                if self.chessboard[opf(self.x, 1, op)][self.y + 1][0] == opposite:
                    ms.add((opf(self.x, 1, op), self.y + 1))
        if in_range(opf(self.x, 2, op)):
            if self.x == 6 or self.x == 1:
                if self.chessboard[opf(self.x, 2, op)][self.y] == '--' and self.chessboard[opf(self.x, 1, op)][self.y] == '--':
                    ms.add((opf(self.x, 2, op), self.y))
        return ms

    def rook(self) -> set:
        ms = set()
        up_down: list = [(self.x - 1, -1, -1), (self.x + 1, len(self.chessboard), 1)]
        for _range in up_down:
            for c in range(_range[0], _range[1], _range[2]):
                if self.chessboard[c][self.y][0] == self.color:
                    break
                ms.add((c, self.y))
                if self.chessboard[c][self.y] != '--':
                    break
        right_left: list = [(self.y + 1, len(self.chessboard), 1), (self.y - 1, -1, -1)]
        for _range in right_left:
            for c in range(_range[0], _range[1], _range[2]):
                if self.chessboard[self.x][c][0] == self.color:
                    break
                ms.add((self.x, c))
                if self.chessboard[self.x][c] != '--':
                    break
        return ms

    def knight(self) -> set:
        ms = set()
        tmp = [(self.x - 2, self.y - 1),
               (self.x - 2, self.y + 1),
               (self.x + 2, self.y - 1),
               (self.x + 2, self.y + 1),
               (self.x - 1, self.y - 2),
               (self.x - 1, self.y + 2),
               (self.x + 1, self.y - 2),
               (self.x + 1, self.y + 2)]
        for point in tmp:
            if exists(point) and self.chessboard[point[0]][point[1]][0] != self.color:
                ms.add((point[0], point[1]))
        return ms

    def bishop(self) -> set:
        ms = set()
        tmp = [('+', '+'), ('-', '+'), ('+', '-'), ('-', '-')]
        for op in tmp:
            for c in range(1, 7, 1):
                x, y = opf(self.x, c, op[0]), opf(self.y, c, op[1])
                if x < 8 and y < 8:
                    if self.chessboard[x][y][0] == self.color:
                        break
                    ms.add((x, y))
                    if self.chessboard[x][y] != '--':
                        break
        return ms

    def queen(self) -> set:
        return self.bishop().union(self.rook())

    def king(self) -> set:
        ms = set()
        tmp = [(self.x, self.y + 1),
               (self.x, self.y - 1),
               (self.x + 1, self.y),
               (self.x - 1, self.y),
               (self.x + 1, self.y + 1),
               (self.x + 1, self.y - 1),
               (self.x - 1, self.y - 1),
               (self.x - 1, self.y + 1)]
        for point in tmp:
            if exists(point) and self.chessboard[point[0]][point[1]][0] != self.color:
                ms.add((point[0], point[1]))
        return ms
