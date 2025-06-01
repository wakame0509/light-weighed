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

def get_feature_flags(p1_hand, board, shift):
    features = []

    ranks_on_board = [card[0] for card in board]
    board_ranks = set(ranks_on_board)
    max_board_rank = max("23456789TJQKA".index(r) for r in ranks_on_board) if ranks_on_board else -1
    hand_ranks = [p1_hand[0][0], p1_hand[1][0]]
    min_hand_rank = min("23456789TJQKA".index(r) for r in hand_ranks)

    # 特徴量例：オーバーカード出現
    if max_board_rank > min_hand_rank:
        features.append({"Feature": "Overcard on board", "Shift": shift})

    # フラッシュドローの可能性
    suits = [c[1] for c in board + p1_hand]
    for s in "cdhs":
        if suits.count(s) >= 4:
            features.append({"Feature": "Flush draw possible", "Shift": shift})
            break

    # ストレートドローの可能性（簡易）
    rank_index = {r: i for i, r in enumerate("23456789TJQKA")}
    idx_list = sorted(rank_index[r] for r in board_ranks)
    for i in range(len(idx_list) - 2):
        if idx_list[i+2] - idx_list[i] <= 4:
            features.append({"Feature": "Straight draw possible", "Shift": shift})
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
    feature_records = []

    for _ in range(num_simulations):
        sim_deck = deck.copy()
        random.shuffle(sim_deck)

        opp_hand = random.choice(selected_range) if selected_range else [sim_deck.pop(), sim_deck.pop()]
        try:
            flop = board + [sim_deck.pop() for _ in range(3 - len(board))]
            p1_hand = [p1_card1, p1_card2]

            p1_flop = [eval7.Card(c) for c in p1_hand + flop]
            p2_flop = [eval7.Card(c) for c in opp_hand + flop]
            s1f, s2f = evaluate_hand(p1_flop), evaluate_hand(p2_flop)
            if s1f > s2f:
                flop_wins += 1
            elif s1f == s2f:
                flop_ties += 1

            turn = flop + [sim_deck.pop()]
            p1_turn = [eval7.Card(c) for c in p1_hand + turn]
            p2_turn = [eval7.Card(c) for c in opp_hand + turn]
            s1t, s2t = evaluate_hand(p1_turn), evaluate_hand(p2_turn)
            if s1t > s2t:
                turn_wins += 1
            elif s1t == s2t:
                turn_ties += 1

            river = turn + [sim_deck.pop()]
            p1_river = [eval7.Card(c) for c in p1_hand + river]
            p2_river = [eval7.Card(c) for c in opp_hand + river]
            s1r, s2r = evaluate_hand(p1_river), evaluate_hand(p2_river)
            if s1r > s2r:
                river_wins += 1
            elif s1r == s2r:
                river_ties += 1

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
        feature_records = get_feature_flags([p1_card1, p1_card2], flop, result["ShiftFlop"])
        return result, feature_records

    return result
