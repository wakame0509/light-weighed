from typing import List

def extract_features(hand: List[str], flop: List[str]) -> dict:
    """
    プレイヤーのハンドとフロップから特徴量を抽出する。
    :param hand: 例 ['8h', '8d']
    :param flop: 例 ['Ks', '2d', '8c']
    :return: 特徴量を示すdict
    """
    ranks_order = '23456789TJQKA'
    suits = [c[1] for c in flop]
    flop_ranks = [c[0] for c in flop]
    hand_ranks = [c[0] for c in hand]

    # 1. オーバーカードの数
    max_hand_rank = max(hand_ranks, key=lambda r: ranks_order.index(r))
    overcards = sum(ranks_order.index(r) > ranks_order.index(max_hand_rank) for r in flop_ranks)

    # 2. セット完成
    is_pair = hand_ranks[0] == hand_ranks[1]
    set_made = is_pair and hand_ranks[0] in flop_ranks

    # 3. モノトーン
    is_monotone = len(set(suits)) == 1

    # 4. フラッシュドロー（手札とフロップで同じスートが4枚以上）
    suit_counts = {s: suits.count(s) for s in 'cdhs'}
    for s in hand:
        suit_counts[s[1]] = suit_counts.get(s[1], 0) + 1
    has_flush_draw = any(v >= 4 for v in suit_counts.values())

    # 5. ストレートドロー（簡易判定：3+2枚の中に連番4つあれば可能性）
    all_ranks = hand_ranks + flop_ranks
    uniq_ranks = sorted(set(all_ranks), key=lambda r: ranks_order.index(r))
    idx_list = [ranks_order.index(r) for r in uniq_ranks]
    straight_draw = False
    for i in range(len(idx_list) - 3):
        if idx_list[i+3] - idx_list[i] <= 4:
            straight_draw = True
            break

    return {
        "Overcards": overcards,
        "SetMade": set_made,
        "Monotone": is_monotone,
        "FlushDraw": has_flush_draw,
        "StraightDraw": straight_draw
    }
