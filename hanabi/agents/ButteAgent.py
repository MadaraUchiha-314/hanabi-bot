from typing import List
from hanabi.game.move import Move
from hanabi.game.state import State
from hanabi.agents.agent import Agent


class ButteAgent(Agent):
    def __init__(self, game_config, player_index):
        super().__init__(game_config, player_index)
    
    def action(self, state: State, candidate_moves: List[Move]) -> Move:
        # Priorities
        # 1. If someone else needs a hint about their cards which is ciritical, give them them the hint.
        #    1.1. What happens to the case where multiple players come together to give a hint to palater
        # 2. Go through all the cards to see if we have a playable card
        #    2.1 
        pass

