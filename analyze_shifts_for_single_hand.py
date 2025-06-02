import pandas as pd
from calculate_winrate_detailed_v2 import run_winrate_evolution
from flop_samples import get_representative_flops
from utils import get_hand_range_25, get_hand_range_30
from tqdm import tqdm

def analyze_shifts_for_hand(card1, card2, range_mode="25", num_simulations=10000, six_player_mode=False):
    if range_mode == "25":
        selected_range = get_hand_range_25()
    elif range_mode == "30":
        selected_range = get_hand_range_30()
    else:
        selected_range = None

    flop_boards = get_representative_flops()
    all_results = []

    for flop in tqdm(flop_boards, desc=f"{card1}{card2}"):
        try:
            result, feature_flags = run_winrate_evolution(
                p1_card1=card1,
                p1_card2=card2,
                board=flop,
                selected_range=selected_range,
                extra_excluded=None,
                num_simulations=num_simulations,
                six_player_mode=six_player_mode,
                return_features=True
            )

            shift = result["ShiftFlop"]
            for feature in feature_flags:
                all_results.append({
                    "Card1": card1,
                    "Card2": card2,
                    "Flop": flop,
                    "Feature": feature["Feature"],
                    "Shift": feature["Shift"],
                    "ShiftFlop": shift
                })
        except Exception as e:
            print(f"Error with flop {flop}: {e}")
            continue

    return pd.DataFrame(all_results)
