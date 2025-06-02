import pandas as pd
import random
from group_calculator import run_group_calculation
from hand_group_definitions import get_all_group_names
from utils import get_static_preflop_winrates

import streamlit as st
st.set_page_config(page_title="勝率変動ツール", layout="centered")

st.title("🃏 ポーカー勝率変動ツール")
st.markdown("### ハンドグループを選択して、勝率変動を計算します")

# --- 入力エリア ---
available_groups = get_all_group_names()
selected_group = st.selectbox("🎯 対象ハンドグループを選択", available_groups)

st.markdown("### 試行回数（モンテカルロ法）")
num_simulations = st.selectbox("シミュレーション回数", [10000, 30000, 50000], index=0)

st.markdown("### 相手ハンドレンジを選択")
range_option = st.radio("レンジ設定", ["すべて", "25%", "30%"], index=0)
selected_range = "all"
if range_option == "25%":
    selected_range = "25"
elif range_option == "30%":
    selected_range = "30"

six_player = st.checkbox("6人テーブル対応モード（他の4人にハンドを配って除外）", value=True)

show_feature_analysis = st.checkbox("📊 特徴量ごとの変化分析も表示する", value=True)

if st.button("✅ 勝率変動を計算"):
    st.info(f"計算中… グループ：`{selected_group}` / レンジ：`{range_option}` / 回数：`{num_simulations}`")

    df_results, df_features = run_group_calculation(
        group_name=selected_group,
        num_simulations=num_simulations,
        range_mode=selected_range,
        six_player_mode=six_player,
        return_feature_analysis=True
    )

    st.success("✅ 計算完了！")

    # 勝率結果表示
    st.subheader("📈 勝率変動結果")
    st.dataframe(df_results.style.format({
        "FlopWinrate": "{:.2f}%",
        "TurnWinrate": "{:.2f}%",
        "RiverWinrate": "{:.2f}%",
        "ShiftFlop": "{:+.2f}%",
        "ShiftTurn": "{:+.2f}%",
        "ShiftRiver": "{:+.2f}%"
    }))

    # 勝率結果CSVダウンロード
    csv1 = df_results.to_csv(index=False).encode("utf-8")
    st.download_button("📥 勝率結果をCSVでダウンロード", data=csv1, file_name="winrate_result.csv", mime="text/csv")

    if show_feature_analysis:
        st.subheader("🧠 特徴量ごとの勝率変化分析")
        st.dataframe(df_features.style.format({"AvgShift": "{:+.3f}"}))

        csv2 = df_features.to_csv(index=False).encode("utf-8")
        st.download_button("📥 特徴量分析結果をCSVでダウンロード", data=csv2, file_name="feature_analysis.csv", mime="text/csv")

# --- プリフロップ勝率表の表示 ---
st.markdown("### 🎯 代表的なハンドのプリフロップ勝率（vs ランダム）")
preflop_df = pd.DataFrame(get_static_preflop_winrates())
st.dataframe(preflop_df.style.format({"Winrate (%)": "{:.1f}"}))
