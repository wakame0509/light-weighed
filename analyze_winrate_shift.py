import eval7
import random
import pandas as pd
from utils import get_group_hands

RANK_TO_INT = {'2': 2, '3': 3, '4': 4, '5': 5,
               '6': 6, '7': 7, '8': 8, '9': 9,
               'T': 10, 'J': 11, 'Q': 12, 'K': 13, 'A': 14}

def evaluate(cards):
    return eval7.evaluate(cards)

def generate_deck():
    return [r + s for r in '23456789TJQKA' for s in 'cdhs']

def detect_overcard(hand_rank, flop):
    flop_ranks = [RANK_TO_INT[c[0]] for c in flop]
    return any(r > hand_rank for r in flop_ranks)

def simulate_winrate_with_features(group_name, flop, num_simulations=1000):
    results = []
    hands = get_group_hands(group_name)

    for hand in hands:
        try:
            if len(hand) == 2:
                rank1, rank2 = hand
                suit1, suit2 = "s", "h"
            elif len(hand) == 3:
                rank1, rank2, suited_flag = hand
                suit1 = "s"
                suit2 = "s" if suited_flag == "s" else "h"
            else:
                continue

            card1 = rank1 + suit1
            card2 = rank2 + suit2

            win = tie = 0
            deck = generate_deck()
            known = [card1, card2] + flop
            for c in known:
                deck.remove(c)

            for _ in range(num_simulations):
                d = deck.copy()
                random.shuffle(d)
                opp1, opp2 = d.pop(), d.pop()
                board = flop + [d.pop(), d.pop()]  # turn + river

                p1_cards = [eval7.Card(c) for c in [card1, card2] + flop]
                p2_cards = [eval7.Card(c) for c in [opp1, opp2] + flop]

                s1 = evaluate(p1_cards)
                s2 = evaluate(p2_cards)

                if s1 > s2:
                    win += 1
                elif s1 == s2:
                    tie += 1

            winrate = (win + tie / 2) / num_simulations * 100
            feature = {
                "Group": group_name,
                "Hand": card1 + card2,
                "Flop": " ".join(flop),
                "Winrate": winrate,
                "OvercardExists": detect_overcard(RANK_TO_INT[rank1], flop)
            }
            results.append(feature)
        except Exception as e:
            print(f"エラー ({hand}): {e}")
            continue

    return pd.DataFrame(results)
