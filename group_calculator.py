from utils import get_group_hands
from calculate_winrate import run_winrate_evolution
import pandas as pd

def run_group_calculation(group_name, num_simulations, range_mode, six_player_mode):
    hands = get_group_hands(group_name)
    results = []

    for hand in hands:
        try:
            # 例: hand = "AKs" や "QJo" のような文字列を想定
            if len(hand) == 3:
                rank1, rank2, suited_flag = hand[0], hand[1], hand[2]
                suit1 = "s"
                suit2 = "s" if suited_flag == "s" else "h"
            elif len(hand) == 2:
                rank1, rank2 = hand[0], hand[1]
                suit1, suit2 = "s", "h"
            else:
                raise ValueError(f"形式不明のハンド: {hand}")

            card1 = rank1 + suit1
            card2 = rank2 + suit2

            result = run_winrate_evolution(
                p1_card1=card1,
                p1_card2=card2,
                board=[],
                selected_range=range_mode,
                extra_excluded=None if not six_player_mode else "simulate_others",
                num_simulations=num_simulations
            )
            result["Hand"] = card1 + card2
            result["Group"] = group_name
            results.append(result)

        except Exception as e:
            print(f"{hand} でエラー: {e}")
            continue

    return pd.DataFrame(results)
