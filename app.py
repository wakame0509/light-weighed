import streamlit as st
import pandas as pd
from detailed_shift_analyzer import run_detailed_shift_analysis
from utils import get_static_preflop_winrates

st.title("📊 テキサスホールデム 勝率変動ランキング")

st.markdown("""
このアプリでは、各ハンドに対して **どのようなフロップ・ターン・リバーの特徴** が
勝率にどう影響するかを表示します。勝率が大きく上昇・下降した要因の特徴量も横に表示されます。
""")

# ボタン押下で分析実行
if st.button("🔍 勝率変動を計算（代表フロップ100通り×各ハンド）"):
    with st.spinner("計算中です。数分お待ちください..."):
        df = run_detailed_shift_analysis(num_flops=100, num_simulations=10000)
        st.success("✅ 計算完了！")

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

        show_shift_ranking("Flop")
        show_shift_ranking("Turn")
        show_shift_ranking("River")

        st.markdown("### 🎯 代表的なハンドのプリフロップ勝率（vs ランダム）")
        preflop_df = pd.DataFrame(get_static_preflop_winrates().items(), columns=["Hand", "Winrate"])
        preflop_df = preflop_df.sort_values(by="Winrate", ascending=False).reset_index(drop=True)
        st.dataframe(preflop_df)
else:
    st.info("上のボタンを押すと、代表フロップ×全ハンドで勝率変動と特徴量を分析します。")
