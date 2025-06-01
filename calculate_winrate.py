import eval7
import random

def evaluate_hand(cards):
    return eval7.evaluate(cards)

def generate_deck():
    ranks = '23456789TJQKA'
    suits = 'cdhs'
    return [r + s for r in ranks for s in suits]

def remove_known_cards(deck, known_cards):
    return [card for card in deck if card not in known_cards]

def detect_features(p1_cards, board_cards):
    """フロップやターンに落ちたカードの特徴を返す（例: オーバーカード, フラッシュドローなど）"""
    features = []

    p1_ranks = [c[0] for c in p1_cards]
    board_ranks = [c[0] for c in board_cards]

    max_p1_rank = max(p1_ranks, key=lambda r: "23456789TJQKA".index(r))
    if any("23456789TJQKA".index(br) > "23456789TJQKA".index(max_p1_rank) for br in board_ranks):
        features.append("Overcard")

    suits = [c[1] for c in board_cards]
    suit_counts = {s: suits.count(s) for s in set(suits)}
    if max(suit_counts.values()) == 3:
        features.append("FlushDraw")

    return features or ["None"]

def run_winrate_evolution(p1_card1, p1_card2, board, selected_range=None,
                          extra_excluded=None, num_simulations=10000,
                          return_features=False):
    known = [p1_card1, p1_card2] + board
    full_deck = generate_deck()
    deck = remove_known_cards(full_deck, known)

    if extra_excluded:
        deck = remove_known_cards(deck, extra_excluded)

    flop_wins = turn_wins = river_wins = 0
    flop_ties = turn_ties = river_ties = 0

    feature_records = []

    for _ in range(num_simulations):
        sim_deck = deck.copy()
        random.shuffle(sim_deck)

        # 相手ハンド
        opp_hand = random.choice(selected_range) if selected_range else [sim_deck.pop(), sim_deck.pop()]

        try:
            flop = board + [sim_deck.pop() for _ in range(3 - len(board))]
            turn = flop + [sim_deck.pop()]
            river = turn + [sim_deck.pop()]

            # フロップ評価
            p1f = [eval7.Card(p1_card1), eval7.Card(p1_card2)] + [eval7.Card(c) for c in flop]
            p2f = [eval7.Card(c) for c in opp_hand] + [eval7.Card(c) for c in flop]
            s1f, s2f = evaluate_hand(p1f), evaluate_hand(p2f)

            # ターン評価
            p1t = [eval7.Card(p1_card1), eval7.Card(p1_card2)] + [eval7.Card(c) for c in turn]
            p2t = [eval7.Card(c) for c in opp_hand] + [eval7.Card(c) for c in turn]
            s1t, s2t = evaluate_hand(p1t), evaluate_hand(p2t)

            # リバー評価
            p1r = [eval7.Card(p1_card1), eval7.Card(p1_card2)] + [eval7.Card(c) for c in river]
            p2r = [eval7.Card(c) for c in opp_hand] + [eval7.Card(c) for c in river]
            s1r, s2r = evaluate_hand(p1r), evaluate_hand(p2r)

            if s1f > s2f:
                flop_wins += 1
                flop_shift = 1
            elif s1f == s2f:
                flop_ties += 1
                flop_shift = 0.5
            else:
                flop_shift = 0

            if s1t > s2t:
                turn_wins += 1
                turn_shift = 1
            elif s1t == s2t:
                turn_ties += 1
                turn_shift = 0.5
            else:
                turn_shift = 0

            if s1r > s2r:
                river_wins += 1
                river_shift = 1
            elif s1r == s2r:
                river_ties += 1
                river_shift = 0.5
            else:
                river_shift = 0

            if return_features:
                flop_feats = detect_features([p1_card1, p1_card2], flop)
                for feat in flop_feats:
                    feature_records.append({
                        "Feature": feat,
                        "Street": "Flop",
                        "Shift": flop_shift * 100
                    })

                turn_feats = detect_features([p1_card1, p1_card2], turn)
                for feat in turn_feats:
                    feature_records.append({
                        "Feature": feat,
                        "Street": "Turn",
                        "Shift": turn_shift * 100
                    })

                river_feats = detect_features([p1_card1, p1_card2], river)
                for feat in river_feats:
                    feature_records.append({
                        "Feature": feat,
                        "Street": "River",
                        "Shift": river_shift * 100
                    })

        except Exception:
            continue

    flop_winrate = (flop_wins + flop_ties / 2) / num_simulations * 100
    turn_winrate = (turn_wins + turn_ties / 2) / num_simulations * 100
    river_winrate = (river_wins + river_ties / 2) / num_simulations * 100

    result = {
        "Preflop": 0.0,
        "FlopWinrate": flop_winrate,
        "TurnWinrate": turn_winrate,
        "RiverWinrate": river_winrate,
        "ShiftFlop": flop_winrate,
        "ShiftTurn": turn_winrate - flop_winrate,
        "ShiftRiver": river_winrate - turn_winrate
    }

    if return_features:
        return result, feature_records
    return result
