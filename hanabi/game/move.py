from enum import Enum
from typing import Union

from hanabi.game.card import CardColor, CardNumber


class MoveType(Enum):
    DISCARD = 'discard'
    HINT = 'hint'
    PLAY = 'play'


class Move:
    move_type: MoveType
    move_detail: Union[CardColor, CardNumber]
    target_player: int

