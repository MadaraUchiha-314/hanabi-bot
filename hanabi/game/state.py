from dataclasses import dataclass
from typing import List

from hanabi.game.card import Card


@dataclass
class State:
    deck: List[Card]
    played_cards: List[int]
    discarded_cards: List[Card]
    player_cards: List[List[Card]]

    player_turn: int

    hint_tokens: int
    penalty_tokens: int

