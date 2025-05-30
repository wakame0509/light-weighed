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

        opp_hand = [sim_deck.pop(), sim_deck.pop()] if not selected_range else random.choice(selected_range)

        try:
            flop_board = board + [sim_deck.pop() for _ in range(5 - len(board))]

            p1_flop = [eval7.Card(p1_card1), eval7.Card(p1_card2)] + [eval7.Card(c) for c in flop_board]
            p2_flop = [eval7.Card(c) for c in opp_hand] + [eval7.Card(c) for c in flop_board]
            s1_flop, s2_flop = evaluate_hand(p1_flop), evaluate_hand(p2_flop)

            flop_wins += s1_flop > s2_flop
            flop_ties += s1_flop == s2_flop

            turn_board = flop_board[:4] + [sim_deck.pop()]
            p1_turn = [eval7.Card(p1_card1), eval7.Card(p1_card2)] + [eval7.Card(c) for c in turn_board]
            p2_turn = [eval7.Card(c) for c in opp_hand] + [eval7.Card(c) for c in turn_board]
            s1_turn, s2_turn = evaluate_hand(p1_turn), evaluate_hand(p2_turn)

            turn_wins += s1_turn > s2_turn
            turn_ties += s1_turn == s2_turn

            river_board = turn_board[:5] + [sim_deck.pop()]
            p1_river = [eval7.Card(p1_card1), eval7.Card(p1_card2)] + [eval7.Card(c) for c in river_board]
            p2_river = [eval7.Card(c) for c in opp_hand] + [eval7.Card(c) for c in river_board]
            s1_river, s2_river = evaluate_hand(p1_river), evaluate_hand(p2_river)

            river_wins += s1_river > s2_river
            river_ties += s1_river == s2_river

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
