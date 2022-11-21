from dataclasses import dataclass
from typing import List

from tabulate import tabulate

from hanabi.game.card import Card, CardColor


@dataclass
class State:
    deck: List[Card]
    played_cards: List[int]
    discarded_cards: List[Card]
    player_cards: List[List[Card]]

    current_player: int

    hint_tokens: int
    penalty_tokens: int

    def __str__(self):
        result = ''
        result += "Played cards: \n"
        colors = [color.value for color in self.played_cards.keys()]
        result += tabulate([self.played_cards.values()], headers=colors)

        result += "\n\nDiscarded cards: \n"
        for card in self.discarded_cards:
            result += f'{str(card)} '
        if len(self.discarded_cards) == 0:
            result += "<empty>"

        result += f"\n\nDeck size: {len(self.deck)}"
        result += f"\nHint tokens: {self.hint_tokens}"
        result += f"\nPenalty tokens: {self.penalty_tokens}"

        result += "\n\nPlayer cards: \n"
        # TODO: Replace with num_players
        for player in range(3):
            result += f"Player {player}: "
            if player == self.current_player:
                result += "Redacted\n"
            else:
                for card in self.player_cards[player]:
                    result += f'{str(card)} '
                result += '\n'

        return result
