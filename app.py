import streamlit as st
import pandas as pd
from utils import (
    get_hand_group_dict, get_group_hands,
    get_hand_range_25, get_hand_range_30,
    get_static_preflop_winrates
)
from flop_samples import representative_flops
from calculate_winrate_detailed_v2 import run_winrate_evolution

st.set_page_config(layout="wide")
st.title("♠️ テキサスホールデム 勝率変動ランキング（自動計算）")

st.markdown("""
このアプリでは、指定した **ハンドグループ** に対して代表的な100フロップを使って勝率変動を自動計算します。  
相手のハンドレンジも指定可能で、**Flop/Turn/Riverの変動幅のランキング**とその要因となる**特徴量**を表示します。
""")

# --- 入力UI ---
group_names = list(get_hand_group_dict().keys())
selected_group = st.selectbox("📂 対象ハンドグループを選択", group_names)

range_option = st.selectbox("🎯 相手のハンドレンジを選択", ["ランダム", "上位25%", "上位30%"])
if range_option == "上位25%":
    selected_range = get_hand_range_25()
elif range_option == "上位30%":
    selected_range = get_hand_range_30()
else:
    selected_range = None

num_simulations = st.selectbox("🔁 シミュレーション回数（1ハンド×1フロップあたり）", [1000, 5000, 10000], index=1)

if st.button("🚀 勝率変動を計算"):
    st.markdown("🧮 計算中...少々お待ちください")
    hands = get_group_hands(selected_group)
    all_results = []

    for hand in hands:
        card1 = hand[0] + 's'
        card2 = hand[1] + 'h' if len(hand) == 2 else hand[1] + ('s' if hand[2] == "o" else 'd')
        shorthand = "".join(hand) if len(hand) == 2 else hand[0] + hand[1] + hand[2]

        total_flop_shift = turn_shift = river_shift = 0
        features_counter = {}
        count = 0

        for flop in representative_flops:
            board = flop[:]
            try:
                result, feature_flags = run_winrate_evolution(
                    card1, card2, board=board,
                    selected_range=selected_range,
                    num_simulations=num_simulations,
                    return_features=True
                )
                total_flop_shift += result["ShiftFlop"]
                turn_shift += result["ShiftTurn"]
                river_shift += result["ShiftRiver"]
                count += 1

                for f in feature_flags:
                    key = f["Feature"]
                    features_counter[key] = features_counter.get(key, 0) + f["Shift"]
            except Exception:
                continue

        if count == 0:
            continue

        most_common_feature = max(features_counter.items(), key=lambda x: abs(x[1]))[0] if features_counter else "N/A"

        all_results.append({
            "Hand": shorthand,
            "ShiftFlop": round(total_flop_shift / count, 2),
            "ShiftTurn": round(turn_shift / count, 2),
            "ShiftRiver": round(river_shift / count, 2),
            "Feature": most_common_feature
        })

    if not all_results:
        st.error("計算に失敗しました。カードの重複やデッキ不足が原因かもしれません。")
    else:
        df = pd.DataFrame(all_results)

        def show_shift_ranking(stage):
            st.markdown(f"### 💡 {stage} 勝率変動ランキング")

            top10 = df.sort_values(by=f"Shift{stage}", ascending=False).head(10)
            bottom10 = df.sort_values(by=f"Shift{stage}", ascending=True).head(10)

            col1, col2 = st.columns(2)

            with col1:
                st.markdown("#### 🔼 上昇幅 Top10")
                st.dataframe(top10[["Hand", f"Shift{stage}", "Feature"]].reset_index(drop=True))

            with col2:
                st.markdown("#### 🔽 下降幅 Top10")
                st.dataframe(bottom10[["Hand", f"Shift{stage}", "Feature"]].reset_index(drop=True))

        show_shift_ranking("Flop")
        show_shift_ranking("Turn")
        show_shift_ranking("River")

        # プリフロップ参考表示
        st.markdown("### 🎯 代表的なハンドのプリフロップ勝率（vs ランダム）")
        preflop_df = pd.DataFrame(get_static_preflop_winrates().items(), columns=["Hand", "Winrate"])
        preflop_df = preflop_df.sort_values(by="Winrate", ascending=False).reset_index(drop=True)
        st.dataframe(preflop_df)
