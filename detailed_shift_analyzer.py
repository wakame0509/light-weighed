import pandas as pd

def load_shift_data_from_csv(filepath="detailed_shift_data.csv"):
    """
    各ハンドに対するフロップ・ターン・リバーでの勝率シフトと特徴量をCSVから読み込む。

    必須列: 
    - Hand: ハンド名（例: 'AKs'）
    - ShiftFlop: フロップ後の勝率変動
    - ShiftTurn: ターン後の勝率変動
    - ShiftRiver: リバー後の勝率変動
    - Feature: 代表的な特徴量（例: 'OvercardOnFlop', 'PairedFlop' など）

    パスは必要に応じて変更してください。
    """
    try:
        df = pd.read_csv(filepath)
        required_cols = {"Hand", "ShiftFlop", "ShiftTurn", "ShiftRiver", "Feature"}

        missing_cols = required_cols - set(df.columns)
        if missing_cols:
            raise ValueError(f"必要な列が不足しています: {missing_cols}")

        return df

    except FileNotFoundError:
        raise FileNotFoundError(f"ファイルが見つかりません: {filepath}")

    except pd.errors.ParserError:
        raise RuntimeError(f"CSVファイルの形式に問題があります: {filepath}")

    except Exception as e:
        raise RuntimeError(f"データ読み込み中にエラーが発生しました: {e}")
