from typing import List, Tuple

from hanabi.game.move import Move
from hanabi.game.state import State


class Agent:
    def __init__(self, player_index):
        self.player_index = player_index

    def action(self, state: State, candidate_moves_and_states: List[Tuple[Move, State]]) -> Move:
        pass
