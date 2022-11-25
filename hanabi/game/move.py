from dataclasses import dataclass
from enum import Enum
from typing import Union

from hanabi.game.card import CardColor, CardNumber, CardIndex


class MoveType(Enum):
    DISCARD = 'discard'
    HINT = 'hint'
    PLAY = 'play'


@dataclass
class HintMoveType(Enum):
    Color = 'Color'
    Number = 'Number'


@dataclass
class HintCardColor:
    card_color: CardColor


@dataclass
class HintCardNumber:
    card_number: CardNumber


@dataclass
class HintCardMove:
    hint_move_type: HintMoveType
    hint_move_detail: Union[HintCardColor, HintCardNumber]

    def __str__(self):
        if isinstance(self.hint_move_detail, HintCardColor):
            return f'card color is {self.hint_move_detail.card_color}'
        else:
            return f'card number is {self.hint_move_detail.card_number}'


@dataclass
class DiscardCardMove:
    card_index: CardIndex

    def __str__(self):
        return str(self.card_index)


@dataclass
class PlayCardMove:
    card_index: CardIndex

    def __str__(self):
        return str(self.card_index)


@dataclass
class Move:
    move_type: MoveType
    move_detail: Union[HintCardMove, DiscardCardMove, PlayCardMove]
    target_player: int

    def __str__(self):
        if self.move_type == MoveType.HINT:
            return f'hinted player {self.target_player} -- {self.move_detail}'
        elif self.move_type == MoveType.DISCARD:
            return f'discarded {self.move_detail}'
        elif self.move_type == MoveType.PLAY:
            return f'played {self.move_detail}'
    
    def __lt__(self, other):
        return False


@dataclass
class PlayedMove:
    player_num: int
    move: Move
