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
FRAMERATE: Final = 200
GAME_TIME: Final = '10:00.00'
TIME_FORMAT: int = TimePrecision.MinSecMilli.value  # show minutes and/or seconds and/or milliseconds
BH: Final = 50  # button height
BW: Final = 300  # button width

ICON: Final = 'Assets/Images/Application/icon.svg'
SOUND_PATH: Final = '/Assets/SoundEffects'
MENU_BACKGROUND: Final = 'Assets/Images/Application/wallpaper.jpg'
GAME_BACKGROUND: Final = 'Assets/Images/Application/background.svg'
SETTINGS_BACKGROUND: Final = 'Assets/Images/Application/settings.svg'
