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
from hand_group_definitions import hand_groups

def get_group_hands(group_name):
    """
    指定されたハンドグループ名に対応するハンド一覧を返す。
    """
    return hand_groups.get(group_name, [])
