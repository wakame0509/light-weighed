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
                          extra_excluded=None, num_simulations=10000):
    known = [p1_card1, p1_card2] + board
    full_deck = generate_deck()
    deck = remove_known_cards(full_deck, known)

    if extra_excluded:
        deck = remove_known_cards(deck, extra_excluded)

    flop_wins = turn_wins = river_wins = 0
    flop_ties = turn_ties = river_ties = 0

    for _ in range(num_simulations):
        sim_deck = deck.copy()
        random.shuffle(sim_deck)

        # 相手のハンドをセット
        opp_hand = random.choice(selected_range) if selected_range else [sim_deck.pop(), sim_deck.pop()]

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

        except Exception:
            continue

    flop_winrate = (flop_wins + flop_ties / 2) / num_simulations * 100
    turn_winrate = (turn_wins + turn_ties / 2) / num_simulations * 100
    river_winrate = (river_wins + river_ties / 2) / num_simulations * 100

    return {
        "Preflop": 0.0,
        "FlopWinrate": flop_winrate,
        "TurnWinrate": turn_winrate,
        "RiverWinrate": river_winrate,
        "ShiftFlop": flop_winrate,
        "ShiftTurn": turn_winrate - flop_winrate,
        "ShiftRiver": river_winrate - turn_winrate
    }
