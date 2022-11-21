from dataclasses import dataclass
from enum import Enum

# hax
CardIndex = int


class CardNumber(Enum):
    ONE = 1
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5

    @staticmethod
    def multiplicity(number: "CardNumber") -> int:
        if number == CardNumber.ONE:
            return 3
        elif number == CardNumber.FIVE:
            return 1
        else:
            return 2


class CardColor(Enum):
    BLUE = 'Blue'
    GREEN = 'Green'
    RED = 'Red'
    YELLOW = 'Yellow'
    WHITE = 'White'


@dataclass
class Card:
    color: CardColor
    number: CardNumber

    def __str__(self):
        return f'{self.color.value[0]}{self.number.value}'
