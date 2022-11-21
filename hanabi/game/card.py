from enum import Enum


class CardNumber(Enum):
    ONE = 1
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5


class CardColor(Enum):
    BLUE = 'blue'
    GREEN = 'green'
    RED = 'red'
    YELLOW = 'yellow'
    WHITE = 'white'


class Card:
    number: CardNumber
    color: CardColor
    is_critical: bool
