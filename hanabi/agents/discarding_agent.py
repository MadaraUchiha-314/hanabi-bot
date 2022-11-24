from typing import List

from hanabi.agents.agent import Agent
from hanabi.game.move import Move, MoveType
from hanabi.game.state import State


class DiscardingAgent(Agent):
    def __init__(self, player_index):
        super().__init__(player_index)

    def action(self, state: State, candidate_moves: List[Move]) -> Move:
        for move in candidate_moves:
            if move.move_type == MoveType.DISCARD:
                return move
