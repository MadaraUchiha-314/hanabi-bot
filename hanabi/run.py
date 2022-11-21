import random
from typing import List

from hanabi.game.card import CardColor, CardNumber, Card
from hanabi.game.game import Game

random.seed(42)


def run_game():
    game_config = {
        "available_decks": [num for num in CardNumber],
        "colors": [color for color in CardColor],
        "num_players": 3,
        "cards_per_players": 5,
        "hint_tokens": 8,
        "max_penalty_tokes": 3,
    }

    initial_deck: List[Card] = []
    for color in CardColor:
        for number in CardNumber:
            for multiplicity in range(CardNumber.multiplicity(number)):
                initial_deck.append(Card(color=color, number=number))
    random.shuffle(initial_deck)

    game = Game(game_config, initial_deck)

    game.state.discarded_cards = [
        Card(CardColor.WHITE, CardNumber.ONE),
        Card(CardColor.WHITE, CardNumber.THREE),
        Card(CardColor.YELLOW, CardNumber.THREE),
    ]

    print(game.state)
    print('\n'.join(str(x) for x in game.get_next_moves()))


if __name__ == '__main__':
    run_game()
