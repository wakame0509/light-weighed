from utils import get_group_hands, get_hand_range_25, get_hand_range_30
from calculate_winrate import run_winrate_evolution
import pandas as pd
import random

def run_group_calculation(group_name, num_simulations, range_mode, six_player_mode, return_feature_analysis=False):
    hands = get_group_hands(group_name)
    results = []
    features = []

    # レンジ処理
    if range_mode == "25":
        selected_range = get_hand_range_25()
    elif range_mode == "30":
        selected_range = get_hand_range_30()
    else:
        selected_range = None

    for hand in hands:
        try:
            if len(hand) == 2:
                rank1, rank2 = hand
                suit1, suit2 = "s", "h"
            elif len(hand) == 3:
                rank1, rank2, suited_flag = hand
                suit1 = "s"
                suit2 = "s" if suited_flag == "s" else "h"
            else:
                continue

            card1 = rank1 + suit1
            card2 = rank2 + suit2

            # 6人テーブルの他プレイヤー除外
            extra_excluded = None
            if six_player_mode:
                full_deck = [r + s for r in "23456789TJQKA" for s in "cdhs"]
                known_cards = [card1, card2]
                deck = [c for c in full_deck if c not in known_cards]
                random.shuffle(deck)
                others = [deck.pop() for _ in range(4 * 2)]
                extra_excluded = others

            result, feature_flags = run_winrate_evolution(
                p1_card1=card1,
                p1_card2=card2,
                board=[],
                selected_range=selected_range,
                extra_excluded=extra_excluded,
                num_simulations=num_simulations,
                return_features=True
            )

            result["Hand"] = card1 + card2
            result["Group"] = group_name
            results.append(result)

            features.extend(feature_flags)

        except Exception as e:
            print(f"{hand} でエラー: {e}")
            continue

    df_results = pd.DataFrame(results)

    if return_feature_analysis:
        df_features = pd.DataFrame(features)
        grouped = df_features.groupby("Feature").agg(
            Count=("Shift", "count"),
            AvgShift=("Shift", "mean")
        ).reset_index()
        return df_results, grouped

    return df_results
