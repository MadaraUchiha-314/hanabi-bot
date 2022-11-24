import random
from typing import List

from hanabi.agents.agent import Agent
from hanabi.agents.discarding_agent import DiscardingAgent
from hanabi.agents.human import Human
from hanabi.game.card import CardColor, CardNumber, Card
from hanabi.game.game import Game
from hanabi.game.move import PlayedMove

random.seed(42)


def get_card_multiplicity(card: Card) -> int:
    number = card.number
    if number == CardNumber.ONE:
        return 3
    elif number == CardNumber.FIVE:
        return 1
    else:
        return 2


def run_game():
    game_config = {
        "available_decks": [num for num in CardNumber],
        "colors": [color for color in CardColor],
        "card_multiplicity": get_card_multiplicity,
        "num_players": 3,
        "cards_per_players": 5,
        "hint_tokens": 8,
        "max_penalty_tokes": 3,
    }

    card_multiplicity_method = game_config["card_multiplicity"]
    initial_deck: List[Card] = []
    for color in CardColor:
        for number in CardNumber:
            card = Card(color=color, number=number)
            for multiplicity in range(card_multiplicity_method(card)):
                initial_deck.append(card)
    random.shuffle(initial_deck)

    game = Game(game_config, initial_deck)
    players = [Human(0), DiscardingAgent(1), DiscardingAgent(2)]

    played_moves_log = []
    for i in range(10):
        print(game.state)

        current_player = game.state.current_player
        current_agent: Agent = players[current_player]

        played_action = current_agent.action(
            state=game.get_state_for_current_player(),
            candidate_moves=game.get_next_moves(),
        )

        played_moves_log.append(PlayedMove(player_num=current_player, move=played_action))
        game.make_move(played_action)

        print("-" * 50)
        print("\nGame log")
        for played_move in played_moves_log:
            print(f"Player {played_move.player_num}: {played_move.move}")


if __name__ == '__main__':
    run_game()
