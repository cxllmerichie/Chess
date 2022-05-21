from pyautogui import size
from typing import Final


COEFFICIENT: Final = 15
SW, SH = size().width, size().height  # screen width & screen height
S: Final = int(SH / COEFFICIENT // 10 * 10) if SH < SW else int(SW / COEFFICIENT // 10 * 10)  # square size (label size)
FS: Final = int(S / 4)  # general font size
FRAMERATE: Final = 200
BH: Final = 50  # button height
BW: Final = 300  # button width

ICON: Final = 'Assets/Images/Application/icon.svg'
SOUND_PATH: Final = '/Assets/SoundEffects'
MENU_BACKGROUND: Final = 'Assets/Images/Application/wallpaper.jpg'
GAME_BACKGROUND: Final = 'Assets/Images/Application/background.svg'
SETTINGS_BACKGROUND: Final = 'Assets/Images/Application/settings.svg'
