from pyautogui import size
from typing import Final
from enum import Enum


class TimePrecision(Enum):
    Min = 2
    MinSec = 5
    MinSecMilli = 8


COEFFICIENT: Final = 15
SW, SH = size().width, size().height  # screen width & screen height
S: Final = int(SH / COEFFICIENT // 10 * 10) if SH < SW else int(SW / COEFFICIENT // 10 * 10)  # square size (label size)
FS: Final = int(S / 4)  # general font size
FRAMERATE: Final = int(200)
GAME_TIME: Final = str('10:00.00')
TIME_FORMAT: int = TimePrecision.MinSecMilli.value  # show minutes and/or seconds and/or milliseconds
BH: Final = int(50)  # button height
BW: Final = int(300)  # button width

CHESSBOARD_STYLE: str = 'standard'
CHESSBOARD_PATH: str = f'Assets/Images/Chessboard/{CHESSBOARD_STYLE}/'
ICON: str = 'Assets/Images/Application/icon.svg'
# Standard: standardhd
# Canonical: cardinal chessnut fresca icpieces kosal merida
# Specific: fantasy pirouetti riohacha spatial
# Strange but interesting: horsey letter shapes
PIECE_STYLE: str = 'standardhd'
PIECE_PATH: str = f'Assets/Images/Pieces/{PIECE_STYLE}/'
INDICATOR_STYLE: str = 'standardhd'
INDICATOR_PATH: str = f'Assets/Images/Indicators/{INDICATOR_STYLE}/'
SOUND_PATH: Final = str('/Assets/SoundEffects')
MENU_BACKGROUND: Final = 'Assets/Images/Application/wallpaper.jpg'
GAME_BACKGROUND: Final = 'Assets/Images/Application/background.svg'
SETTINGS_BACKGROUND: Final = 'Assets/Images/Application/settings.svg'


def set_piece_style(style: str):
    global PIECE_STYLE, PIECE_PATH
    PIECE_STYLE = style
    PIECE_PATH = f'Assets/Images/Pieces/{PIECE_STYLE}/'


def set_chessboard_style(style: str):
    global CHESSBOARD_STYLE, CHESSBOARD_PATH
    CHESSBOARD_STYLE = style
    CHESSBOARD_PATH = f'Assets/Images/Chessboard/{CHESSBOARD_STYLE}/'
