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
        self.castling = Castling()

    @staticmethod
    def create_square_names() -> list:
        square_names: list = []
        for row in range(1, 9, 1):
            square_names.append([])
            for letter in ascii_lowercase:
                square_names[row - 1].append(letter + str(9 - row))
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
                    tmp: set = Position(self.chessboard, r, c).move_set()
                    tmp = self.evade_the_check(r, c, tmp)
                    _ams.update(tmp)
        return len(_ams) == 0

    def cms(self, color: str):
        ms = set()
        for r in range(len(self.chessboard)):
            for c in range(len(self.chessboard)):
                if self.chessboard[r][c][0] == color:
                    ms.update(Position(self.chessboard, r, c).move_set())
        return ms

    def check(self, color: str) -> bool:
        return self.pos(color + 'K') in (self.cms('b') if color == 'w' else self.cms('w'))

    def evade_the_check(self, x, y, ms: set):
        vms = set()
        for p in ms:
            p1, p2 = self.chessboard[x][y], self.chessboard[p[0]][p[1]]
            if p2 == '--':
                self.chessboard[x][y], self.chessboard[p[0]][p[1]] = self.chessboard[p[0]][p[1]], self.chessboard[x][y]
            else:
                self.chessboard[p[0]][p[1]] = self.chessboard[x][y]
                self.chessboard[x][y] = '--'
            if not self.check(self.chessboard[p[0]][p[1]][0]):
                vms.add(p)
            self.chessboard[x][y], self.chessboard[p[0]][p[1]] = p1, p2
        return vms

    def print_chessboard(self):
        for r in range(len(self.chessboard)):
            for c in range(len(self.chessboard)):
                print(self.chessboard[r][c], end=' ')
            print()

    def print_position(self):
        for r in range(len(self.chessboard)):
            for c in range(len(self.chessboard)):
                print(r, c, sep="", end=' ')
            print()

    def move_set(self, x: int, y: int) -> set:
        move_set: set = Position(self.chessboard, x, y).move_set()
        move_set = self.evade_the_check(x, y, move_set)
        self.castling.update_castling(self.chessboard, self.cms)
        if self.chessboard[x][y] == 'wK':
            if self.castling.through(self.castling.long_w):
                move_set.add((7, 2))
            if self.castling.through(self.castling.short_w):
                move_set.add((7, 6))
        elif self.chessboard[x][y] == 'bK':
            if self.castling.through(self.castling.long_b):
                move_set.add((0, 2))
            if self.castling.through(self.castling.short_b):
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


class Castling:
    def __init__(self):
        # R was not moved, K was not moved, way is clear, not dangerous pos, K would not be under check
        self.long_w = [True, True, True, True, True]
        self.long_b = [True, True, True, True, True]
        self.short_w = [True, True, True, True, True]
        self.short_b = [True, True, True, True, True]

    def dangerous_white_pos(self, bms: set):
        # wK goes through dangerous pos
        self.long_w[3] = False if (7, 3) in bms else True
        self.long_w[3] = False if (7, 2) in bms else True
        self.short_w[3] = False if (7, 5) in bms else True
        self.short_w[3] = False if (7, 6) in bms else True

    def dangerous_black_pos(self, wms: set):
        # bK goes through dangerous pos
        self.long_b[3] = False if (0, 3) in wms else True
        self.long_b[3] = False if (0, 2) in wms else True
        self.short_b[3] = False if (0, 5) in wms else True
        self.short_b[3] = False if (0, 6) in wms else True

    def way_is_clear(self, chessboard: list):
        # long white
        for c in range(1, 4, 1):
            self.long_w[2] = True
            if chessboard[7][c] != '--':
                self.long_w[2] = False
                break
        # short white
        print("NEW")
        for c in range(5, 7, 1):
            print(7, c)
            self.short_w[2] = True
            if chessboard[7][c] != '--':
                self.short_w[2] = False
                break
        # long black
        for c in range(1, 4, 1):
            self.long_b[2] = True
            if chessboard[0][c] != '--':
                self.long_b[2] = False
                break
        # short black
        for c in range(5, 7, 1):
            self.short_b[2] = True
            if chessboard[0][c] != '--':
                self.short_b[2] = False
                break

    def moved_guy(self, chessboard: list):
        if chessboard[0][4][1] != 'K':
            self.long_b[1] = False
            self.short_b[1] = False
        if chessboard[0][0][1] != 'R':
            self.long_b[0] = False
        if chessboard[0][7][1] != 'R':
            self.short_b[0] = False
        if chessboard[7][0][1] != 'R':
            self.long_w[0] = False
        if chessboard[7][7][1] != 'R':
            self.short_w[0] = False
        if chessboard[7][4][1] != 'K':
            self.long_w[1] = False
            self.short_w[1] = False

    def update_castling(self, chessboard: list, cms):
        self.way_is_clear(chessboard)
        self.dangerous_white_pos(cms('b'))
        self.dangerous_black_pos(cms('w'))
        self.moved_guy(chessboard)

    @staticmethod
    def through(guy: list) -> bool:
        for _bool in guy:
            if not _bool:
                return False
        return True
