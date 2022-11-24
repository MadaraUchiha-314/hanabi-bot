

class Human(Agent):
    def __init__(self, player_index):
        super().__init__(player_index)
    
    def action(self, state: State, candidate_moves: List[Move]) -> Move:
        pass
