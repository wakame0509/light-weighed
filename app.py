import streamlit as st
import pandas as pd
from group_calculator import run_group_calculation
from hand_group_definitions import get_all_group_names

st.set_page_config(page_title="勝率変動ツール（特徴量分析付き）", layout="centered")

st.title("🃏 ポーカー勝率変動・特徴量分析ツール")
st.markdown("### ✅ 複数のハンドグループを選択して勝率変動と特徴量を計算します")

# ハンドグループ選択（複数可）
available_groups = get_all_group_names()
selected_groups = st.multiselect("🎯 対象ハンドグループを選択", available_groups)

# モンテカルロ試行回数選択
st.markdown("### 試行回数（モンテカルロ法）")
num_simulations = st.selectbox("シミュレーション回数", [10000, 30000, 50000], index=0)

# レンジ選択
st.markdown("### 相手ハンドレンジを選択")
range_option = st.radio("レンジ設定", ["すべて", "25%", "30%"], index=0)
selected_range = {"すべて": "all", "25%": "25", "30%": "30"}[range_option]

# 6人テーブル対応チェック
six_player = st.checkbox("6人テーブル対応モード（他4人のハンド除外）", value=True)

# 実行
if st.button("🚀 勝率変動＋特徴量分析を開始"):
    if not selected_groups:
        st.warning("⚠️ ハンドグループを1つ以上選択してください。")
    else:
        st.info("計算中です。しばらくお待ちください…")

        df_all = pd.DataFrame()
        for group in selected_groups:
            df = run_group_calculation(
                group_name=group,
                num_simulations=num_simulations,
                range_mode=selected_range,
                six_player_mode=six_player
            )
            df_all = pd.concat([df_all, df], ignore_index=True)

        # 結果表示
        st.success("✅ 計算完了！")
        st.dataframe(df_all.style.format({
            "FlopWinrate": "{:.2f}%",
            "TurnWinrate": "{:.2f}%",
            "RiverWinrate": "{:.2f}%",
            "ShiftFlop": "{:+.2f}%",
            "ShiftTurn": "{:+.2f}%",
            "ShiftRiver": "{:+.2f}%",
        }))

        # CSVダウンロード
        csv = df_all.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="📥 特徴量付き結果をCSVで保存",
            data=csv,
            file_name="winrate_with_features.csv",
            mime="text/csv"
        )
