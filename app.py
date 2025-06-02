import streamlit as st
import pandas as pd
from group_calculator import run_group_calculation
from utils import get_group_hands, get_hand_range_25, get_hand_range_30
from analyze_detailed_features import analyze_detailed_features

st.set_page_config(layout="wide")

st.title("♠ テキサスホールデム 勝率変動分析ツール")

st.markdown("このツールでは、プリフロップからリバーまでの勝率変動や影響する特徴量を分析できます。")

# --- 入力セクション ---
group = st.selectbox("🔍 分析するハンドグループを選択", [
    "High Pair", "Middle Pair", "Low Pair",
    "Broadway", "Ace-High", "Suited Connectors",
    "Offsuit Connectors", "Suited One-Gappers",
    "Offsuit One-Gappers", "Suited Two-Gappers",
    "Offsuit Two-Gappers", "Trash"
])

range_mode = st.radio("🎯 相手レンジ", options=["None", "25", "30"], index=0)
six_player = st.checkbox("6人テーブル（他4人のカード除外）", value=False)
simulations = st.select_slider("🎲 モンテカルロ試行回数", options=[10000, 50000, 100000], value=50000)

if st.button("✅ 勝率変動を計算・分析開始"):
    with st.spinner("計算中..."):
        df_result, df_features = run_group_calculation(
            group_name=group,
            num_simulations=simulations,
            range_mode=range_mode,
            six_player_mode=six_player,
            return_feature_analysis=True
        )

        st.markdown("### 🧮 勝率変動（ハンド別）")
        st.dataframe(df_result)

        st.markdown("### 🔬 特徴量別の平均勝率変動")
        st.dataframe(df_features)

# --- プリフロップ勝率表（静的） ---
from utils import get_static_preflop_winrates

st.markdown("### 📊 代表的なハンドのプリフロップ勝率（vs ランダム）")
preflop_df = pd.DataFrame(get_static_preflop_winrates())
st.dataframe(preflop_df)

# --- フロップ勝率変動ランキング（事前に保存されたCSVを使用） ---
st.markdown("### 🏆 フロップ勝率変動ランキング")

try:
    df = pd.read_csv("results/detailed_shifts.csv")
except FileNotFoundError:
    st.warning("⚠️ 分析結果ファイル（results/detailed_shifts.csv）が見つかりません。")
    df = pd.DataFrame()

if not df.empty:
    top_increase = df.sort_values(by="ShiftFlop", ascending=False).head(10)
    top_decrease = df.sort_values(by="ShiftFlop", ascending=True).head(10)

    st.markdown("#### 📈 勝率上昇トップ10")
    st.dataframe(top_increase[["Hand", "ShiftFlop", "Feature"]])

    st.markdown("#### 📉 勝率下降トップ10")
    st.dataframe(top_decrease[["Hand", "ShiftFlop", "Feature"]])
else:
    st.info("結果データがまだ生成されていないか、ファイルが読み込まれていません。")
