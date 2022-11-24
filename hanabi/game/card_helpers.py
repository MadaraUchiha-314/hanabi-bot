from typing import Optional

from hanabi.game.card import Card, CardNumber
from hanabi.game.game import Game, GameConfig
from hanabi.game.state import State


def resolve_hints_to_card(game_config: GameConfig, card: Card) -> Optional[Card]:
    possible_colors = [color for color in game_config.colors if card.hints[color] is True]
    possible_numbers = [number for number in game_config.available_decks if card.hints[number] is True]

    if len(possible_colors) != 1 and len(possible_numbers) != 1:
        return None
    return Card(color=possible_colors[0], number=possible_numbers[0])


def is_card_playable_without_penalty(game_config: GameConfig, state: State, card: Card, resolve_hints=False):
    if resolve_hints:
        resolved_card = resolve_hints_to_card(game_config, card)
        if resolved_card is not None:
            card = resolved_card

    new_state = Game.simulate_play_card(game_config=None, state=state, card=card)
    if new_state.penalty_tokens > state.penalty_tokens:
        return False
    else:
        return True


def is_card_only_unplayed_copy(game_config: GameConfig, state: State, card: Card, resolve_hints=False):
    if resolve_hints:
        resolved_card = resolve_hints_to_card(game_config, card)
        if resolved_card is not None:
            card = resolved_card

    # Find all played + discarded cards
    all_used_cards = state.discarded_cards
    for color, played_value in state.played_cards:
        for card_value in range(1, played_value):
            card = Card(color=color, number=CardNumber(str(card_value)))
            all_used_cards.append(card)

    used_copies = len([used_card for used_card in all_used_cards if used_card == card])

    card_multiplicity_method = game_config.card_multiplicity
    card_available_copies = card_multiplicity_method(card)
    if card_available_copies - used_copies == 1:
        return True
    else:
        return False
