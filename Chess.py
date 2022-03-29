from Library import in_range, exists, opf, verify, line
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

    def create_square_names(self) -> list:
        square_names: list = []
        for row in range(1, 9, 1):
            square_names.append([])
            for letter in ascii_lowercase:
                square_names[row-1].append(letter+str(8-row+1))
        return square_names

    def pos(self, piece: str) -> list:
        for row in range(len(self.chessboard)):
            for col in range(len(self.chessboard)):
                if self.chessboard[row][col] == piece:
                    return [row, col]
        return [-1, -1]

    def print(self):
        for row in range(len(self.chessboard)):
            for col in range(len(self.chessboard)):
                print(self.chessboard[row][col], end=" ")
            print()

    def print_coo(self):
        for r in range(len(self.chessboard)):
            for c in range(len(self.chessboard)):
                print(r, c, sep="", end=" ")
            print()

    def print_cells(self):
        for row in range(len(self.square_names)):
            for col in range(len(self.square_names)):
                print(self.square_names[row][col], end=" ")
            print()


class Position:
    def __init__(self, chessboard, x: int = 0, y: int = 0, _object: str = ""):
        self.chessboard = chessboard
        self.x: int = x
        self.y: int = y
        self.pieces: str = _object[1]
        self.color: str = _object[0]

    def move_set(self) -> set:
        _set = set()
        if self.pieces == 'p':
            _set = self.pawn(self.chessboard)
        elif self.pieces == 'R':
            _set = self.rook(self.chessboard)
        elif self.pieces == 'N':
            _set = self.knight(self.chessboard)
        elif self.pieces == 'B':
            _set = self.bishop(self.chessboard)
        elif self.pieces == 'Q':
            _set = self.queen(self.chessboard)
        elif self.pieces == 'K':
            _set = self.king(self.chessboard)
        return verify(_set)

    def pawn(self, desk: list) -> set:
        ms = set()
        opposite = 'b'
        op = '-'
        if self.color == 'b':
            opposite = 'w'
            op = '+'

        if in_range(opf(self.x, 1, op)):
            if desk[opf(self.x, 1, op)][self.y] == '--':
                ms.add((opf(self.x, 1, op), self.y))
            if in_range(opf(self.x, 1, op)) and in_range(self.y - 1):
                if desk[opf(self.x, 1, op)][self.y - 1][0] == opposite:
                    ms.add((opf(self.x, 1, op), self.y - 1))
            if in_range(opf(self.x, 1, op)) and in_range(self.y + 1):
                if desk[opf(self.x, 1, op)][self.y + 1][0] == opposite:
                    ms.add((opf(self.x, 1, op), self.y + 1))
        if in_range(opf(self.x, 2, op)):
            if self.x == 6 or self.x == 1:
                if desk[opf(self.x, 2, op)][self.y] == '--':
                    ms.add((opf(self.x, 2, op), self.y))
        return ms

    def rook(self, desk: list) -> set:
        ms = set()
        up_down: list = [(self.x - 1, -1, -1), (self.x + 1, len(desk), 1)]
        for _range in up_down:
            for c in range(_range[0], _range[1], _range[2]):
                if desk[c][self.y][0] == self.color:
                    break
                ms.add((c, self.y))
                if desk[c][self.y] != '--':
                    break
        right_left: list = [(self.y + 1, len(desk), 1), (self.y - 1, -1, -1)]
        for _range in right_left:
            for c in range(_range[0], _range[1], _range[2]):
                if desk[self.x][c][0] == self.color:
                    break
                ms.add((self.x, c))
                if desk[self.x][c] != '--':
                    break
        return ms

    def knight(self, desk: list) -> set:
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
            if exists(point) and desk[point[0]][point[1]][0] != self.color:
                ms.add((point[0], point[1]))
        return ms

    def bishop(self, desk: list) -> set:
        ms = set()
        tmp = [('+', '+'), ('-', '+'), ('+', '-'), ('-', '-')]
        for op in tmp:
            for c in range(1, 7, 1):
                x, y = opf(self.x, c, op[0]), opf(self.y, c, op[1])
                if x < 8 and y < 8:
                    if desk[x][y][0] == self.color:
                        break
                    ms.add((x, y))
                    if desk[x][y] != '--':
                        break
        return ms

    def queen(self, desk: list) -> set:
        return self.bishop(desk).union(self.rook(desk))

    def king(self, desk: list) -> set:
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
            if exists(point) and desk[point[0]][point[1]][0] != self.color:
                ms.add((point[0], point[1]))
        return ms


class MovementControl:
    def __init__(self):
        pass

    def wms(self, chessboard: list):
        _wms = set()
        for r in range(len(chessboard)):
            for c in range(len(chessboard)):
                if chessboard[r][c][0] == 'w':
                    _wms.update(Position(chessboard, r, c, chessboard[r][c]).move_set())
        return _wms

    def bms(self, chessboard: list):
        _bms = set()
        for r in range(len(chessboard)):
            for c in range(len(chessboard)):
                if chessboard[r][c][0] == 'b':
                    _bms.update(Position(chessboard, r, c, chessboard[r][c]).move_set())
        return _bms

    def print_board(self, chessboard: list):
        for r in range(len(chessboard)):
            for c in range(len(chessboard)):
                print(chessboard[r][c], end=" ")
            print()

    def pos(self, piece, chessboard: list):
        for r in range(len(chessboard)):
            for c in range(len(chessboard)):
                if chessboard[r][c] == piece:
                    return r, c
        return -1, -1

    def check(self, color: str, chessboard: list) -> bool:
        print('Check on ', color, 'K ', (self.pos(color + 'K', chessboard) in (self.bms(chessboard) if color == 'w' else self.wms(chessboard))), sep='')
        return self.pos(color + 'K', chessboard) in (self.bms(chessboard) if color == 'w' else self.wms(chessboard))

    def allowed(self, x1, y1, x2, y2, chessboard: list):
        chessboard[x1][y1], chessboard[x2][y2] = chessboard[x2][y2], chessboard[x1][y1]

    def verify_move_to_avoid_check(self, x, y, ms: set, chessboard: list):
        vms = set()
        test_desk: list = chessboard
        for move in ms:
            p1, p2 = test_desk[x][y], test_desk[move[0]][move[1]]
            if p2 == '--':
                test_desk[x][y], test_desk[move[0]][move[1]] = test_desk[move[0]][move[1]], test_desk[x][y]
            else:
                test_desk[move[0]][move[1]] = test_desk[x][y]
                test_desk[x][y] = '--'
            self.print_board(test_desk)
            if not self.check(test_desk[move[0]][move[1]][0], chessboard):
                vms.add(move)
            test_desk[x][y], test_desk[move[0]][move[1]] = p1, p2
        print(line(50))

        return vms
