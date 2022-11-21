from dataclasses import dataclass
from typing import List

from hanabi.game.state import State
from hanabi.game.move import Move, MoveType
from hanabi.game.card import CardNumber, CardColor, CardIndex


@dataclass
class GameConfig:
    available_decks: List[CardNumber]
    colors: List[CardColor]
    num_players: int
    cards_per_players: int
    hint_tokens: int
    max_penalty_tokes: int


class Game:
    state: State

    def __init__(self, config, initial_deck):
        self.game_config = GameConfig(
            available_decks=config["available_decks"],
            colors=config["colors"],
            num_players=config["num_players"],
            cards_per_players=config["cards_per_players"],
            hint_tokens=config["hint_tokens"],
            max_penalty_tokes=config["max_penalty_tokes"],
        )

        player_cards = []
        for _ in range(self.game_config.num_players):
            player_cards.append(initial_deck[:self.game_config.cards_per_players])
            initial_deck = initial_deck[self.game_config.cards_per_players:]

        self.state = State(
            deck=initial_deck,
            played_cards=[0] * len(self.game_config.colors),
            discarded_cards=[],
            player_cards=player_cards,
            player_turn=0,
            hint_tokens=0,
            penalty_tokens=0,
        )

    def get_hint_moves(self) -> List[Move]:
        if self.game_config.hint_tokens < 1:
            return []
        moves = []
        for target_player in range(self.game_config.num_players):
            if target_player == self.state.player_turn:
                continue
            for color in self.game_config.colors:
                moves.append(Move(
                    move_type=MoveType.HINT,
                    target_player=target_player,
                    move_detail=color
                ))
            for deck in self.game_config.available_decks:
               moves.append(Move(
                    move_type=MoveType.HINT,
                    target_player=target_player,
                    move_detail=deck
                ))
        return moves

    def get_dicard_moves(self) -> List[Move]:
        moves = []
        for i in range(len(self.state.player_cards[self.state.player_turn])):
            moves.append(Move(
                move_type=MoveType.DISCARD,
                move_detail=CardIndex(i),
                target_player=self.state.player_turn,
            ))
        return moves
    
    def get_play_moves(self) -> List[Move]:
        moves = []
        for i in range(len(self.state.player_cards[self.state.player_turn])):
            moves.append(Move(
                move_type=MoveType.PLAY,
                move_detail=CardIndex(i),
                target_player=self.state.player_turn,
            ))
        return moves

    def get_next_moves(self) -> List[Move]:
        return self.get_hint_moves() + self.get_dicard_moves() + self.get_play_moves()
    
    def apply_move(self) -> State:
        pass
    
    def get_current_state(self) -> State:
        pass
    
    def get_next_states(self) -> List[State]:
        pass
    
    def make_move(self, move):
        pass
