import streamlit as st
import pandas as pd
from group_calculator import run_group_calculation
from hand_group_definitions import get_all_group_names

st.set_page_config(page_title="勝率変動ツール（特徴量分析つき）", layout="centered")

st.title("🃏 ポーカー勝率変動ツール")
st.markdown("### ハンドグループを選択して、勝率変動と特徴量を分析します")

# --- 入力エリア ---
available_groups = get_all_group_names()
selected_group = st.selectbox("🎯 対象ハンドグループを選択", available_groups)

# モンテカルロ試行回数選択
st.markdown("### 試行回数（モンテカルロ法）")
num_simulations = st.selectbox("シミュレーション回数", [10000, 30000, 50000], index=0)

# レンジ選択
st.markdown("### 相手ハンドレンジを選択")
range_option = st.radio("レンジ設定", ["すべて", "25%", "30%"], index=0)
selected_range = "all"
if range_option == "25%":
    selected_range = "25"
elif range_option == "30%":
    selected_range = "30"

# 6人テーブル対応チェックボックス
six_player = st.checkbox("6人テーブル対応モード（他の4人にハンドを配って除外）", value=True)

# 実行ボタン
if st.button("✅ 勝率変動と特徴量を計算"):
    st.info(f"計算中… グループ：`{selected_group}` / レンジ：`{range_option}` / 回数：`{num_simulations}`")
    
    result_df, feature_df = run_group_calculation(
        group_name=selected_group,
        num_simulations=num_simulations,
        range_mode=selected_range,
        six_player_mode=six_player,
        return_feature_analysis=True
    )

    st.success("✅ 計算完了！")
from preflop_winrates import preflop_winrates
    st.markdown("### 🎯 代表的なハンドのプリフロップ勝率（vs ランダム）")
    with st.expander("クリックで表示"):
        df_preflop = pd.DataFrame([
            {"Hand": k, "Preflop Winrate (%)": v} for k, v in preflop_winrates.items()
        ])
        df_preflop = df_preflop.sort_values(by="Preflop Winrate (%)", ascending=False)
        st.dataframe(df_preflop.reset_index(drop=True))
    # 勝率結果
    st.subheader("📊 勝率変動結果")
    st.dataframe(result_df.style.format({
        "FlopWinrate": "{:.2f}%",
        "TurnWinrate": "{:.2f}%",
        "RiverWinrate": "{:.2f}%",
        "ShiftFlop": "{:+.2f}%",
        "ShiftTurn": "{:+.2f}%",
        "ShiftRiver": "{:+.2f}%"
    }))

    # 特徴量別分析結果
    st.subheader("🧠 特徴量ごとの勝率変化分析")
    st.dataframe(feature_df.style.format({
        "AvgShift": "{:+.3f}",
        "Count": "{:d}"
    }))

    # CSVダウンロード
    st.download_button(
        label="📥 勝率結果をCSVでダウンロード",
        data=result_df.to_csv(index=False).encode("utf-8"),
        file_name=f"{selected_group}_winrate_results.csv",
        mime="text/csv"
    )

    st.download_button(
        label="📥 特徴量分析結果をCSVでダウンロード",
        data=feature_df.to_csv(index=False).encode("utf-8"),
        file_name=f"{selected_group}_feature_analysis.csv",
        mime="text/csv"
    )
