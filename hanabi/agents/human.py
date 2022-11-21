from typing import List, Optional

from hanabi.agents.agent import Agent
from hanabi.game.move import Move, MoveType
from hanabi.game.state import State


class Human(Agent):
    def __init__(self, player_index):
        super().__init__(player_index)

    def get_move_from_user(self, candidate_moves) -> Optional[Move]:
        available_move_types = set(move.move_type.value for move in candidate_moves)
        print(f"Available moves: {', '.join(sorted(available_move_types))}")
        chosen_move_type = input("Your move: ")

        filtered_moves = [move for move in candidate_moves if move.move_type.value == chosen_move_type]

        if chosen_move_type == MoveType.DISCARD.value:
            chosen_index = int(input("Card index: "))
            for move in filtered_moves:
                if chosen_index == move.move_detail:
                    return move
        elif chosen_move_type == MoveType.PLAY.value:
            chosen_index = int(input("Card index: "))
            for move in filtered_moves:
                if chosen_index == move.move_detail:
                    return move
        elif chosen_move_type == MoveType.HINT.value:
            chosen_player = int(input("Player: "))
            hints_available = set(move.move_detail.value for move in candidate_moves if move.move_type == MoveType.HINT)
            print(f"Available hints: {', '.join(sorted(hints_available))}")
            chosen_hint = input("Hint: ")
            for move in filtered_moves:
                if chosen_player == move.target_player and chosen_hint == move.move_detail.value:
                    return move

        return None

    def action(self, state: State, candidate_moves: List[Move]) -> Move:
        result = self.get_move_from_user(candidate_moves)
        while result is None:
            print(f"Invalid input, please retry:")
            result = self.get_move_from_user(candidate_moves)
        return result

