ENCODING: str = 'utf-8'
CONNECTION_LIMIT: int = 100
BYTES: int = 1024
# '[0]fromX(),[1]from(),[2]toX(),[3]toY(),[4]PROMOTIONAL_PIECE,[5]SELF_COLOR,[6]READY_STATE'
DEFAULT: str = '0,0,0,0,  , ,'


class Message:
    DISCONNECT: str = 'DISCONNECT'
    RESIGN: str = 'RESIGN'
    SUGGESTDRAW: str = 'SUGGESTDRAW'
    ACCEPTEDDRAW: str = 'ACCEPTEDDRAW'
    WIN: str = 'WIN'
    DEFEAT: str = 'DEFEAT'
