import streamlit as st
import pandas as pd
from hand_group_definitions import get_all_group_names
from group_calculator import run_group_calculation

st.set_page_config(page_title="勝率変動＋特徴量分析ツール", layout="centered")

st.title("🃏 ポーカー勝率変動＋特徴量分析")
st.markdown("### ハンドグループを選択して、勝率変動とその要因を分析します")

# グループ選択
available_groups = get_all_group_names()
selected_group = st.selectbox("🎯 対象ハンドグループを選択", available_groups)

# 試行回数
num_simulations = st.selectbox("🧮 シミュレーション回数（モンテカルロ法）", [10000, 30000, 50000], index=0)

# レンジ設定
range_option = st.radio("相手レンジ", ["すべて", "25%", "30%"], index=0)
selected_range = {"すべて": "all", "25%": "25", "30%": "30"}[range_option]

# 6人テーブル設定
six_player = st.checkbox("6人テーブルモード（他プレイヤー除外）", value=True)

# 実行
if st.button("✅ 計算・分析スタート"):
    st.info("計算中です。しばらくお待ちください...")
    result_df, feature_df = run_group_calculation(
        group_name=selected_group,
        num_simulations=num_simulations,
        range_mode=selected_range,
        six_player_mode=six_player,
        return_feature_analysis=True
    )

    st.success("✅ 完了しました！")

    st.subheader("📊 勝率変動結果")
    st.dataframe(result_df.style.format({
        "FlopWinrate": "{:.2f}%",
        "TurnWinrate": "{:.2f}%",
        "RiverWinrate": "{:.2f}%",
        "ShiftFlop": "{:+.2f}%",
        "ShiftTurn": "{:+.2f}%",
        "ShiftRiver": "{:+.2f}%"
    }))

    st.subheader("🔍 特徴量別の勝率変動分析（フロップ）")
    st.dataframe(feature_df.style.format({
        "Count": "{:.0f}",
        "AvgShift": "{:+.2f}%"
    }))

    # ダウンロード
    csv1 = result_df.to_csv(index=False).encode("utf-8")
    st.download_button("📥 勝率結果CSVダウンロード", csv1, file_name="winrate_result.csv", mime="text/csv")

    csv2 = feature_df.to_csv(index=False).encode("utf-8")
    st.download_button("📥 特徴量分析CSVダウンロード", csv2, file_name="feature_analysis.csv", mime="text/csv")
