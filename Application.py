from PyQt5.QtWidgets import QWidget, QLabel
from PyQt5.QtCore import QSize, Qt, QEvent
from ChessLogic import Chess, Position
from Library import exists, new_label, LS

turn: int = 0
x1 = y1 = x2 = y2 = 0
move_buffer: list = []
check_buffer: list = []
position_buffer: list = []
capture_buffer: list = []


class Window(QWidget):
    enable_mouse_click: bool = True

    def __init__(self, log_file):
        super(Window, self).__init__()
        self.chess = Chess()
        self.label = Label(self, self.chess)
        self.log_file = log_file

        self.setFixedSize(QSize(LS*8, LS*8))
        self.setWindowTitle('Chess')
        # self.move(200, 200)
        self.show()

    # user interaction
    def mousePressEvent(self, click) -> None:
        global x1, x2, y1, y2, move_buffer
        if not (len(move_buffer) == 0 and self.chess.chessboard[click.y() // LS][click.x() // LS] == '--'):
            move_buffer.append([click.y() // LS, click.x() // LS])
            x1, y1 = move_buffer[0][0], move_buffer[0][1]
            self.fill_buffers()
            self.label.show_indicators()
            if len(move_buffer) == 2:
                x2, y2 = move_buffer[1][0], move_buffer[1][1]
                self.move_action()
                self.label.hide_indicators()
        self.check()
        if self.checkmate() or self.stalemate():
            self.enable_mouse_click = False

    def eventFilter(self, obj, event) -> bool:
        if not self.enable_mouse_click:
            if event.type() in (QEvent.MouseButtonPress, QEvent.MouseButtonDblClick):
                if event.button() == Qt.LeftButton:
                    return True
        return super(Window, self).eventFilter(obj, event)

    # INDICATORS
    def fill_buffers(self) -> None:
        global check_buffer, x1, x1
        move_set: set = Position(self.chess.chessboard, x1, y1, self.chess.chessboard[x1][y1]).move_set()
        move_set = self.chess.verify_position(x1, y1, move_set, self.chess.chessboard.copy())
        for cell in move_set:
            if exists(cell):
                if self.chess.chessboard[cell[0]][cell[1]] == '--':
                    position_buffer.append(cell)
                elif self.chess.chessboard[cell[0]][cell[1]] != '--' and self.chess.chessboard[cell[0]][cell[1]][1] != 'K':
                    capture_buffer.append(cell)
                elif self.chess.chessboard[cell[0]][cell[1]][1] == 'K':
                    check_buffer = list(cell)

    # piece move
    def move_action(self) -> None:
        if (x2, y2) in position_buffer or (x2, y2) in capture_buffer:
            self.is_capture()
            self.is_promotion(self.chess.chessboard[x1][y1], (x2, y2))
            self.move_piece()
            self.update_log()
        else:
            move_buffer.clear()

    def is_promotion(self, piece: str, pos: tuple):
        if piece[1] == 'p':
            if (piece[0] == 'w' and pos[0] == 0) or (piece[0] == 'b' and pos[0] == 7):
                self.enable_mouse_click = False
                Promotion(self, pos, piece)

    def is_capture(self) -> None:
        if self.chess.chessboard[x2][y2] != '--':
            self.label.pieces[x2][y2].hide()
            self.chess.chessboard[x2][y2] = '--'

    def move_piece(self) -> None:
        self.chess.chessboard[x2][y2] = self.chess.chessboard[x1][y1]
        self.chess.chessboard[x1][y1] = '--'
        self.move_piece_label()

    def move_piece_label(self) -> None:
        self.label.pieces[x2][y2] = self.label.pieces[x1][y1]
        self.label.pieces[x1][y1] = QLabel(self)
        self.label.pieces[x2][y2].move(y2 * LS, x2 * LS)
        self.label.hide_position()
        move_buffer.clear()

    # game log
    def update_log(self) -> None:
        global turn
        turn += 1
        self.log_file.write(
            str(turn) + '. ' +
            self.chess.chessboard[x2][y2] + ' ' +
            self.chess.square_names[x1][y1] + '->' +
            self.chess.square_names[x2][y2] + '\n'
        )

    # END-GAME procedures
    def check_for(self, piece: str) -> None:
        position: tuple = self.chess.pos(piece)
        check_buffer.append(position[0])
        check_buffer.append(position[1])
        self.label.show_check()

    def check(self) -> None:
        if self.chess.check('w') and len(check_buffer) != 2:
            self.check_for('wK')
        elif self.chess.check('b') and len(check_buffer) != 2:
            self.check_for('bK')
        else:
            self.label.hide_check()

    def checkmate(self) -> bool:
        if self.chess.no_position('w'):
            if self.chess.check('w'):
                self.label.checkmate[self.chess.pos('wK')[0]][self.chess.pos('wK')[1]].show()
                return True
        elif self.chess.no_position('b'):
            if self.chess.check('b'):
                self.label.checkmate[self.chess.pos('bK')[0]][self.chess.pos('bK')[1]].show()
                return True
        return False

    def stalemate_for(self, color: str) -> bool:
        if self.chess.no_position(color):
            if not self.chess.check(color):
                for r in range(len(self.chess.chessboard)):
                    for c in range(len(self.chess.chessboard)):
                        if self.chess.chessboard[r][c][0] == color:
                            if self.chess.chessboard[r][c][1] == 'K':
                                self.label.checkmate[r][c].show()
                            else:
                                self.label.stalemate[r][c].show()
                            return True
        return False

    def stalemate(self) -> bool:
        if self.stalemate_for('w'):
            return True
        return self.stalemate_for('b')


class Promotion(QWidget):
    def __init__(self, _window: QWidget, position: tuple, piece: str):
        self.window: QWidget = _window
        self.color: str = piece[0]
        self.x = position[0]
        self.y = position[1]
        super(Promotion, self).__init__(self.window)

        self.case: list = [(0, 'Q'), (LS, 'R'), (LS*2, 'N'), (LS*3, 'B')] if self.color == 'w' else [(0, 'B'), (LS, 'N'), (LS*2, 'R'), (LS*3, 'Q')]
        for _tuple in self.case:
            new_label(0, _tuple[0], LS, LS, 'grs', self).show()
            new_label(0, _tuple[0], LS, LS, self.color + _tuple[1], self).show()

        self.move(self.y * LS, 0) if self.color == 'w' else self.move(self.y * LS, LS*4)
        self.setFixedSize(QSize(LS, LS*4))
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.show()

    def mousePressEvent(self, click):
        self.window.enable_mouse_click = True
        piece: str = self.color + self.case[click.y() // LS][1]
        self.promotional_replacement(piece)
        self.hide()

    def promotional_replacement(self, _piece: str):
        self.window.chess.chessboard[self.x][self.y] = _piece
        self.window.label.pieces[self.x][self.y].hide()
        self.window.label.pieces[self.x][self.y] = new_label(self.y * LS, self.x * LS, LS, LS, _piece, self.window)
        self.window.label.pieces[self.x][self.y].show()


class Label:
    def __init__(self, window: QWidget, chess: Chess = None):
        self.background: list = self.create_background(window, chess)
        self.position: list = self.create_indicators('gd', window, chess)
        self.check: list = self.create_indicators('rc', window, chess)
        self.choice: list = self.create_indicators('ys', window, chess)
        self.checkmate: list = self.create_indicators('rs', window, chess)
        self.stalemate: list = self.create_indicators('os', window, chess)
        self.capture: list = self.create_indicators('gc', window, chess)
        self.pieces: list = self.create_pieces(window, chess)

    # labels
    @staticmethod
    def create_background(window: QWidget, chess: Chess) -> list:
        _background: list = []
        for y in range(len(chess.chessboard)):
            _background.append([])
            for x in range(len(chess.chessboard)):
                _background[y].append(
                    new_label(x * LS, y * LS, LS, LS, 'gs' if (y + x) % 2 else 'ws', window))
                _background[y][x].show()
        return _background

    @staticmethod
    def create_pieces(window: QWidget, chess: Chess) -> list:
        _pieces: list = []
        for y in range(len(chess.chessboard)):
            _pieces.append([])
            for x in range(len(chess.chessboard)):
                _pieces[y].append(QLabel(parent=window))
                if chess.chessboard[y][x] != '--':
                    _pieces[y][x] = new_label(x * LS, y * LS, LS, LS, chess.chessboard[y][x], window)
                    _pieces[y][x].show()
        return _pieces

    @staticmethod
    def create_indicators(label: str, window: QWidget, chess: Chess) -> list:
        indicators: list = []
        for y in range(len(chess.chessboard)):
            indicators.append([])
            for x in range(len(chess.chessboard)):
                indicators[y].append(new_label(x * LS, y * LS, LS, LS, label, window))
                indicators[y][x].hide()
        return indicators

    # SHOW/HIDE all indicators
    def show_indicators(self) -> None:
        self.show_choice()
        self.show_position()
        self.show_capture()
        self.show_check()

    def hide_indicators(self) -> None:
        self.hide_choice()
        self.hide_position()
        self.hide_capture()
        self.hide_check()

    # CHOICE indicator
    def show_choice(self) -> None:
        self.choice[x1][y1].show()

    def hide_choice(self) -> None:
        self.choice[x1][y1].hide()

    # CHECK indicator
    def show_check(self) -> None:
        if len(check_buffer) != 0:
            self.check[check_buffer[0]][check_buffer[1]].show()

    def hide_check(self) -> None:
        if len(check_buffer) != 0:
            self.check[check_buffer[0]][check_buffer[1]].hide()
            check_buffer.clear()

    # CAPTURE indicator
    def show_capture(self) -> None:
        for cell in capture_buffer:
            self.capture[cell[0]][cell[1]].show()

    def hide_capture(self) -> None:
        for cell in capture_buffer:
            self.capture[cell[0]][cell[1]].hide()
        capture_buffer.clear()

    # POSITION indicator
    def show_position(self) -> None:
        for cell in position_buffer:
            self.position[cell[0]][cell[1]].show()

    def hide_position(self) -> None:
        for cell in position_buffer:
            self.position[cell[0]][cell[1]].hide()
        position_buffer.clear()
