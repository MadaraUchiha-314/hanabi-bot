import copy
from dataclasses import dataclass
from typing import List, Tuple, Callable

from hanabi.game.state import State
from hanabi.game.move import Move, MoveType, HintCardMove, DiscardCardMove, PlayCardMove, HintCardColor, HintCardNumber, HintMoveType
from hanabi.game.card import CardNumber, CardColor, CardIndex, Card


@dataclass
class GameConfig:
    available_decks: List[CardNumber]
    colors: List[CardColor]
    card_multiplicity: Callable[[Card], int]
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
            card_multiplicity=config["card_multiplicity"],
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
            penalty_tokens=0,
        )

    def _get_hint_moves(self) -> List[Move]:
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
                    move_detail=HintCardMove(
                        hint_move_type=HintMoveType.Color,
                        hint_move_detail=HintCardColor(
                            card_color=color
                        )
                    )
                ))
            for deck in self.game_config.available_decks:
               moves.append(Move(
                    move_type=MoveType.HINT,
                    target_player=target_player,
                    move_detail=HintCardMove(
                        hint_move_type=HintMoveType.Number,
                        hint_move_detail=HintCardNumber(
                            card_number=deck
                        )
                    )
                ))
        return moves

    def _get_dicard_moves(self) -> List[Move]:
        moves = []
        for i in range(len(self.state.player_cards[self.state.current_player])):
            moves.append(Move(
                move_type=MoveType.DISCARD,
                target_player=self.state.current_player,
                move_detail=DiscardCardMove(
                    card_index=CardIndex(i)
                ),
            ))
        return moves
    
    def _get_play_moves(self) -> List[Move]:
        moves = []
        for i in range(len(self.state.player_cards[self.state.current_player])):
            moves.append(Move(
                move_type=MoveType.PLAY,
                target_player=self.state.current_player,
                move_detail=PlayCardMove(
                    card_index=CardIndex(i)
                ),
            ))
        return moves

    def get_next_moves(self) -> List[Move]:
        return self._get_hint_moves() + self._get_dicard_moves() + self._get_play_moves()

    @staticmethod
    def move_to_next_player(game_config: GameConfig, state: State) -> State:
        state.current_player = (state.current_player + 1) % game_config.num_players
        return state

    @staticmethod
    def simulate_discard_move(game_config: GameConfig, state: State, move: Move) -> State:
        new_state = copy.deepcopy(state)
        new_state.discarded_cards.append(
            new_state.player_cards[new_state.current_player].pop(
                move.move_detail.card_index
            )
        )
        new_state.player_cards[new_state.current_player].insert(0, new_state.deck.pop())
        return new_state

    @staticmethod
    def simulate_play_move(game_config: GameConfig, state: State, move: Move) -> State:
        new_state = copy.deepcopy(state)

        card_played = new_state.player_cards[new_state.current_player].pop(move.move_detail.card_index)
        return Game.simulate_play_card(game_config, state, card_played)

    @staticmethod
    def simulate_play_card(game_config: GameConfig, state: State, card: Card) -> State:
        new_state = copy.deepcopy(state)

        if new_state.played_cards[card.color] == int(card.number.value) + 1:
            new_state.played_cards[card.color] += 1
        else:
            new_state.discarded_cards.append(card)
            new_state.penalty_tokens += 1
        new_state.player_cards[new_state.current_player].append(new_state.deck.pop())
        return new_state
    
    @staticmethod
    def simulate_hint_move(game_config: GameConfig, state: State, move: Move) -> State:
        new_state = copy.deepcopy(state)
        new_state.hint_tokens -= 1
        return new_state
    
    @staticmethod
    def simulate_move(game_config: GameConfig, state: State, move: Move) -> State:
        state = copy.deepcopy(state)
        if move.move_type == MoveType.DISCARD:
            return Game.simulate_discard_move(game_config, state, move)
        elif move.move_type == MoveType.PLAY:
            return Game.simulate_play_move(game_config, state, move)
        else:
            return Game.simulate_hint_move(game_config, state, move)
         
    def get_state_for_current_player(self) -> State:
        state = copy.deepcopy(self.state)
        state.player_cards[self.state.current_player] = [card.get(True) for card in self.state.player_cards[self.state.current_player]]
        state.deck = []
        return state
    
    def get_next_moves_and_states(self) -> List[Tuple[Move, State]]:
        pass

    def _update_hints(self, move: Move, target_player: int):
        if isinstance(move.move_detail.hint_move_detail, HintCardNumber):
            hinted_number = move.move_detail.hint_move_detail.card_number
            for card in self.state.player_cards[target_player]:
                if card.number == hinted_number:  # If match, cross out every other number
                    for number in CardNumber:
                        card.hints[number] = False
                    card.hints[card.number] = True
                else:  # else cross out the number hinted
                    card.hints[hinted_number] = False
        if isinstance(move.move_detail.hint_move_detail, HintCardColor):
            hinted_color = move.move_detail.hint_move_detail.card_color
            for card in self.state.player_cards[target_player]:
                if card.color == hinted_color:  # If match, cross out every other color
                    for color in CardColor:
                        card.hints[color] = False
                    card.hints[card.color] = True
                else:  # else cross out the color hinted
                    card.hints[hinted_color] = False

    def make_move(self, move: Move):
        if move.move_type == MoveType.DISCARD:
            self.state = Game.simulate_discard_move(self.game_config, self.state, move)
        elif move.move_type == MoveType.PLAY:
            self.state = Game.simulate_play_move(self.game_config, self.state, move)
        else:
            self.state.hint_tokens -= 1
            self._update_hints(move, target_player=move.target_player)

        self.state.current_player = (self.state.current_player + 1) % self.game_config.num_players
