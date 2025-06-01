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

def detect_features(board, hand):
    """ボードとハンドに基づく特徴量を抽出する"""
    features = []
    ranks_in_board = [card[0] for card in board]
    ranks_in_hand = [card[0] for card in hand]

    # オーバーカードチェック（ハンドより高いカードがボードにあるか）
    max_rank = max(ranks_in_hand, key="23456789TJQKA".index)
    if any("23456789TJQKA".index(r) > "23456789TJQKA".index(max_rank) for r in ranks_in_board):
        features.append("Overcard on Board")

    # フラッシュの可能性チェック
    suits = [c[1] for c in board + hand]
    for s in "cdhs":
        if suits.count(s) >= 4:
            features.append("Flush Possible")
            break

    # ストレートの可能性チェック（ランクの連続性）
    rank_order = "23456789TJQKA"
    rank_set = set(ranks_in_board + ranks_in_hand)
    for i in range(len(rank_order) - 4):
        seq = set(rank_order[i:i+5])
        if seq.issubset(rank_set):
            features.append("Straight Possible")
            break

    return features

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
    features_collected = []

    for _ in range(num_simulations):
        sim_deck = deck.copy()
        random.shuffle(sim_deck)

        opp_hand = random.choice(selected_range) if selected_range else [sim_deck.pop(), sim_deck.pop()]
        try:
            # フロップ
            flop = board + [sim_deck.pop() for _ in range(3 - len(board))]
            p1_flop = [eval7.Card(p1_card1), eval7.Card(p1_card2)] + [eval7.Card(c) for c in flop]
            p2_flop = [eval7.Card(c) for c in opp_hand] + [eval7.Card(c) for c in flop]
            s1f, s2f = evaluate_hand(p1_flop), evaluate_hand(p2_flop)
            if s1f > s2f:
                flop_wins += 1
            elif s1f == s2f:
                flop_ties += 1

            # ターン
            turn = flop + [sim_deck.pop()]
            p1_turn = [eval7.Card(p1_card1), eval7.Card(p1_card2)] + [eval7.Card(c) for c in turn]
            p2_turn = [eval7.Card(c) for c in opp_hand] + [eval7.Card(c) for c in turn]
            s1t, s2t = evaluate_hand(p1_turn), evaluate_hand(p2_turn)
            if s1t > s2t:
                turn_wins += 1
            elif s1t == s2t:
                turn_ties += 1

            # リバー
            river = turn + [sim_deck.pop()]
            p1_river = [eval7.Card(p1_card1), eval7.Card(p1_card2)] + [eval7.Card(c) for c in river]
            p2_river = [eval7.Card(c) for c in opp_hand] + [eval7.Card(c) for c in river]
            s1r, s2r = evaluate_hand(p1_river), evaluate_hand(p2_river)
            if s1r > s2r:
                river_wins += 1
            elif s1r == s2r:
                river_ties += 1

            # 特徴量抽出（希望時）
            if return_features:
                features = detect_features(river, [p1_card1, p1_card2])
                for feat in features:
                    features_collected.append({
                        "Feature": feat,
                        "Shift": (s1r > s2r) - (s1r < s2r)  # 1=勝ち, 0=引き分け, -1=負け
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
        return result, features_collected
    else:
        return result
