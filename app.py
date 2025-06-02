import streamlit as st
import pandas as pd
from analyze_detailed_features import analyze_detailed_features
from utils import get_static_preflop_winrates

# タイトル
st.title("📊 テキサスホールデム 勝率変動ランキング")

# 説明
st.markdown("""
このアプリでは、各ハンドに対して **どのようなフロップ・ターン・リバーの特徴** が
勝率にどう影響するかを表示します。勝率が大きく上昇・下降した要因の特徴量も横に表示されます。
""")

# --- データ読み込み（サンプルデータ） ---
sample_data = [
    {"Hand": "AKs", "ShiftFlop": 4.2, "ShiftTurn": 1.5, "ShiftRiver": -0.3, "Feature": "OvercardOnFlop"},
    {"Hand": "QJo", "ShiftFlop": -2.1, "ShiftTurn": -0.7, "ShiftRiver": -1.0, "Feature": "PairedFlop"},
    {"Hand": "99",  "ShiftFlop": 3.8, "ShiftTurn": 1.2, "ShiftRiver": 0.5, "Feature": "PairedFlop"},
    {"Hand": "JTs", "ShiftFlop": 5.5, "ShiftTurn": 1.9, "ShiftRiver": -0.1, "Feature": "StraightDrawFlop"},
    {"Hand": "55",  "ShiftFlop": -4.3, "ShiftTurn": -1.0, "ShiftRiver": -1.2, "Feature": "OvercardOnFlop"},
    {"Hand": "AQo", "ShiftFlop": 2.5, "ShiftTurn": 0.9, "ShiftRiver": -0.4, "Feature": "MonotoneFlop"},
    {"Hand": "KQs", "ShiftFlop": 1.1, "ShiftTurn": 0.7, "ShiftRiver": 0.3, "Feature": "NormalFlop"},
    {"Hand": "44",  "ShiftFlop": -5.2, "ShiftTurn": -1.5, "ShiftRiver": -0.7, "Feature": "OvercardOnFlop"},
    {"Hand": "87s", "ShiftFlop": 3.3, "ShiftTurn": 1.1, "ShiftRiver": -0.6, "Feature": "ConnectedFlop"},
    {"Hand": "T9s", "ShiftFlop": 4.7, "ShiftTurn": 2.0, "ShiftRiver": -0.2, "Feature": "StraightDrawFlop"},
    {"Hand": "66",  "ShiftFlop": -3.9, "ShiftTurn": -1.3, "ShiftRiver": -0.5, "Feature": "OvercardOnFlop"},
    {"Hand": "AJo", "ShiftFlop": 2.9, "ShiftTurn": 1.4, "ShiftRiver": 0.1, "Feature": "NormalFlop"},
]

df = pd.DataFrame(sample_data)

# --- 勝率変動ランキング表示 ---
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

# 各ステージごとに表示
show_shift_ranking("Flop")
show_shift_ranking("Turn")
show_shift_ranking("River")

# --- プリフロップ勝率表の表示 ---
st.markdown("### 🎯 代表的なハンドのプリフロップ勝率（vs ランダム）")

preflop_df = pd.DataFrame(get_static_preflop_winrates().items(), columns=["Hand", "Winrate"])
preflop_df = preflop_df.sort_values(by="Winrate", ascending=False).reset_index(drop=True)
st.dataframe(preflop_df)
