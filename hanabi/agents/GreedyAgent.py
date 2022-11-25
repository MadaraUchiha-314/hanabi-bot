from typing import List
from hanabi.game.move import Move, PlayCardMove, MoveType, HintCardMove, HintCardNumber, HintCardColor, HintMoveType, DiscardCardMove
from hanabi.game.state import State
from hanabi.agents.agent import Agent
from hanabi.game.game import Game


from hanabi.game.card_helpers import resolve_hints_to_all_possible_cards

class GreedyAgent(Agent):
    def __init__(self, game_config, player_index):
        super().__init__(game_config, player_index)


    def evalutate_next_state_score(self, state: State, next_state: State, move: Move):
        score = 0
        total_played_cards_before = sum([state.played_cards[color] for color in self.game_config.colors])
        total_played_cards_after = sum([next_state.played_cards[color] for color in self.game_config.colors])

        if total_played_cards_after > total_played_cards_before:
            score += 10
        
        if next_state.penalty_tokens > state.penalty_tokens:
            score -= 100

        if move.move_type == MoveType.HINT:
            score += 2

        if next_state.penalty_tokens >= self.game_config.max_penalty_tokes:
            score -= 10 ** 5
        
        return score

            
    def action(self, state: State, candidate_moves: List[Move]) -> Move:
        current_player = state.current_player
        current_player_cards = state.player_cards[current_player]
        possible_cards_for_current_player = []
        for idx, card in enumerate(current_player_cards):
            possible_cards_for_current_player += [ (idx,possible_card) for possible_card in resolve_hints_to_all_possible_cards(self.game_config, card)]

        possible_next_states: List[State] = []
        for idx, card in possible_cards_for_current_player:
            state.player_cards[current_player][idx] = card
            move = Move(
                move_detail=PlayCardMove(
                    card_index=idx,
                ),
                move_type=MoveType.PLAY,
                target_player=current_player
            )
            possible_next_states.append((move, Game.simulate_move(self.game_config, state, move)))
        for player in range(self.game_config.num_players):
            if player == state.current_player:
                continue
            for color in self.game_config.colors:
                move = Move(
                    move_detail=HintCardMove(
                        hint_move_type=HintMoveType.Color,
                        hint_move_detail=HintCardColor(
                            card_color=color,
                        )
                    ),
                    move_type=MoveType.HINT,
                    target_player=player
                )
                possible_next_states.append((move, Game.simulate_move(self.game_config, state, move)))
            for number in self.game_config.available_decks:
                move = Move(
                    move_detail=HintCardMove(
                        hint_move_type=HintMoveType.Number,
                        hint_move_detail=HintCardNumber(
                            card_number=number,
                        )
                    ),
                    move_type=MoveType.HINT,
                    target_player=player
                )
                possible_next_states.append((move, Game.simulate_move(self.game_config, state, move)))
            
            for idx, _ in enumerate(current_player_cards):
                move = Move(
                            move_detail=DiscardCardMove(
                                card_index=idx,
                            ),
                            move_type=MoveType.DISCARD,
                            target_player=current_player
                        )
                possible_next_states.append((move,
                    Game.simulate_move(
                        self.game_config, state, move 
                    )
                ))
        return sorted(zip([
             self.evalutate_next_state_score(
                state, next_state, move
            ) for move, next_state in possible_next_states
        ], [move for move, _ in possible_next_states]))[-1][1]
                



