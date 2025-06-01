from hand_group_definitions import hand_groups
import random

def generate_deck():
    """52枚のデッキを生成"""
    ranks = "23456789TJQKA"
    suits = "cdhs"
    return [r + s for r in ranks for s in suits]

def remove_known_cards(deck, known_cards):
    """指定されたカードをデッキから除外"""
    return [card for card in deck if card not in known_cards]

def get_hand_group_dict():
    """ハンドグループの辞書を取得"""
    return hand_groups

def get_group_hands(group_name):
    """指定されたハンドグループ名に対応するハンド一覧を返す"""
    return hand_groups.get(group_name, [])

def get_hand_range_25():
    """実戦向けの上位25%レンジ（PokerStoveベース）"""
    return [
        ["A", "A"], ["K", "K"], ["Q", "Q"], ["J", "J"], ["T", "T"],
        ["9", "9"], ["8", "8"], ["7", "7"], ["6", "6"],
        ["A", "K", "s"], ["A", "Q", "s"], ["A", "J", "s"], ["A", "T", "s"], ["K", "Q", "s"],
        ["K", "J", "s"], ["Q", "J", "s"], ["J", "T", "s"], ["T", "9", "s"],
        ["A", "K", "o"], ["A", "Q", "o"], ["A", "J", "o"], ["K", "Q", "o"]
    ]

def get_hand_range_30():
    """実戦向けの上位30%レンジ（25%に追加）"""
    return get_hand_range_25() + [
        ["5", "5"], ["4", "4"],
        ["9", "8", "s"], ["8", "7", "s"], ["Q", "T", "s"], ["K", "T", "s"],
        ["A", "T", "o"], ["K", "J", "o"], ["Q", "J", "o"]
    ]
