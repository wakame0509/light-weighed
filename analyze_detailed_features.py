import pandas as pd

def is_connected(ranks):
    rank_order = "23456789TJQKA"
    rank_values = sorted([rank_order.index(r) for r in ranks if r in rank_order])
    return max(rank_values) - min(rank_values) <= 4 and len(rank_values) == 3

def analyze_detailed_features_expanded(df):
    features = []

    for _, row in df.iterrows():
        hand = row["Hand"]
        group = row["Group"]
        flop_cards = row.get("Flop", [])
        flop_winrate = row["FlopWinrate"]
        turn_winrate = row["TurnWinrate"]
        river_winrate = row["RiverWinrate"]

        if len(flop_cards) != 3:
            continue

        flop_ranks = [card[0] for card in flop_cards]
        flop_suits = [card[1] for card in flop_cards]
        hole_ranks = [hand[0], hand[2]] if len(hand) == 4 else [hand[0], hand[1]]

        rank_order = "23456789TJQKA"
        hole_values = [rank_order.index(r) for r in hole_ranks if r in rank_order]
        flop_values = [rank_order.index(r) for r in flop_ranks if r in rank_order]

        overcard_on_flop = any(fv > max(hole_values) for fv in flop_values)
        undercard_on_flop = all(fv < min(hole_values) for fv in flop_values)
        paired_board = len(set(flop_ranks)) < 3
        monotone_flop = len(set(flop_suits)) == 1
        rainbow_flop = len(set(flop_suits)) == 3
        two_tone_flop = len(set(flop_suits)) == 2
        connected_flop = is_connected(flop_ranks)
        flush_draw_possible = any(flop_suits.count(suit) >= 2 for suit in flop_suits)

        shift_flop = flop_winrate
        shift_turn = turn_winrate - flop_winrate
        shift_river = river_winrate - turn_winrate

        features.append({
            "Hand": hand,
            "Group": group,
            "OvercardOnFlop": overcard_on_flop,
            "UndercardOnFlop": undercard_on_flop,
            "PairedBoard": paired_board,
            "MonotoneFlop": monotone_flop,
            "RainbowFlop": rainbow_flop,
            "TwoToneFlop": two_tone_flop,
            "ConnectedFlop": connected_flop,
            "FlushDrawPossible": flush_draw_possible,
            "FlopWinrate": flop_winrate,
            "TurnWinrate": turn_winrate,
            "RiverWinrate": river_winrate,
            "ShiftFlop": shift_flop,
            "ShiftTurn": shift_turn,
            "ShiftRiver": shift_river
        })

    return pd.DataFrame(features)
