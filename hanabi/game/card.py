from enum import Enum
from typing import Dict, Union, Optional

from dataclasses import dataclass

CardIndex = int


class CardNumber(Enum):
    ONE = '1'
    TWO = '2'
    THREE = '3'
    FOUR = '4'
    FIVE = '5'


class CardColor(Enum):
    BLUE = 'Blue'
    GREEN = 'Green'
    RED = 'Red'
    YELLOW = 'Yellow'
    WHITE = 'White'

@dataclass
class Card:
    color: Optional[CardColor]
    number: Optional[CardNumber]

    # Hints: True indicate possible values
    hints: Dict[Union[CardColor, CardNumber], bool]

    def __init__(self, color = None, number = None, hints = None):
        self.color = color
        self.number = number
        if hints != None:
            self.hints = hints
        else:
            self.hints = {}
            for color in CardColor:
                self.hints[color] = True
            for number in CardNumber:
                self.hints[number] = True
    
    def get(self, isMaked = False):
        if not isMaked:
            return self
        return Card(
            color=None,
            number=None,
            hints=self.hints,
        )

    def __str__(self):
        return f'{self.color.value[0]}{self.number.value}'

    def hints_str(self):
        color_hints = [color.value[0] for color in CardColor if self.hints[color]]
        number_hints = [number.value[0] for number in CardNumber if self.hints[number]]
        return f"{''.join(color_hints)} {''.join(number_hints)}"

    def __eq__(self, other):
        return self.color == other.color and self.number == other.number
