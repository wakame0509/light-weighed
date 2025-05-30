import streamlit as st
import pandas as pd
from calculate_winrate_single import run_winrate_evolution
from utils import generate_deck, remove_known_cards, get_hand_group_dict

st.title("📈 ハンドグループごとの勝率変動計算")

# --- UI部分 ---
hand_groups = [
    "High Pair", "Mid Pair", "Low Pair",
    "High Suited Connector", "Low Suited Connector",
    "High Offsuit Connector", "Low Offsuit Connector",
    "High Broadway", "Low Broadway",
    "Suited Ace", "Suited King", "Suited One-Gapper"
]

selected_groups = st.multiselect("📌 計算するハンドグループを選んでください", hand_groups)

flop_options = st.selectbox(
    "🃏 フロップパターンを選択（例: ['Ah', 'Kd', '7s']）",
    options=[
        ["Ah", "Kd", "7s"],
        ["8c", "9d", "Ts"],
        ["2d", "2c", "5h"],
        ["Qs", "Qc", "3h"],
        ["Jd", "Td", "9d"],
        ["3c", "4c", "5c"],
        ["7s", "8s", "9h"],
        ["6d", "7d", "8d"],
        ["As", "Ks", "Qs"],
        ["9h", "9c", "9s"]
    ]
)

num_simulations = st.selectbox("🧮 モンテカルロ試行回数", [10000, 50000, 100000])

start_button = st.button("🚀 計算スタート")

# --- 計算実行 ---
results = []

if start_button and selected_groups:
    st.info("計算中です。しばらくお待ちください。")

    hand_dict = get_hand_group_dict()
    selected_hands = []

    for group in selected_groups:
        selected_hands.extend(hand_dict.get(group, []))

    for hand in selected_hands:
        try:
            card1, card2 = hand
            result = run_winrate_evolution(
                card1, card2, flop_options, selected_range=None,
                extra_excluded=None, num_simulations=num_simulations
            )
            result["Hand"] = f"{card1}{card2}"
            result["Group"] = group
            result["Flop"] = flop_options
            results.append(result)
        except Exception as e:
            st.warning(f"{hand} の処理中にエラーが発生しました: {e}")

# --- 結果表示と保存 ---
if results:
    st.subheader("📊 計算結果（勝率変動）")

    df = pd.DataFrame(results)

    st.dataframe(df.style.format({
        "FlopWinrate": "{:.2f}%",
        "TurnWinrate": "{:.2f}%",
        "RiverWinrate": "{:.2f}%",
        "ShiftFlop": "{:+.2f}%",
        "ShiftTurn": "{:+.2f}%",
        "ShiftRiver": "{:+.2f}%"
    }))

    csv_data = df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="📥 CSVとして保存",
        data=csv_data,
        file_name="winrate_results.csv",
        mime="text/csv"
    )
