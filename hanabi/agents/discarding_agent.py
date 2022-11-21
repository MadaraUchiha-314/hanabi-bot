from typing import List, Tuple

from hanabi.agents.agent import Agent
from hanabi.game.move import Move, MoveType
from hanabi.game.state import State


class DiscardingAgent(Agent):
    def __init__(self, player_index):
        super().__init__(player_index)

    def action(self, state: State, candidate_moves_and_states: List[Tuple[Move, State]]) -> Move:
        for move in candidate_moves_and_states:
            if move.move_type == MoveType.DISCARD:
                return move
