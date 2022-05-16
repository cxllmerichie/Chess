from PyQt5.QtWidgets import QWidget, QLabel, QMessageBox
from PyQt5.QtCore import QSize, Qt
from Common.Library import game_btn, str_time_to_float, text_label, TimerState
from Common.Constants import GAME_TIME, S, FRAMERATE, TimePrecision
from string import ascii_uppercase
from ClientSingleplayer.ChessGUI import ChessGUI
from threading import Thread
from contextlib import redirect_stdout
with redirect_stdout(None):
    from pygame.time import Clock


class ChessGame(QWidget):
    def __init__(self, parent_window: QWidget):
        super(ChessGame, self).__init__(parent=parent_window)
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setFixedSize(QSize(S * 10, S * 10))

        self.text_labels()
        self.buttons()
        self.clock: Clock = Clock()
        self.timers: dict = {'w': Timer(text_label(GAME_TIME, Qt.AlignHCenter | Qt.AlignBottom, (S * 4, S * 9), QSize(S * 2, S), self)),
                             'b': Timer(text_label(GAME_TIME, Qt.AlignHCenter | Qt.AlignTop, (S * 4, 0), QSize(S * 2, S), self))}

        self.chessgui = ChessGUI(self)
        self.chessgui.installEventFilter(self.chessgui)
        self.hide()

    def disable_timers(self):
        self.chessgui.enable_mouse_click = False
        self.timers['w'].label.hide()
        self.timers['b'].label.hide()
        self.chessgui.enable_mouse_click = True
        print('DISABLED')

    def enable_timers(self):
        self.chessgui = ChessGUI(self)
        self.timers['w'].time = '10:00.00'
        self.timers['b'].time = '10:00.00'
        self.timers['w'].label.setText(self.timers['w'].time)
        self.timers['b'].label.setText(self.timers['b'].time)
        self.timers['w'].label.show()
        self.timers['b'].label.show()
        self.start_game()
        print('ENABLED')

    def reset_game(self):
        self.chessgui.enable_mouse_click = False
        self.timers['w'].time = '10:00.00'
        self.timers['b'].time = '10:00.00'
        self.timers['w'].label.setText(self.timers['w'].time)
        self.timers['b'].label.setText(self.timers['b'].time)
        self.timers['w'].label.show()
        self.timers['b'].label.show()
        self.chessgui = ChessGUI(self)
        self.start_game()
        print('RESET')

    def closeEvent(self, event):
        self.end_game()
        event.accept()

    def start_game(self):
        Thread(target=lambda: self.timer_control()).start()

    def timer_control(self):
        while self.chessgui.enable_mouse_click and str_time_to_float(self.timers['b'].time) > 0 and str_time_to_float(self.timers['w'].time) > 0:
            if self.chessgui.chess.chessboard[self.chessgui.chess.last_move[1][0]][self.chessgui.chess.last_move[1][1]][0] == 'b':
                print(f'Last: {self.chessgui.chess.chessboard[self.chessgui.chess.last_move[1][0]][self.chessgui.chess.last_move[1][1]][0]}, B pause, W resume')
                self.timers['b'].pause()
                self.timers['w'].resume()
            else:
                print(f'Last: {self.chessgui.chess.chessboard[self.chessgui.chess.last_move[1][0]][self.chessgui.chess.last_move[1][1]][0]}, W pause, B resume')
                self.timers['w'].pause()
                self.timers['b'].resume()
            self.clock.tick(FRAMERATE)
        self.end_game()

    def text_labels(self):
        for i in range(1, 9, 1):
            text_label(str(ascii_uppercase[i - 1]), Qt.AlignHCenter | Qt.AlignBottom, (i * S, 0), QSize(S, S), self)
            text_label(str(ascii_uppercase[i - 1]), Qt.AlignHCenter | Qt.AlignTop, (S * i, S * 9), QSize(S, S), self)
            text_label(str(9 - i), Qt.AlignVCenter | Qt.AlignLeft, (S * 9 + 0.1 * S, S * i), QSize(0.9 * S, S), self)
            text_label(str(9 - i), Qt.AlignVCenter | Qt.AlignRight, (0, S * i), QSize(0.9 * S, S), self)

    def buttons(self):
        game_btn('Draw by agreement', (S, S * 9 + S / 2, S * 2, S / 4),
                   lambda: self.end_game_message(QMessageBox.Question, 'Draw by agreement', 'Do you agree for a draw?'), self)
        game_btn('Resign', (S, S * 9 + S / 2 + S / 4, S * 2, S / 4),
                   lambda: self.end_game_message(QMessageBox.Warning, 'Resignation', 'Do you want to resign?'), self)
        game_btn('VolumeUp', (S * 9, S * 9 + S / 4, S, S / 4),
                   lambda: self.chessgui.audio_player.setVolume(self.chessgui.audio_player.volume() + 10), self)
        game_btn('VolumeDown', (S * 9, S * 10 - S / 2, S, S / 4),
                   lambda: self.chessgui.audio_player.setVolume(self.chessgui.audio_player.volume() - 10), self)
        game_btn('Mute', (S * 9, S * 10 - S / 4, S, S / 4),
                   lambda: self.chessgui.audio_player.setVolume(0 if self.chessgui.audio_player.volume() != 0 else 100), self)

    def end_game_message(self, icon_type, title: str, text: str) -> None:
        msg = QMessageBox()
        msg.setIcon(icon_type)
        msg.setText(text)
        msg.setWindowTitle(title)
        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        if msg.exec_() == QMessageBox.Yes:
            self.end_game()

    def end_game(self):
        self.chessgui.enable_mouse_click = False
        self.timers['w'].stop()
        self.timers['b'].stop()


class Timer:
    def __init__(self, label: QLabel):
        self.label: QLabel = label
        self.time: str = label.text()
        self.state: TimerState = TimerState.Stopped
        self.thread: Thread = Thread(target=lambda: self.countdown(amount=str_time_to_float(self.time)))
        self.clock: Clock = Clock()

    def countdown(self, amount: float = 600) -> None:
        while amount > 0 and self.state is not TimerState.Stopped:
            minutes, seconds_milliseconds = divmod(amount, 60)
            seconds, milliseconds = divmod(seconds_milliseconds, 1)
            self.label.setText('{:02.0f}:{:02.0f}.{:02.0f}'.format(minutes, seconds, milliseconds * 1000)[:TimePrecision.MinSecMilli])
            self.clock.tick(100)
            amount -= 0.01
            if amount <= 0:
                self.label.setText('00:00.00')
                self.time = '00:00.00'
                self.stop()

    def start(self) -> None:
        if self.state is TimerState.Started:
            return None
        print(f'Start: {self.time}, {self.label.text()}')
        self.state = TimerState.Started
        self.thread = Thread(target=lambda: self.countdown(amount=str_time_to_float(self.time)))
        self.thread.start()

    def stop(self) -> None:
        if self.state is TimerState.Stopped:
            return None
        print(f'Stop: {self.time}, {self.label.text()}')
        self.state = TimerState.Stopped
        try:
            self.thread.join()
        except RuntimeError:
            pass

    def pause(self) -> None:
        if self.state is TimerState.Paused or self.state is TimerState:
            return None
        print(f'Pause: {self.time}, {self.label.text()}')
        self.state = TimerState.Paused
        self.time = self.label.text()
        self.stop()

    def resume(self) -> None:
        if self.state is TimerState.Resumed or self.state is TimerState.Started:
            return None
        print(f'Resume: {self.time}, {self.label.text()}')
        self.state = TimerState.Resumed
        self.thread: Thread = Thread(target=lambda: self.countdown(amount=str_time_to_float(self.time)))
        self.start()
