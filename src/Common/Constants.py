from pyautogui import size
from typing import Final

PATH_PREFIX: str = ''
COEFFICIENT: Final = 15
SW, SH = size().width, size().height  # screen width & screen height
S: Final = int(SH / COEFFICIENT // 10 * 10) if SH < SW else int(SW / COEFFICIENT // 10 * 10)  # square size (label size)
FS: Final = int(S / 4)  # general font size
FRAMERATE: Final = 200
BH: Final = 50  # button height
BW: Final = 300  # button width

ICON: Final = f'{PATH_PREFIX}Assets/Images/Application/icon.svg'
if len(PATH_PREFIX) == 3:
    SOUND_PATH: Final = f'./Assets/SoundEffects'
elif len(PATH_PREFIX) == 0:
    SOUND_PATH: Final = f'{PATH_PREFIX}/Assets/SoundEffects'
MENU_BACKGROUND: Final = f'{PATH_PREFIX}Assets/Images/Application/wallpaper.jpg'
GAME_BACKGROUND: Final = f'{PATH_PREFIX}Assets/Images/Application/background.svg'
SETTINGS_BACKGROUND: Final = f'{PATH_PREFIX}Assets/Images/Application/settings.svg'
