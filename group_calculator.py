from calculate_winrate_single import run_winrate_evolution
from utils import get_hand_group_dict

def run_group_calculation(selected_groups, flop, num_simulations):
    """
    複数のハンドグループを処理し、各ハンドの勝率変動結果をリストで返す。
    """
    hand_dict = get_hand_group_dict()
    selected_hands = []

    for group in selected_groups:
        selected_hands.extend(hand_dict.get(group, []))

    results = []

    for hand in selected_hands:
        try:
            card1, card2 = hand
            result = run_winrate_evolution(
                card1, card2, flop, selected_range=None,
                extra_excluded=None, num_simulations=num_simulations
            )
            result["Hand"] = f"{card1}{card2}"
            result["Group"] = group
            result["Flop"] = flop
            results.append(result)
        except Exception as e:
            print(f"Error while processing {hand}: {e}")

    return results
