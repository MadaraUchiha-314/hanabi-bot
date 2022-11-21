from dataclasses import dataclass
from enum import Enum
from typing import Union

from hanabi.game.card import CardColor, CardNumber, CardIndex


class MoveType(Enum):
    DISCARD = 'discard'
    HINT = 'hint'
    PLAY = 'play'


@dataclass
class Move:
    move_type: MoveType
    move_detail: Union[CardColor, CardNumber, CardIndex]
    target_player: int

