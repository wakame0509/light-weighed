import pandas as pd

def analyze_detailed_features(df):
    """
    勝率結果DataFrameに特徴量を追加。
    必須列: Hand, Group, FlopWinrate, TurnWinrate, RiverWinrate, Flop (list of 3 cards)
    """
    features = []

    for _, row in df.iterrows():
        hand = row["Hand"]
        group = row["Group"]
        flop_cards = row.get("Flop", [])
        flop_winrate = row["FlopWinrate"]
        turn_winrate = row["TurnWinrate"]
        river_winrate = row["RiverWinrate"]

        flop_ranks = [card[0] for card in flop_cards if len(card) == 2]
        hole_ranks = [hand[0], hand[2]] if len(hand) == 4 else [hand[0], hand[1]]

        overcard_on_flop = any(r > max(hole_ranks) for r in flop_ranks if r in "23456789TJQKA")
        paired_board = len(set(flop_ranks)) < 3
        monotone_flop = len(set([card[1] for card in flop_cards if len(card) == 2])) == 1
        connected_flop = is_connected(flop_ranks)

        shift_flop = flop_winrate
        shift_turn = turn_winrate - flop_winrate
        shift_river = river_winrate - turn_winrate

        features.append({
            "Hand": hand,
            "Group": group,
            "OvercardOnFlop": overcard_on_flop,
            "PairedBoard": paired_board,
            "MonotoneFlop": monotone_flop,
            "ConnectedFlop": connected_flop,
            "FlopWinrate": flop_winrate,
            "TurnWinrate": turn_winrate,
            "RiverWinrate": river_winrate,
            "ShiftFlop": shift_flop,
            "ShiftTurn": shift_turn,
            "ShiftRiver": shift_river
        })

    return pd.DataFrame(features)


def is_connected(ranks):
    """ランクがストレートっぽいか判定（例: 9, T, J）"""
    rank_order = "23456789TJQKA"
    rank_values = sorted([rank_order.index(r) for r in ranks if r in rank_order])
    return max(rank_values) - min(rank_values) <= 4 and len(rank_values) == 3
