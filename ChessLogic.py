from Library import exists, exist, operate, set_exists, create_square_names, true_list


class ChessLogic:
    def __init__(self):
        self.square_names: list = create_square_names()
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
        self.last_move = [(0, 0), (0, 0)]

    def position(self, piece: str) -> tuple:
        for row in range(len(self.chessboard)):
            for col in range(len(self.chessboard)):
                if self.chessboard[row][col] == piece:
                    return row, col
        return -1, -1

    def empty_move_set_for(self, color: str) -> bool:
        ms = set()
        for r in range(len(self.chessboard)):
            for c in range(len(self.chessboard)):
                if self.chessboard[r][c][0] == color:
                    tmp: set = Position(self.chessboard, r, c, self.last_move).move_set()
                    tmp = self.prevent_the_check(r, c, tmp)
                    ms.update(tmp)
        return len(ms) == 0

    def move_set_for(self, color: str):
        ms = set()
        for r in range(len(self.chessboard)):
            for c in range(len(self.chessboard)):
                if self.chessboard[r][c][0] == color:
                    ms.update(Position(self.chessboard, r, c, self.last_move).move_set())
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

    def move_set(self, x: int, y: int) -> set:
        move_set: set = Position(self.chessboard, x, y, self.last_move).move_set()
        self.castling.update(self.chessboard, self.move_set_for)
        if self.chessboard[x][y] == 'wK':
            if true_list(self.castling.long_w):
                move_set.add((7, 2))
            if true_list(self.castling.short_w):
                move_set.add((7, 6))
        elif self.chessboard[x][y] == 'bK':
            if true_list(self.castling.long_b):
                move_set.add((0, 2))
            if true_list(self.castling.short_b):
                move_set.add((0, 6))
        move_set = self.prevent_the_check(x, y, move_set)
        return move_set


class Position:
    def __init__(self, chessboard, x: int, y: int, last_move: list):
        self.chessboard = chessboard
        self.x: int = x
        self.y: int = y
        self.piece: str = self.chessboard[x][y][1]
        self.color: str = self.chessboard[x][y][0]
        self.last_move: list = last_move

    def move_set(self) -> set:
        _set = set()
        if self.piece == 'p':
            _set = self.pawn()
        elif self.piece == 'R':
            _set = self.rook()
        elif self.piece == 'N':
            _set = self.knight()
        elif self.piece == 'B':
            _set = self.bishop()
        elif self.piece == 'Q':
            _set = self.queen()
        elif self.piece == 'K':
            _set = self.king()
        return set_exists(_set)

    def pawn(self) -> set:
        ms = set()
        opponents = 'w' if self.color == 'b' else 'b'
        operator = '+' if self.color == 'b' else '-'
        x1, x2 = operate(self.x, operator, 1), operate(self.x, operator, 2)
        if exists(x1):
            if self.chessboard[x1][self.y] == '--':
                ms.add((x1, self.y))
            if exists(x1) and exists(self.y - 1) and self.chessboard[x1][self.y - 1][0] == opponents:
                ms.add((x1, self.y - 1))
            if exists(x1) and exists(self.y + 1) and self.chessboard[x1][self.y + 1][0] == opponents:
                ms.add((x1, self.y + 1))
        if exists(x2) and (self.x == 6 or self.x == 1):
            if self.chessboard[x2][self.y] == self.chessboard[x1][self.y] == '--':
                ms.add((x2, self.y))
        # en passant
        x1, y1, x2, y2 = self.last_move[0][0], self.last_move[0][1], self.last_move[1][0], self.last_move[1][1]
        if self.chessboard[x2][y2] == 'bp':
            if abs(x1 - x2) == 2 and self.chessboard[self.x][self.y] == 'wp' and self.x == 3:
                if exists(y2 + 1) and self.chessboard[x2][y2 + 1] == 'wp':
                    ms.add((self.x-1, self.y-1))
                elif exists(y2 - 1) and self.chessboard[x2][y2 - 1] == 'wp':
                    ms.add((self.x-1, self.y+1))
        elif self.chessboard[x2][y2] == 'wp':
            if abs(x1 - x2) == 2 and self.chessboard[self.x][self.y] == 'bp' and self.x == 4:
                if exists(y2 + 1) and self.chessboard[x2][y2 + 1] == 'bp':
                    ms.add((self.x+1, self.y-1))
                elif exists(y2 - 1) and self.chessboard[x2][y2 - 1] == 'bp':
                    ms.add((self.x+1, self.y+1))
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
            if exist(point) and self.chessboard[point[0]][point[1]][0] != self.color:
                ms.add((point[0], point[1]))
        return ms

    def bishop(self) -> set:
        ms = set()
        tmp = [('+', '+'), ('-', '+'), ('+', '-'), ('-', '-')]
        for op in tmp:
            for c in range(1, 8, 1):
                x, y = operate(self.x, op[0], c), operate(self.y, op[1], c)
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
            if exist(point) and self.chessboard[point[0]][point[1]][0] != self.color:
                ms.add((point[0], point[1]))
        return ms


class Castling:
    def __init__(self):
        # R and K were not moved, way is clear, K would not be under check during the way
        self.long_w = [True, True, True]
        self.long_b = [True, True, True]
        self.short_w = [True, True, True]
        self.short_b = [True, True, True]

    def safe_position(self, bms: set, wms: set) -> None:
        self.long_w[2] = False if (7, 3) in bms or (7, 2) in bms else True
        self.short_w[2] = False if (7, 5) in bms or (7, 6) in bms else True
        self.long_b[2] = False if (0, 3) in wms or (0, 2) in wms else True
        self.short_b[2] = False if (0, 5) in wms or (0, 6) in wms else True

    def clear_way(self, chessboard: list) -> None:
        self.long_w[1] = False if chessboard[7][1] != '--' or chessboard[7][2] != '--' or chessboard[7][3] != '--' else True
        self.short_w[1] = False if chessboard[7][5] != '--' or chessboard[7][6] != '--' else True
        self.long_b[1] = False if chessboard[0][1] != '--' or chessboard[0][2] != '--' or chessboard[0][3] != '--' else True
        self.short_b[1] = False if chessboard[0][5] != '--' or chessboard[0][6] != '--' else True

    def not_moved_pieces(self, chessboard: list) -> None:
        if chessboard[0][4] != 'bK':
            self.long_b[0] = False
            self.short_b[0] = False
            return None
        if chessboard[0][0] != 'bR':
            self.long_b[0] = False
            return None
        if chessboard[0][7] != 'bR':
            self.short_b[0] = False
            return None
        if chessboard[7][0] != 'wR':
            self.long_w[0] = False
            return None
        if chessboard[7][7] != 'wR':
            self.short_w[0] = False
            return None
        if chessboard[7][4] != 'wK':
            self.long_w[0] = False
            self.short_w[0] = False

    def update(self, chessboard: list, cms) -> None:
        self.clear_way(chessboard)
        self.safe_position(cms('b'), cms('w'))
        self.not_moved_pieces(chessboard)
