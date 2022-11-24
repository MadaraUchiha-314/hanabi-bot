from enum import Enum
from typing import Dict, Union

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


class Card:
    color: CardColor
    number: CardNumber

    # Hints: True indicate possible values
    hints: Dict[Union[CardColor, CardNumber], bool]

    def __init__(self, color, number):
        self.color = color
        self.number = number

        self.hints = {}
        for color in CardColor:
            self.hints[color] = True
        for number in CardNumber:
            self.hints[number] = True

    def __str__(self):
        return f'{self.color.value[0]}{self.number.value}'

    def hints_str(self):
        color_hints = [color.value[0] for color in CardColor if self.hints[color]]
        number_hints = [number.value[0] for number in CardNumber if self.hints[number]]
        return f"{''.join(color_hints)} {''.join(number_hints)}"
