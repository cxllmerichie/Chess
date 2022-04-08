from Library import exist, exists, opf, set_exists
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
        self.castling = Castling()

    @staticmethod
    def create_square_names() -> list:
        square_names: list = []
        for row in range(1, 9, 1):
            square_names.append([])
            for letter in ascii_lowercase:
                square_names[row - 1].append(letter + str(9 - row))
        return square_names

    def position(self, piece: str) -> tuple:
        for row in range(len(self.chessboard)):
            for col in range(len(self.chessboard)):
                if self.chessboard[row][col] == piece:
                    return row, col
        return -1, -1

    def empty_move_set_for(self, color: str) -> bool:
        _ams = set()
        for r in range(len(self.chessboard)):
            for c in range(len(self.chessboard)):
                if self.chessboard[r][c][0] == color:
                    tmp: set = Position(self.chessboard, r, c).move_set()
                    tmp = self.prevent_the_check(r, c, tmp)
                    _ams.update(tmp)
        return len(_ams) == 0

    def move_set_for(self, color: str):
        ms = set()
        for r in range(len(self.chessboard)):
            for c in range(len(self.chessboard)):
                if self.chessboard[r][c][0] == color:
                    ms.update(Position(self.chessboard, r, c).move_set())
        return ms

    def is_check_for(self, color: str) -> bool:
        return self.position(color + 'K') in (self.move_set_for('b') if color == 'w' else self.move_set_for('w'))

    def prevent_the_check(self, x, y, ms: set):
        vms = set()
        for p in ms:
            p1, p2 = self.chessboard[x][y], self.chessboard[p[0]][p[1]]
            if p2 == '--':
                self.chessboard[x][y], self.chessboard[p[0]][p[1]] = self.chessboard[p[0]][p[1]], self.chessboard[x][y]
            else:
                self.chessboard[p[0]][p[1]] = self.chessboard[x][y]
                self.chessboard[x][y] = '--'
            if not self.is_check_for(self.chessboard[p[0]][p[1]][0]):
                vms.add(p)
            self.chessboard[x][y], self.chessboard[p[0]][p[1]] = p1, p2
        return vms

    """def print_chessboard(self):
        for r in range(len(self.chessboard)):
            for c in range(len(self.chessboard)):
                print(self.chessboard[r][c], end=' ')
            print()

    def print_position(self):
        for r in range(len(self.chessboard)):
            for c in range(len(self.chessboard)):
                print(r, c, sep="", end=' ')
            print()"""

    def move_set(self, x: int, y: int) -> set:
        move_set: set = Position(self.chessboard, x, y).move_set()
        move_set = self.prevent_the_check(x, y, move_set)
        self.castling.update(self.chessboard, self.move_set_for)
        if self.chessboard[x][y] == 'wK':
            if self.castling.allowed(self.castling.long_w):
                move_set.add((7, 2))
            if self.castling.allowed(self.castling.short_w):
                move_set.add((7, 6))
        elif self.chessboard[x][y] == 'bK':
            if self.castling.allowed(self.castling.long_b):
                move_set.add((0, 2))
            if self.castling.allowed(self.castling.short_b):
                move_set.add((0, 6))
        return move_set


class Position:
    def __init__(self, chessboard, x: int = 0, y: int = 0):
        self.chessboard = chessboard
        self.x: int = x
        self.y: int = y
        self.piece_name: str = self.chessboard[x][y][1]
        self.color: str = self.chessboard[x][y][0]

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
        return set_exists(_set)

    def pawn(self) -> set:
        ms = set()
        opposite = 'b'
        op = '-'
        if self.color == 'b':
            opposite = 'w'
            op = '+'

        if exist(opf(self.x, 1, op)):
            if self.chessboard[opf(self.x, 1, op)][self.y] == '--':
                ms.add((opf(self.x, 1, op), self.y))
            if exist(opf(self.x, 1, op)) and exist(self.y - 1):
                if self.chessboard[opf(self.x, 1, op)][self.y - 1][0] == opposite:
                    ms.add((opf(self.x, 1, op), self.y - 1))
            if exist(opf(self.x, 1, op)) and exist(self.y + 1):
                if self.chessboard[opf(self.x, 1, op)][self.y + 1][0] == opposite:
                    ms.add((opf(self.x, 1, op), self.y + 1))
        if exist(opf(self.x, 2, op)):
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
            for c in range(1, 8, 1):
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


class Castling:
    def __init__(self):
        # R and K were not moved, way is clear, K would not be under check during the way
        self.long_w = [True, True, True]
        self.long_b = [True, True, True]
        self.short_w = [True, True, True]
        self.short_b = [True, True, True]

    def safe_position(self, bms: set, wms: set):
        self.long_w[2] = False if (7, 3) in bms or (7, 2) in bms else True
        self.short_w[2] = False if (7, 5) in bms or (7, 6) in bms else True
        self.long_b[2] = False if (0, 3) in wms or (0, 2) in wms else True
        self.short_b[2] = False if (0, 5) in wms or (0, 6) in wms else True

    def clear_way(self, chessboard: list):
        self.long_w[1] = False if chessboard[7][1] != '--' or chessboard[7][2] != '--' or chessboard[7][3] != '--' else True
        self.short_w[1] = False if chessboard[7][5] != '--' or chessboard[7][6] != '--' else True
        self.long_b[1] = False if chessboard[0][1] != '--' or chessboard[0][2] != '--' or chessboard[0][3] != '--' else True
        self.short_b[1] = False if chessboard[0][5] != '--' or chessboard[0][6] != '--' else True

    def not_moved_pieces(self, chessboard: list):
        if chessboard[0][4] != 'bK':
            self.long_b[0] = False
            self.short_b[0] = False
        if chessboard[0][0] != 'bR':
            self.long_b[0] = False
        if chessboard[0][7] != 'bR':
            self.short_b[0] = False
        if chessboard[7][0] != 'wR':
            self.long_w[0] = False
        if chessboard[7][7] != 'wR':
            self.short_w[0] = False
        if chessboard[7][4] != 'wK':
            self.long_w[0] = False
            self.short_w[0] = False

    def update(self, chessboard: list, cms):
        self.clear_way(chessboard)
        self.safe_position(cms('b'), cms('w'))
        self.not_moved_pieces(chessboard)

    @staticmethod
    def allowed(guy: list) -> bool:
        for _bool in guy:
            if not _bool:
                return False
        return True
