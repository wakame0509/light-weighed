import streamlit as st
import pandas as pd
from utils import get_static_preflop_winrates

st.title("📊 テキサスホールデム 勝率変動ランキング")

st.markdown("""
このアプリでは、各ハンドに対して **どのようなフロップ・ターン・リバーの特徴** が
勝率にどう影響するかを表示します。勝率が大きく上昇・下降した要因の特徴量も横に表示されます。
""")

# --- CSVから読み込み ---
@st.cache_data
def load_shift_data():
    return pd.read_csv("detailed_shift_data.csv")

df = load_shift_data()

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
