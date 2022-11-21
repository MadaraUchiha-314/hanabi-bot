class GameConfig:
    def __init__(self, config):
        self.number_of_decks = config["number_of_decks"]
        self.colors = config["colors"]
        self.players = config["players"]
        self.hint_tokens = config["hint_tokens"]
        self.max_penalty_tokes = config["max_penalty_tokes"]

class Game:
    def __init__(self, config, initial_deck):
        self.game_config = GameConfig(config)
        self.deck = initial_deck
        self.played_cards = [0] * len(self.game_config.number_of_decks)
        self.player_turn = 0
        self.hint_tokens = self.game_config.hint_tokens
        self.penalty_tokens = 0
        self.max_penalty_tokes = self.game_config.max_penalty_tokes
        self.discarded_cards = []
    
    def get_current_state():
        pass
    
    def get_next_states():
        pass
    
    def make_move(move):
        pass