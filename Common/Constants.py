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
TICK_PERIOD: Final = float(0.1)
GAME_TIME: Final = str('10:00.00')
TIME_FORMAT: int = TimePrecision.MinSecMilli.value  # show minutes and/or seconds and/or milliseconds
IMAGE_PATH: Final = str('Assets/Images/Standard/')
SOUND_PATH: Final = str('/Assets/SoundEffects')
MENU_BACKGROUND: Final = IMAGE_PATH + 'wallpaper.jpg'
GAME_BACKGROUND: Final = IMAGE_PATH + 'background.png'
BH: Final = int(50)  # button height
BW: Final = int(300)  # button width
ICON: str = 'Assets/Images/icon.jpg'