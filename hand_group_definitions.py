# hand_group_definitions.py

hand_groups = {
    "High Pair": [["A", "A"], ["K", "K"], ["Q", "Q"]],
    "Mid Pair": [["J", "J"], ["T", "T"], ["9", "9"]],
    "Low Pair": [["8", "8"], ["7", "7"], ["6", "6"], ["5", "5"], ["4", "4"], ["3", "3"], ["2", "2"]],
    
    "High Suited Connector": [["A", "K", "s"], ["K", "Q", "s"], ["Q", "J", "s"], ["J", "T", "s"]],
    "Low Suited Connector": [["6", "5", "s"], ["5", "4", "s"], ["4", "3", "s"], ["3", "2", "s"]],
    
    "High Offsuit Connector": [["A", "K", "o"], ["K", "Q", "o"], ["Q", "J", "o"]],
    "Low Offsuit Connector": [["6", "5", "o"], ["5", "4", "o"], ["4", "3", "o"]],
    
    "High Broadway": [["A", "K"], ["A", "Q"], ["K", "Q"]],
    "Low Broadway": [["J", "T"], ["T", "9"], ["9", "8"]],
    
    "Suited Ace": [["A", r, "s"] for r in ["K", "Q", "J", "T", "9", "8", "7", "6", "5", "4", "3", "2"]],
    "Suited King": [["K", r, "s"] for r in ["Q", "J", "T", "9", "8", "7", "6", "5", "4", "3", "2"]],
    
    "Suited One-Gapper": [["9", "7", "s"], ["8", "6", "s"], ["7", "5", "s"], ["6", "4", "s"]]
}

def get_all_group_names():
    return list(hand_groups.keys())

def get_group_hands(group_name):
    return hand_groups.get(group_name, [])
