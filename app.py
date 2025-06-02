import streamlit as st
import pandas as pd
from group_calculator import run_group_calculation
from utils import get_all_group_names, get_static_preflop_winrates

st.set_page_config(page_title="勝率変動分析アプリ", layout="wide")

st.title("♠ テキサスホールデム 勝率変動分析ツール")

# --- 設定項目 ---
st.sidebar.header("⚙️ 計算設定")
group_name = st.sidebar.selectbox("ハンドグループを選択", get_all_group_names())
num_simulations = st.sidebar.selectbox("シミュレーション回数", [1000, 5000, 10000], index=2)
range_mode = st.sidebar.radio("レンジ選択", ["all", "25", "30"], horizontal=True)
six_player_mode = st.sidebar.checkbox("6人テーブル対応", value=True)

# --- 計算ボタン ---
if st.button("✅ 勝率変動を計算"):
    with st.spinner("計算中..."):
        df_result, df_feature = run_group_calculation(
            group_name=group_name,
            num_simulations=num_simulations,
            range_mode=range_mode,
            six_player_mode=six_player_mode,
            return_feature_analysis=True
        )
        st.success("✅ 勝率変動データの計算完了")

        # --- 結果表示 ---
        st.subheader("📊 勝率変動結果")
        st.dataframe(df_result)

        # --- 特徴量集計表示 ---
        st.subheader("🧠 特徴量別 勝率変動分析")
        st.dataframe(df_feature)

        # --- 勝率変動ランキング（その場で表示） ---
        def show_shift_ranking(stage):
            st.markdown(f"### 💡 {stage} 勝率変動ランキング")
            top10 = df_result.sort_values(by=f"Shift{stage}", ascending=False).head(10)
            bottom10 = df_result.sort_values(by=f"Shift{stage}", ascending=True).head(10)

            col1, col2 = st.columns(2)
            with col1:
                st.markdown("#### 🔼 上昇幅 Top10")
                st.dataframe(top10[["Hand", f"Shift{stage}", "Feature"]].reset_index(drop=True))
            with col2:
                st.markdown("#### 🔽 下降幅 Top10")
                st.dataframe(bottom10[["Hand", f"Shift{stage}", "Feature"]].reset_index(drop=True))

        st.subheader("💡 Flop 勝率変動ランキング")
        show_shift_ranking("Flop")

        st.subheader("💡 Turn 勝率変動ランキング")
        show_shift_ranking("Turn")

        st.subheader("💡 River 勝率変動ランキング")
        show_shift_ranking("River")

        # --- CSV保存 ---
        st.download_button("📥 結果CSVをダウンロード", data=df_result.to_csv(index=False), file_name="result.csv", mime="text/csv")
        st.download_button("📥 特徴量集計CSVをダウンロード", data=df_feature.to_csv(index=False), file_name="features.csv", mime="text/csv")

# --- プリフロップ勝率（代表表） ---
st.markdown("### 🎯 代表的なハンドのプリフロップ勝率（vs ランダム）")
preflop_df = pd.DataFrame(get_static_preflop_winrates().items(), columns=["Hand", "Winrate (%)"])
preflop_df = preflop_df.sort_values(by="Winrate (%)", ascending=False).reset_index(drop=True)
st.dataframe(preflop_df)
