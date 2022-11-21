from hanabi.game.state import State


class GameConfig:
    def __init__(self, config):
        self.number_of_decks = config["number_of_decks"]
        self.colors = config["colors"]
        self.num_players = config["num_players"]
        self.cards_per_players = config["cards_per_players"]
        self.hint_tokens = config["hint_tokens"]
        self.max_penalty_tokes = config["max_penalty_tokes"]


class Game:
    state: State

    def __init__(self, config, initial_deck):
        self.game_config = GameConfig(config)

        player_cards = []
        for _ in range(self.game_config.num_players):
            player_cards.append(initial_deck[:self.game_config.cards_per_players])
            initial_deck = initial_deck[self.game_config.cards_per_players:]

        self.state = State(
            deck=initial_deck,
            played_cards=[0] * len(self.game_config.number_of_decks),
            discarded_cards=[],
            player_cards=player_cards,
            player_turn=0,
            hint_tokens=0,
            penalty_tokens=0,
        )
    
    def get_current_state(self):
        pass
    
    def get_next_states(self):
        pass
    
    def make_move(self, move):
        pass
