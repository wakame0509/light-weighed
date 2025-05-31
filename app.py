import streamlit as st
import pandas as pd
from group_calculator import run_group_calculation
from hand_group_definitions import get_all_group_names

st.set_page_config(page_title="勝率変動ツール（分担・保存対応）", layout="centered")

st.title("🃏 ポーカー勝率変動ツール")
st.markdown("### ハンドグループを選択して、勝率変動を計算します")

# --- 入力エリア ---
available_groups = get_all_group_names()
selected_group = st.selectbox("🎯 対象ハンドグループを選択", available_groups)

# モンテカルロ試行回数選択
st.markdown("### 試行回数（モンテカルロ法）")
num_simulations = st.selectbox("シミュレーション回数", [10000, 30000, 50000], index=0)

# レンジ選択
st.markdown("### 相手ハンドレンジを選択")
range_option = st.radio("レンジ設定", ["すべて", "25%", "30%"], index=0)
selected_range = None
if range_option == "25%":
    selected_range = "25"
elif range_option == "30%":
    selected_range = "30"
else:
    selected_range = "all"

# 6人テーブル対応チェックボックス
six_player = st.checkbox("6人テーブル対応モード（他の4人にハンドを配って除外）", value=True)

# --- 実行ボタン ---
if st.button("✅ 勝率変動を計算"):
    st.write(f"計算中… グループ：`{selected_group}` / レンジ：`{range_option}` / 回数：`{num_simulations}`")
    result_df = run_group_calculation(
        group_name=selected_group,
        num_simulations=num_simulations,
        range_mode=selected_range,
        six_player_mode=six_player
    )

    # 結果表示
    st.success("✅ 計算完了！")
    st.dataframe(result_df.style.format({
        "FlopWinrate": "{:.2f}%",
        "TurnWinrate": "{:.2f}%",
        "RiverWinrate": "{:.2f}%",
        "ShiftFlop": "{:+.2f}%",
        "ShiftTurn": "{:+.2f}%",
        "ShiftRiver": "{:+.2f}%"
    }))

    # CSV保存
    csv = result_df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="📥 結果をCSVでダウンロード",
        data=csv,
        file_name=f"{selected_group}_winrate_shift.csv",
        mime="text/csv"
    )
