from typing import List

from hanabi.game.move import Move
from hanabi.game.state import State
from hanabi.game.game import GameConfig


class Agent:
    def __init__(self, game_config: GameConfig,player_index):
        self.player_index = player_index
        self.game_config = game_config

    def action(self, state: State, candidate_moves: List[Move]) -> Move:
        pass
