import copy

from typing import List, Tuple, Dict
from hanabi.game.move import Move, PlayCardMove, MoveType, HintCardMove, HintCardNumber, HintCardColor, HintMoveType, DiscardCardMove
from hanabi.game.state import State
from hanabi.agents.agent import Agent
from hanabi.game.game import Game


from hanabi.game.card_helpers import resolve_hints_to_all_possible_cards, is_direct_hint, is_hint_adding_information, \
    is_card_only_unplayed_copy, is_card_playable_without_penalty, resolve_hints_to_card


class GreedyAgent(Agent):
    def __init__(self, game_config, player_index):
        super().__init__(game_config, player_index)

    def evaluate_next_state_score(self, state: State, next_state: State, move):
        if next_state.penalty_tokens > state.penalty_tokens:
            return -100

        if next_state.hint_tokens == 0:
            return -10

        if move.move_type == MoveType.HINT:
            for player in range(len(state.player_cards)):
                if player == state.current_player:
                    continue

                for idx, target_card in enumerate(state.player_cards[player]):
                    if is_direct_hint(hint_card_move=move.move_detail, card=target_card) \
                            and is_hint_adding_information(state=state, move=move, target_card_idx=idx):
                        if is_card_only_unplayed_copy(game_config=self.game_config, state=state, card=target_card):
                            return +20
                        if is_card_playable_without_penalty(self.game_config, state, target_card):
                            return +15
        elif move.move_type == MoveType.DISCARD:
            target_card = state.player_cards[state.current_player][move.move_detail.card_index]
            target_card_resolved = resolve_hints_to_card(self.game_config, target_card)
            if target_card_resolved is not None:
                if not is_card_only_unplayed_copy(self.game_config, state, target_card_resolved, resolve_hints=True):
                    return +5
                else:
                    return -20
        elif move.move_type == MoveType.PLAY:
            target_card = state.player_cards[state.current_player][move.move_detail.card_index]
            target_card_resolved = resolve_hints_to_card(self.game_config, target_card)
            if target_card_resolved is not None and next_state.played_cards != state.played_cards:
                return +100
            elif next_state.played_cards != state.played_cards:
                return +10

        return 0

    def action(self, state: State, candidate_moves: List[Move]) -> Move:
        score: Dict[Move: int] = {}
        for move in candidate_moves:
            score[move] = 0
            if move.move_type == MoveType.PLAY or move.move_type == MoveType.DISCARD:
                possible_cards = state.player_cards[state.current_player][move.move_detail.card_index].get_possible_cards_from_hints()
                for possible_card in possible_cards:
                    current_state = copy.deepcopy(state)
                    current_state.player_cards[state.current_player][move.move_detail.card_index] = possible_card
                    next_state = Game.simulate_move(self.game_config, current_state, move)
                    score_for_move = self.evaluate_next_state_score(current_state, next_state, move)
                    score[move] += float(score_for_move) / float(len([possible_cards]))
            else:
                next_state = Game.simulate_move(self.game_config, state, move)
                score_for_move = self.evaluate_next_state_score(state, next_state, move)
                score[move] += float(score_for_move)
        return sorted(
            [(b, a) for a, b  in score.items()]
        , reverse=True)[0][1]

                