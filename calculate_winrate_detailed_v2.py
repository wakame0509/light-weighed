# calculate_winrate_detailed_v2.py
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

def run_winrate_vs_flops(p1_card1, p1_card2, flop_list, selected_range=None,
                         extra_excluded=None, num_simulations=1000):
    results = []

    full_deck = generate_deck()
    known = [p1_card1, p1_card2]
    if extra_excluded:
        known += extra_excluded
    deck = remove_known_cards(full_deck, known)

    for flop in flop_list:
        flop = list(flop)
        flop_wins = flop_ties = 0
        turn_wins = turn_ties = 0
        river_wins = river_ties = 0

        for _ in range(num_simulations):
            sim_deck = remove_known_cards(deck, flop).copy()
            random.shuffle(sim_deck)

            if selected_range:
                opp_hand = random.choice(selected_range)
                if len(opp_hand) == 2:
                    o_card1 = opp_hand[0]
                    o_card2 = opp_hand[1]
                else:
                    rank1, rank2, suited = opp_hand
                    suit1 = 's'
                    suit2 = 's' if suited == 's' else 'h'
                    o_card1 = rank1 + suit1
                    o_card2 = rank2 + suit2
            else:
                o_card1 = sim_deck.pop()
                o_card2 = sim_deck.pop()

            try:
                p1_flop = [eval7.Card(p1_card1), eval7.Card(p1_card2)] + [eval7.Card(c) for c in flop]
                p2_flop = [eval7.Card(o_card1), eval7.Card(o_card2)] + [eval7.Card(c) for c in flop]
                s1f, s2f = evaluate_hand(p1_flop), evaluate_hand(p2_flop)
                if s1f > s2f:
                    flop_wins += 1
                elif s1f == s2f:
                    flop_ties += 1

                turn = flop + [sim_deck.pop()]
                p1_turn = [eval7.Card(p1_card1), eval7.Card(p1_card2)] + [eval7.Card(c) for c in turn]
                p2_turn = [eval7.Card(o_card1), eval7.Card(o_card2)] + [eval7.Card(c) for c in turn]
                s1t, s2t = evaluate_hand(p1_turn), evaluate_hand(p2_turn)
                if s1t > s2t:
                    turn_wins += 1
                elif s1t == s2t:
                    turn_ties += 1

                river = turn + [sim_deck.pop()]
                p1_river = [eval7.Card(p1_card1), eval7.Card(p1_card2)] + [eval7.Card(c) for c in river]
                p2_river = [eval7.Card(o_card1), eval7.Card(o_card2)] + [eval7.Card(c) for c in river]
                s1r, s2r = evaluate_hand(p1_river), evaluate_hand(p2_river)
                if s1r > s2r:
                    river_wins += 1
                elif s1r == s2r:
                    river_ties += 1

            except Exception:
                continue

        flop_wr = (flop_wins + flop_ties / 2) / num_simulations * 100
        turn_wr = (turn_wins + turn_ties / 2) / num_simulations * 100
        river_wr = (river_wins + river_ties / 2) / num_simulations * 100

        results.append({
            "Hand": p1_card1 + p1_card2,
            "Flop": flop,
            "FlopWinrate": flop_wr,
            "TurnWinrate": turn_wr,
            "RiverWinrate": river_wr,
            "ShiftFlop": flop_wr,
            "ShiftTurn": turn_wr - flop_wr,
            "ShiftRiver": river_wr - turn_wr
        })

    return results
