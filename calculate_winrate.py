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

    feature_flags = []

    for _ in range(num_simulations):
        sim_deck = deck.copy()
        random.shuffle(sim_deck)

        # 相手ハンドを決定
        if selected_range:
            raw = random.choice(selected_range)
            if len(raw) == 2:
                r1, r2 = raw
                c1 = r1 + 'c'
                c2 = r2 + 'd'
            else:
                r1, r2, suited = raw
                if suited == "s":
                    suit = random.choice(['c', 'd', 'h', 's'])
                    c1 = r1 + suit
                    c2 = r2 + suit
                else:
                    suits_combo = random.sample(['c', 'd', 'h', 's'], 2)
                    c1 = r1 + suits_combo[0]
                    c2 = r2 + suits_combo[1]
            opp_hand = [c1, c2]
        else:
            opp_hand = [sim_deck.pop(), sim_deck.pop()]

        try:
            # フロップ（3枚）
            flop = board + [sim_deck.pop() for _ in range(3 - len(board))]
            p1_flop = [eval7.Card(p1_card1), eval7.Card(p1_card2)] + [eval7.Card(c) for c in flop]
            p2_flop = [eval7.Card(c) for c in opp_hand] + [eval7.Card(c) for c in flop]
            s1f, s2f = evaluate_hand(p1_flop), evaluate_hand(p2_flop)
            if s1f > s2f:
                flop_wins += 1
            elif s1f == s2f:
                flop_ties += 1

            # ターン（4枚目）
            turn = flop + [sim_deck.pop()]
            p1_turn = [eval7.Card(p1_card1), eval7.Card(p1_card2)] + [eval7.Card(c) for c in turn]
            p2_turn = [eval7.Card(c) for c in opp_hand] + [eval7.Card(c) for c in turn]
            s1t, s2t = evaluate_hand(p1_turn), evaluate_hand(p2_turn)
            if s1t > s2t:
                turn_wins += 1
            elif s1t == s2t:
                turn_ties += 1

            # リバー（5枚目）
            river = turn + [sim_deck.pop()]
            p1_river = [eval7.Card(p1_card1), eval7.Card(p1_card2)] + [eval7.Card(c) for c in river]
            p2_river = [eval7.Card(c) for c in opp_hand] + [eval7.Card(c) for c in river]
            s1r, s2r = evaluate_hand(p1_river), evaluate_hand(p2_river)
            if s1r > s2r:
                river_wins += 1
            elif s1r == s2r:
                river_ties += 1

            if return_features:
                # 特徴量フラグ（例: paired flop）
                flop_ranks = [card[0] for card in flop]
                flop_suits = [card[1] for card in flop]
                paired = len(set(flop_ranks)) < 3
                monotone = len(set(flop_suits)) == 1
                feature_flags.append({
                    "Feature": "PairedFlop" if paired else ("MonotoneFlop" if monotone else "NormalFlop"),
                    "Shift": s1r - s2r
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
        return result, feature_flags
    else:
        return result
