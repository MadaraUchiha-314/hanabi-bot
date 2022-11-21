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
            played_cards={color: 0 for color in self.game_config.colors},
            discarded_cards=[],
            player_cards=player_cards,
            current_player=0,
            hint_tokens=self.game_config.hint_tokens,
            penalty_tokens=self.game_config.max_penalty_tokes,
        )

    def get_hint_moves(self) -> List[Move]:
        if self.game_config.hint_tokens < 1:
            return []
        moves = []
        for target_player in range(self.game_config.num_players):
            if target_player == self.state.current_player:
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
        for i in range(len(self.state.player_cards[self.state.current_player])):
            moves.append(Move(
                move_type=MoveType.DISCARD,
                move_detail=CardIndex(i),
                target_player=self.state.current_player,
            ))
        return moves
    
    def get_play_moves(self) -> List[Move]:
        moves = []
        for i in range(len(self.state.player_cards[self.state.current_player])):
            moves.append(Move(
                move_type=MoveType.PLAY,
                move_detail=CardIndex(i),
                target_player=self.state.current_player,
            ))
        return moves

    def get_next_moves(self) -> List[Move]:
        return self.get_hint_moves() + self.get_dicard_moves() + self.get_play_moves()
    
    def apply_move(self, move: Move) -> State:
        pass
    
    def get_current_state(self) -> State:
        pass
    
    def get_next_states(self) -> List[State]:
        pass
    
    def make_move(self, move: Move):
        if move.move_type == MoveType.DISCARD:
            self.state.discarded_cards.append(
                self.state.player_cards[self.state.current_player].pop(
                    move.move_detail
                )
            )
            self.state.player_cards[self.state.current_player].insert(0, self.state.deck.pop())
        elif move.move_type == MoveType.PLAY:
            card_played = self.state.player_cards[self.state.current_player].pop(move.move_detail)
            if self.state.played_cards[card_played.color.value] == int(card_played.number.value) + 1:
                self.state.played_cards[card_played.color.value] += 1
            else:
                self.state.discarded_cards.append(card_played)
                self.state.penalty_tokens += 1
            self.state.player_cards[self.state.current_player].append(self.state.deck.pop())
        else:
            self.state.hint_tokens -= 1
        self.state.current_player = (self.state.current_player + 1) % self.game_config.num_players
