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

    def __str__(self):
        if self.move_type == MoveType.HINT:
            return f'hinted player {self.target_player} -- {self.move_detail.value}'
        elif self.move_type == MoveType.DISCARD:
            return f'discarded {self.move_detail}'
        elif self.move_type == MoveType.PLAY:
            return f'played {self.move_detail}'


@dataclass
class PlayedMove:
    player_num: int
    move: Move
