import streamlit as st
import pandas as pd
from utils import get_all_group_names, get_static_preflop_winrates
from group_calculator import run_group_calculation

st.set_page_config(page_title="📊 勝率変動ランキング", layout="centered")

st.title("📊 テキサスホールデム 勝率変動ランキング")

st.markdown("""
このアプリでは、各ハンドに対して **どのようなフロップ・ターン・リバーの特徴** が
勝率にどう影響するかを表示します。勝率が大きく上昇・下降した要因の特徴量も横に表示されます。
""")

# --- サイドバー UI ---
st.sidebar.header("設定")
group_name = st.sidebar.selectbox("🎯 対象ハンドグループを選択", get_all_group_names())
num_simulations = st.sidebar.selectbox("シミュレーション回数", [10000, 30000, 50000], index=0)
range_option = st.sidebar.radio("相手ハンドレンジ", ["すべて", "25%", "30%"], index=0)
range_mode = {"すべて": "all", "25%": "25", "30%": "30"}[range_option]
six_player_mode = st.sidebar.checkbox("6人テーブル対応（他4人を除外）", value=True)

# --- 計算ボタン ---
if st.button("✅ 勝率変動を計算"):
    st.write(f"計算中... グループ: `{group_name}`, レンジ: `{range_option}`, 回数: `{num_simulations}`")
    df_result, df_feature = run_group_calculation(
        group_name=group_name,
        num_simulations=num_simulations,
        range_mode=range_mode,
        six_player_mode=six_player_mode,
        return_feature_analysis=True
    )
    st.success("✅ 計算完了！")

    # --- 勝率変動ランキング表示 ---
    def show_shift_ranking(stage):
        st.markdown(f"### 💡 {stage} 勝率変動ランキング")
        if "Feature" in df_result.columns:
            merged = df_result
        elif "Feature" in df_feature.columns:
            merged = df_result.merge(df_feature[["Hand", "Feature"]], on="Hand", how="left")
        else:
            merged = df_result.copy()
            merged["Feature"] = "N/A"

        top10 = merged.sort_values(by=f"Shift{stage}", ascending=False).head(10)
        bottom10 = merged.sort_values(by=f"Shift{stage}", ascending=True).head(10)

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

# --- プリフロップ勝率表 ---
st.markdown("### 🎯 代表的なハンドのプリフロップ勝率（vs ランダム）")
preflop_df = pd.DataFrame(get_static_preflop_winrates().items(), columns=["Hand", "Winrate"])
preflop_df = preflop_df.sort_values(by="Winrate", ascending=False).reset_index(drop=True)
st.dataframe(preflop_df)
