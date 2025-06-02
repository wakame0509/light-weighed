# --- 勝率変動ランキング表示セクション ---
st.markdown("### 🏆 勝率変動ランキング（フロップ・ターン・リバー）")

try:
    df = pd.read_csv("results/detailed_shifts.csv")
except FileNotFoundError:
    st.warning("⚠️ 分析結果ファイル（results/detailed_shifts.csv）が見つかりません。")
    df = pd.DataFrame()

if not df.empty:
    # --- フロップ ---
    st.markdown("#### 📈 フロップ勝率上昇トップ10")
    top_flop_increase = df.sort_values(by="ShiftFlop", ascending=False).head(10)
    st.dataframe(top_flop_increase[["Hand", "ShiftFlop", "Feature"]])

    st.markdown("#### 📉 フロップ勝率下降トップ10")
    top_flop_decrease = df.sort_values(by="ShiftFlop", ascending=True).head(10)
    st.dataframe(top_flop_decrease[["Hand", "ShiftFlop", "Feature"]])

    # --- ターン ---
    st.markdown("#### 📈 ターン勝率上昇トップ10")
    top_turn_increase = df.sort_values(by="ShiftTurn", ascending=False).head(10)
    st.dataframe(top_turn_increase[["Hand", "ShiftTurn", "Feature"]])

    st.markdown("#### 📉 ターン勝率下降トップ10")
    top_turn_decrease = df.sort_values(by="ShiftTurn", ascending=True).head(10)
    st.dataframe(top_turn_decrease[["Hand", "ShiftTurn", "Feature"]])

    # --- リバー ---
    st.markdown("#### 📈 リバー勝率上昇トップ10")
    top_river_increase = df.sort_values(by="ShiftRiver", ascending=False).head(10)
    st.dataframe(top_river_increase[["Hand", "ShiftRiver", "Feature"]])

    st.markdown("#### 📉 リバー勝率下降トップ10")
    top_river_decrease = df.sort_values(by="ShiftRiver", ascending=True).head(10)
    st.dataframe(top_river_decrease[["Hand", "ShiftRiver", "Feature"]])
else:
    st.info("結果データがまだ生成されていないか、ファイルが読み込まれていません。")
