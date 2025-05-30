from calculate_winrate import run_winrate_evolution

def run_single_hand_evaluation(hand, board, selected_range, six_player_mode, num_simulations):
    card1, card2 = hand
    return run_winrate_evolution(
        p1_card1=card1,
        p1_card2=card2,
        board=board,
        selected_range=selected_range,
        extra_excluded=None,
        num_simulations=num_simulations,
        six_player_mode=six_player_mode
    )
