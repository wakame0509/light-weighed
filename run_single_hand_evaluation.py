from calculate_winrate_detailed_v2 import run_winrate_evolution
from utils import generate_deck, remove_known_cards
import random

def run_single_hand_evaluation(hand, board, selected_range, six_player_mode, num_simulations):
    card1, card2 = hand

    # 6人テーブル用: 他の4人のカードを除外
    extra_excluded = None
    if six_player_mode:
        known_cards = [card1, card2] + board
        full_deck = generate_deck()
        deck = remove_known_cards(full_deck, known_cards)
        random.shuffle(deck)
        extra_excluded = [deck.pop() for _ in range(8)]  # 4人分（2枚ずつ）

    result, feature_flags = run_winrate_evolution(
        p1_card1=card1,
        p1_card2=card2,
        board=board,
        selected_range=selected_range,
        extra_excluded=extra_excluded,
        num_simulations=num_simulations,
        return_features=True
    )

    return result, feature_flags
