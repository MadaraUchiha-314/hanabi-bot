from typing import List, Optional

from hanabi.agents.agent import Agent
from hanabi.game.card_helpers import is_direct_hint, is_card_playable_without_penalty, is_card_only_unplayed_copy, \
    is_hint_adding_information
from hanabi.game.move import Move, HintCardMove, PlayCardMove, DiscardCardMove
from hanabi.game.state import State


class InfiniteHintsAgent(Agent):
    def __init__(self, game_config, player_index):
        super().__init__(game_config, player_index)

    def hint_move(self, state: State, candidate_moves: List[Move]) -> Optional[Move]:
        # Extract hints to playable cards
        playable_hints = []
        for move in candidate_moves:
            if not isinstance(move.move_detail, HintCardMove):
                continue

            target_player_cards = state.player_cards[move.target_player]
            for idx, card in enumerate(target_player_cards):
                if is_card_playable_without_penalty(self.game_config, state, card) \
                        and is_direct_hint(hint_card_move=move.move_detail, card=card) \
                        and is_hint_adding_information(state=state, move=move, target_card_idx=idx):
                    playable_hints.append(move)

        if len(playable_hints) == 0:
            return None
        return playable_hints[0]

    def play_move(self, state: State, candidate_moves: List[Move]) -> Optional[Move]:
        playable_card_moves = []
        for move in candidate_moves:
            if not isinstance(move.move_detail, PlayCardMove):
                continue

            card = state.player_cards[self.player_index][move.move_detail.card_index]
            if is_card_playable_without_penalty(game_config=self.game_config, state=state, card=card, resolve_hints=True):
                playable_card_moves.append(move)

        if len(playable_card_moves) == 0:
            return None
        return playable_card_moves[0]

    def discard_move(self, state: State, candidate_moves: List[Move]) -> Move:
        discardable_moves = []
        for move in candidate_moves:
            if not isinstance(move.move_detail, DiscardCardMove):
                continue

            card = state.player_cards[self.player_index][move.move_detail.card_index]
            if is_card_only_unplayed_copy(game_config=self.game_config, state=state, card=card, resolve_hints=True):
                discardable_moves.append(move)

        if len(discardable_moves) == 0:
            all_discardable_moves = [move for move in candidate_moves if isinstance(move.move_detail, DiscardCardMove)]
            largest_index_move = max(all_discardable_moves, key=lambda move: move.move_detail.card_index)
            return largest_index_move
        return discardable_moves[0]

    def action(self, state: State, candidate_moves: List[Move]) -> Move:
        play_move = self.play_move(state, candidate_moves)
        if play_move is not None:
            return play_move

        hint_move = self.hint_move(state, candidate_moves)
        if hint_move is not None:
            return hint_move

        return self.discard_move(state, candidate_moves)
