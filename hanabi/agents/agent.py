from typing import List

from hanabi.game.move import Move
from hanabi.game.state import State


class Agent:
    def __init__(self, player_index):
        self.player_index = player_index

    def action(self, state: State, candidate_moves: List[Move]) -> Move:
        pass
