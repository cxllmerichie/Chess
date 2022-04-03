from PyQt5.QtWidgets import QWidget, QLabel
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QPixmap
from Chess import Chess, Position, MovementControl
from Library import exists, image


class Window(QWidget):
    turn: int = 0
    x1 = y1 = x2 = y2 = 0
    move_buffer: list = []
    position_buffer: list = []
    hit_buffer: list = []
    check_buffer: list = []

    def __init__(self, log_file):
        super(Window, self).__init__()
        self.chess = Chess()
        self.log_file = log_file

        self.chessboard_labels: list = self.create_chessboard_labels()
        self.position_indicators: list = self.create_indicators('gd')
        self.check_indicators: list = self.create_indicators('rc')
        self.pick_indicators: list = self.create_indicators('ys')
        self.checkmate_indicators: list = self.create_indicators('rs')
        self.stalemate_indicators: list = self.create_indicators('os')
        self.pieces_labels: list = self.create_pieces_labels()
        self.hit_indicators: list = self.create_indicators('gc')

        self.setFixedSize(QSize(800, 800))
        self.setWindowTitle('Chess')
        self.show()

    # user interaction
    def mousePressEvent(self, mouse_event) -> None:
        if not (len(self.move_buffer) == 0 and self.chess.chessboard[int(mouse_event.y() / 100)][int(mouse_event.x() / 100)] == '--'):
            self.move_buffer.append([int(mouse_event.y() / 100), int(mouse_event.x() / 100)])
            self.x1, self.y1 = self.move_buffer[0][0], self.move_buffer[0][1]
            self.fill_buffers()
            self.show_indicators()
            if len(self.move_buffer) == 2:
                self.x2, self.y2 = self.move_buffer[1][0], self.move_buffer[1][1]
                self.move_action()
                self.hide_indicators()
        self.check()
        self.checkmate()
        self.stalemate()

    # labels
    def create_chessboard_labels(self) -> list:
        background: list = []
        for y in range(len(self.chess.chessboard)):
            background.append([])
            for x in range(len(self.chess.chessboard)):
                background[y].append(
                    self.new_label(x * 100, y * 100, 100, 100, 'gs' if (y + x) % 2 else 'ws'))
                background[y][x].show()
        return background

    def create_pieces_labels(self) -> list:
        pieces: list = []
        for y in range(len(self.chess.chessboard)):
            pieces.append([])
            for x in range(len(self.chess.chessboard)):
                pieces[y].append(QLabel(self))
                if self.chess.chessboard[y][x] != '--':
                    pieces[y][x] = self.new_label(x * 100, y * 100, 100, 100, self.chess.chessboard[y][x])
                    pieces[y][x].show()
        return pieces

    def create_indicators(self, label: str) -> list:
        indicators: list = []
        for y in range(len(self.chess.chessboard)):
            indicators.append([])
            for x in range(len(self.chess.chessboard)):
                indicators[y].append(self.new_label(x * 100, y * 100, 100, 100, label))
                indicators[y][x].hide()
        return indicators

    def new_label(self, x: int, y: int, width: int, height: int, img: str) -> QLabel:
        label = QLabel(self)
        label.setPixmap(QPixmap(image(img)).scaled(100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        label.resize(width, height)
        label.move(x, y)
        return label

    # INDICATORS
    def fill_buffers(self) -> None:
        move_set: set = Position(self.chess.chessboard, self.x1, self.y1, self.chess.chessboard[self.x1][self.y1]).move_set()
        move_set = MovementControl().verify_move_to_avoid_check(self.x1, self.y1, move_set, self.chess.chessboard.copy())
        for cell in move_set:
            if exists(cell):
                if self.chess.chessboard[cell[0]][cell[1]] == '--':
                    self.position_buffer.append(cell)
                elif self.chess.chessboard[cell[0]][cell[1]] != '--' and self.chess.chessboard[cell[0]][cell[1]][1] != 'K':
                    self.hit_buffer.append(cell)
                elif self.chess.chessboard[cell[0]][cell[1]][1] == 'K':
                    self.check_buffer = list(cell)

    def show_indicators(self) -> None:
        self.show_pick_indicator()
        self.show_position_indicators()
        self.show_hit_indicators()
        self.show_check_indicator()

    def hide_indicators(self) -> None:
        self.hide_pick_indicator()
        self.hide_position_indicators()
        self.hide_hit_indicators()
        self.hide_check_indicator()

    # PICK indicator
    def show_pick_indicator(self) -> None:
        self.pick_indicators[self.x1][self.y1].show()

    def hide_pick_indicator(self) -> None:
        self.pick_indicators[self.x1][self.y1].hide()

    # CHECK indicator
    def show_check_indicator(self) -> None:
        if len(self.check_buffer) != 0:
            self.check_indicators[self.check_buffer[0]][self.check_buffer[1]].show()

    def hide_check_indicator(self) -> None:
        if len(self.check_buffer) != 0:
            self.check_indicators[self.check_buffer[0]][self.check_buffer[1]].hide()
            self.check_buffer.clear()

    # HIT indicator
    def show_hit_indicators(self) -> None:
        for cell in self.hit_buffer:
            self.hit_indicators[cell[0]][cell[1]].show()

    def hide_hit_indicators(self) -> None:
        for cell in self.hit_buffer:
            self.hit_indicators[cell[0]][cell[1]].hide()
        self.hit_buffer.clear()

    # POSITION indicator
    def show_position_indicators(self) -> None:
        for cell in self.position_buffer:
            self.position_indicators[cell[0]][cell[1]].show()

    def hide_position_indicators(self) -> None:
        for cell in self.position_buffer:
            self.position_indicators[cell[0]][cell[1]].hide()
        self.position_buffer.clear()

    # figure move
    def move_action(self) -> None:
        if (self.x2, self.y2) in self.position_buffer or (self.x2, self.y2) in self.hit_buffer:
            self.is_hit()
            self.move_figure()
            self.update_log()
        else:
            self.move_buffer.clear()

    def is_hit(self) -> None:
        if self.chess.chessboard[self.x2][self.y2] != '--':
            self.pieces_labels[self.x2][self.y2].hide()
            self.chess.chessboard[self.x2][self.y2] = '--'

    def move_figure(self) -> None:
        self.chess.chessboard[self.x2][self.y2] = self.chess.chessboard[self.x1][self.y1]
        self.chess.chessboard[self.x1][self.y1] = '--'
        self.move_figure_label()

    def move_figure_label(self) -> None:
        self.pieces_labels[self.x2][self.y2] = self.pieces_labels[self.x1][self.y1]
        self.pieces_labels[self.x1][self.y1] = QLabel(self)
        self.pieces_labels[self.x2][self.y2].move(self.y2 * 100, self.x2 * 100)
        self.hide_position_indicators()
        self.move_buffer.clear()

    # game log
    def update_log(self):
        self.turn += 1
        self.log_file.write(
            str(self.turn) + '. ' +
            self.chess.chessboard[self.x2][self.y2] + ' ' +
            self.chess.square_names[self.x1][self.y1] + '->' +
            self.chess.square_names[self.x2][self.y2] + '\n'
        )

    # END-GAME procedures
    def check(self):
        if MovementControl().check('w', self.chess.chessboard) and len(self.check_buffer) != 2:
            self.check_buffer.append(self.chess.pos('wK')[0])
            self.check_buffer.append(self.chess.pos('wK')[1])
            self.show_check_indicator()
        elif MovementControl().check('b', self.chess.chessboard) and len(self.check_buffer) != 2:
            self.check_buffer.append(self.chess.pos('bK')[0])
            self.check_buffer.append(self.chess.pos('bK')[1])
            self.show_check_indicator()
        else:
            self.hide_check_indicator()

    def checkmate(self):
        if MovementControl().zero_moves('w', self.chess.chessboard):
            if MovementControl().check('w', self.chess.chessboard):
                self.checkmate_indicators[self.chess.pos('wK')[0]][self.chess.pos('wK')[1]].show()
        elif MovementControl().zero_moves('b', self.chess.chessboard):
            if MovementControl().check('b', self.chess.chessboard):
                self.checkmate_indicators[self.chess.pos('bK')[0]][self.chess.pos('bK')[1]].show()

    def stalemate(self):
        if MovementControl().zero_moves('b', self.chess.chessboard):
            if not MovementControl().check('b', self.chess.chessboard):
                for r in range(len(self.chess.chessboard)):
                    for c in range(len(self.chess.chessboard)):
                        if self.chess.chessboard[r][c][0] == 'b':
                            if self.chess.chessboard[r][c][1] == 'K':
                                self.checkmate_indicators[r][c].show()
                            else:
                                self.stalemate_indicators[r][c].show()
        elif MovementControl().zero_moves('w', self.chess.chessboard):
            if not MovementControl().check('w', self.chess.chessboard):
                for r in range(len(self.chess.chessboard)):
                    for c in range(len(self.chess.chessboard)):
                        if self.chess.chessboard[r][c][0] == 'w':
                            if self.chess.chessboard[r][c][1] == 'K':
                                self.checkmate_indicators[r][c].show()
                            else:
                                self.stalemate_indicators[r][c].show()
