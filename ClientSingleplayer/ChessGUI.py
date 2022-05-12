from PyQt5.QtWidgets import QWidget, QLabel
from PyQt5.QtCore import QSize, Qt, QEvent, QUrl
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from ClientSingleplayer.ChessLogic import ChessLogic
from Common.Library import exist, image_label, sound, operate
from Common.Constants import S


x1 = y1 = x2 = y2 = 0
move_buffer, check_buffer, position_buffer, capture_buffer = [], [], [], []


class ChessGUI(QWidget):
    #def __init__(self, parent_window: QWidget, log_file):
    def __init__(self, parent_window: QWidget):
        super(ChessGUI, self).__init__(parent=parent_window)
        self.audio_player = QMediaPlayer()
        self.sound: str = ''
        self.enable_mouse_click: bool = True

        self.chess: ChessLogic = ChessLogic()
        self.label: Label = Label(self, self.chess)
        #self.log_file = log_file
        self.turn: int = 1
        self.color = '?'

        self.move(S, S)
        self.setFixedSize(QSize(S * 8, S * 8))
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.show()

    # user interaction
    # @DECORATOR
    def mousePressEvent(self, click) -> None:
        global x1, x2, y1, y2, move_buffer
        if self.color == 'w' and self.turn % 2 != 1:
            return None
        elif self.color == 'b' and self.turn % 2 != 0:
                return None
        if not (len(move_buffer) == 0 and self.chess.chessboard[click.y() // S][click.x() // S] == '--'):
            if not (len(move_buffer) == 0 and self.chess.chessboard[click.y() // S][click.x() // S][0] == self.chess.chessboard[self.chess.last_move[1][0]][self.chess.last_move[1][1]][0]):
                move_buffer.append([click.y() // S, click.x() // S])
                x1, y1 = move_buffer[0][0], move_buffer[0][1]
                self.fill_buffers()
                self.label.show_indicators()
                if len(move_buffer) == 2:
                    x2, y2 = move_buffer[1][0], move_buffer[1][1]
                    is_moved: bool = self.move_action()
                    self.label.hide_indicators()
                    self.end_game_procedures()
                    if is_moved:
                        self.turn += 1
                        self.chess.last_move = [(x1, y1), (x2, y2)]
                        self.play_sound(self.sound)

    # @DECORATOR
    def eventFilter(self, obj, event) -> bool:
        if not self.enable_mouse_click:
            if event.type() in (QEvent.MouseButtonPress, QEvent.MouseButtonDblClick):
                if event.timer_control() == Qt.LeftButton:
                    return True
        return super(ChessGUI, self).eventFilter(obj, event)

    # INDICATORS
    def fill_buffers(self) -> None:
        global check_buffer, x1, x1
        for cell in self.chess.move_set(x1, y1):
            if exist(cell):
                if self.chess.chessboard[cell[0]][cell[1]] == '--' and\
                        not (abs(cell[0]-x1) == abs(cell[1]-y1) == 1 and self.chess.chessboard[x1][y1][1] == 'p'):
                    position_buffer.append(cell)
                elif self.chess.chessboard[cell[0]][cell[1]][1] == 'K':
                    check_buffer = list(cell)
                elif self.chess.chessboard[cell[0]][cell[1]] != '--' or\
                        (abs(cell[0]-x1) == abs(cell[1]-y1) == 1 and self.chess.chessboard[x1][y1][1] == 'p'):
                    capture_buffer.append(cell)

    # piece move
    def move_action(self) -> bool:
        if (x2, y2) in position_buffer or (x2, y2) in capture_buffer:
            self.sound = 'move'
            if not self.is_castling():
                captured: bool = self.is_capture()
                promoted: bool = self.is_promotion()
                if not captured and not promoted:
                    self.is_en_passant()
            self.move_piece()
            #self.update_log()
            return True
        move_buffer.clear()
        return False

    def is_promotion(self) -> bool:
        if self.chess.chessboard[x1][y1][1] == 'p':
            if (self.chess.chessboard[x1][y1][0] == 'w' and x2 == 0) or (self.chess.chessboard[x1][y1][0] == 'b' and x2 == 7):
                self.enable_mouse_click = False
                Promotion(self, (x2, y2), self.chess.chessboard[x1][y1])
                self.sound = 'castling'
                return True
        return False

    def is_capture(self) -> bool:
        if self.chess.chessboard[x2][y2] != '--':
            self.label.pieces[x2][y2].hide()
            self.chess.chessboard[x2][y2] = '--'
            self.sound = 'capture'
            return True
        return False

    def is_castling(self) -> bool:
        rp, ep = [], []
        if self.chess.chessboard[x1][y1] == 'wK':
            if x1 == 7 and y1 == 4 and x2 == 7 and y2 == 6:
                rp, ep = [7, 7], [7, 5]
            elif x1 == 7 and y1 == 4 and x2 == 7 and y2 == 2:
                rp, ep = [7, 0], [7, 3]
        elif self.chess.chessboard[x1][y1] == 'bK':
            if x1 == 0 and y1 == 4 and x2 == 0 and y2 == 6:
                rp, ep = [0, 7], [0, 5]
            elif x1 == 0 and y1 == 4 and x2 == 0 and y2 == 2:
                rp, ep = [0, 0], [0, 3]
        if len(rp) == len(ep) == 2:
            self.chess.chessboard[ep[0]][ep[1]], self.chess.chessboard[rp[0]][rp[1]] =\
                self.chess.chessboard[rp[0]][rp[1]], self.chess.chessboard[ep[0]][ep[1]]
            self.label.pieces[ep[0]][ep[1]], self.label.pieces[rp[0]][rp[1]] =\
                self.label.pieces[rp[0]][rp[1]], self.label.pieces[ep[0]][ep[1]]
            self.label.pieces[ep[0]][ep[1]].move(ep[1] * S, ep[0] * S)
            self.sound = 'castling'
            return True
        return False

    def is_en_passant(self) -> bool:
        if self.chess.chessboard[x2][y2] == '--' and abs(y1-y2) == 1:
            operator = '+' if self.chess.chessboard[x1][y1] == 'wp' else '-'
            if self.chess.chessboard[x1][y1][1] == 'p':
                x = operate(x2, operator, 1)
                self.label.pieces[x][y2].hide()
                self.label.pieces[x][y2] = QLabel(self)
                self.chess.chessboard[x][y2] = '--'
                self.sound = 'capture'
                return True
        return False

    def move_piece(self) -> None:
        self.chess.chessboard[x2][y2], self.chess.chessboard[x1][y1] =\
            self.chess.chessboard[x1][y1], self.chess.chessboard[x2][y2]
        self.move_piece_label()

    def move_piece_label(self) -> None:
        self.label.pieces[x2][y2], self.label.pieces[x1][y1] = self.label.pieces[x1][y1], self.label.pieces[x2][y2]
        self.label.pieces[x2][y2].move(y2 * S, x2 * S)
        self.label.hide_position()
        move_buffer.clear()

    def play_sound(self, action: str):
        self.audio_player.setMedia(QMediaContent(QUrl.fromLocalFile(sound(action))))
        self.audio_player.play()

    """# game log
    def update_log(self) -> None:
        self.turn += 1
        self.log_file.write(f"{self.turn}. {self.chess.chessboard[x2][y2]} {self.chess.square_names[x1][y1]}->{self.chess.square_names[x2][y2]}\n")
"""
    # END-GAME procedures
    def end_game_procedures(self) -> bool:
        if self.checkmate() or self.stalemate():
            self.enable_mouse_click = False
            return True
        return self.check()

    def check_for(self, piece: str) -> None:
        global check_buffer
        check_buffer = list(self.chess.position(piece))
        self.label.show_check()
        self.sound = 'check'

    def check(self) -> bool:
        if self.chess.is_check_for('w'):
            self.check_for('wK')
            return True
        elif self.chess.is_check_for('b'):
            self.check_for('bK')
            return True
        self.label.hide_check()
        return False

    def checkmate_for(self, piece: str) -> bool:
        if self.chess.empty_move_set_for(piece[0]) and self.chess.is_check_for(piece[0]):
            self.label.checkmate[self.chess.position(piece)[0]][self.chess.position(piece)[1]].show()
            self.sound = 'check'
            return True
        return False

    def checkmate(self) -> bool:
        return self.checkmate_for('wK') or self.checkmate_for('bK')

    def stalemate_for(self, color: str) -> bool:
        if self.chess.empty_move_set_for(color) and not self.chess.is_check_for(color):
            for r in range(len(self.chess.chessboard)):
                for c in range(len(self.chess.chessboard)):
                    if self.chess.chessboard[r][c][0] == color:
                        self.label.stalemate[r][c].show()
            self.sound = 'check'
            return True
        return False

    def stalemate(self) -> bool:
        return self.stalemate_for('w') or self.stalemate_for('b')


class Promotion(QWidget):
    def __init__(self, _window: QWidget, position: tuple, piece: str):
        self.window: QWidget = _window
        self.color: str = piece[0]
        self.x = position[0]
        self.y = position[1]
        super(Promotion, self).__init__(self.window)

        self.case: list = [(0, 'Q'), (S, 'R'), (S * 2, 'N'), (S * 3, 'B')] if self.color == 'w' else [(0, 'B'), (S, 'N'), (S * 2, 'R'), (S * 3, 'Q')]
        for _tuple in self.case:
            image_label(0, _tuple[0], S, S, 'promotion', self).show()
            image_label(0, _tuple[0], S, S, self.color + _tuple[1], self).show()

        self.move(self.y * S, 0) if self.color == 'w' else self.move(self.y * S, S * 4)
        self.setFixedSize(QSize(S, S * 4))
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.show()

    # @DECORATOR
    def mousePressEvent(self, click):
        self.window.enable_mouse_click = True
        piece: str = self.color + self.case[click.y() // S][1]
        self.promotional_replacement(piece)
        self.hide()

    def promotional_replacement(self, _piece: str):
        self.window.chess.chessboard[self.x][self.y] = _piece
        self.window.label.pieces[self.x][self.y].hide()
        self.window.label.pieces[self.x][self.y] = image_label(self.y * S, self.x * S, S, S, _piece, self.window)
        self.window.label.pieces[self.x][self.y].show()
        if self.window.end_game_procedures():
            self.window.play_sound('check')


class Label:
    def __init__(self, window: QWidget, chess: ChessLogic):
        self.background: list = self.create_background(window, chess)
        self.position: list = self.create_indicators('position', window, chess)
        self.check: list = self.create_indicators('check', window, chess)
        self.choice: list = self.create_indicators('choice', window, chess)
        self.checkmate: list = self.create_indicators('checkmate', window, chess)
        self.stalemate: list = self.create_indicators('stalemate', window, chess)
        self.capture: list = self.create_indicators('capture', window, chess)
        self.pieces: list = self.create_pieces(window, chess)

    # labels
    @staticmethod
    def create_background(window: QWidget, chess: ChessLogic) -> list:
        _background: list = []
        for y in range(len(chess.chessboard)):
            _background.append([])
            for x in range(len(chess.chessboard)):
                _background[y].append(
                    image_label(x * S, y * S, S, S, 'dark' if (y + x) % 2 else 'light', window))
                _background[y][x].show()
        return _background

    @staticmethod
    def create_pieces(window: QWidget, chess: ChessLogic) -> list:
        _pieces: list = []
        for y in range(len(chess.chessboard)):
            _pieces.append([])
            for x in range(len(chess.chessboard)):
                _pieces[y].append(QLabel(parent=window))
                if chess.chessboard[y][x] != '--':
                    _pieces[y][x] = image_label(x * S, y * S, S, S, chess.chessboard[y][x], window)
                    _pieces[y][x].show()
        return _pieces

    @staticmethod
    def create_indicators(label: str, window: QWidget, chess: ChessLogic) -> list:
        indicators: list = []
        for y in range(len(chess.chessboard)):
            indicators.append([])
            for x in range(len(chess.chessboard)):
                indicators[y].append(image_label(x * S, y * S, S, S, label, window))
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
