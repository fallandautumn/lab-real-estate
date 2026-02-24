import pandas as pd
import statsmodels.api as sm
from sqlalchemy import create_engine
import sys
import os
from dotenv import load_dotenv
load_dotenv()


def run_multiple_regression():
    # --- 1. データベース接続設定 ---
    DATABASE_URL = os.getenv("DATABASE_URL")
    engine = create_engine(DATABASE_URL)
    print("重回帰分析フェーズ：多角的な価値算出モデルの構築")
    
    # --- 2. データの読み込み ---
    try:
        df = pd.read_sql("SELECT * FROM properties_integration_lab", engine)
    except Exception as e:
        print(f"DB接続エラー: {e}")
        return

    if df.empty:
        print("データが空です。先にスクレイピングとDB保存を実行してください。")
        return

    # --- 3. 分析用データの作成（前処理） ---
    # 実質家賃（家賃＋管理費）を算出
    df['total_price'] = df['price'] + df['admin_num']
    # 目的変数：平米単価 (円/m2)
    df['unit_price'] = df['total_price'] / df['menseki']

    # 統計的に意味のないデータや異常値を除外（面積0などは計算不可のため）
    analysis_df = df[
        (df['unit_price'] > 0) & 
        (df['menseki'] > 0) & 
        (df['building_floor'] > 0)
    ].copy()

    # --- 4. モデルの構築 ---
    # 目的変数 Y: 平米単価
    # 説明変数 X: 築年数, 所在階, 建物の総階数
    Y = analysis_df['unit_price']
    X = analysis_df[['age', 'room_floor', 'building_floor']]
    
    # 統計検定の基本：定数項（切片）を明示的に追加
    X_with_const = sm.add_constant(X)

    # OLS (最小二乗法) によるモデル適合
    model = sm.OLS(Y, X_with_const)
    results = model.fit()
    
    # --- 5. 結果の出力（統計レポート） ---
    print("\n" + "="*80)
    print("重回帰分析 詳細レポート (OLS Regression Results)")
    print("="*80)
    print(results.summary())
    
    # --- 6. 応用：残差分析による「割安物件」の特定 ---
    # モデルによる「理論上の適正平米単価」を算出
    analysis_df['predicted_unit_price'] = results.predict(X_with_const)
    
    # 残差（実際の価格 - 理論価格）
    # これがマイナスに大きいほど、統計的な理論値より安い「お買い得」物件
    analysis_df['residual'] = analysis_df['unit_price'] - analysis_df['predicted_unit_price']

    print("\n" + "-"*30)
    print("統計的「お買い得」物件 TOP 5 (理論値より安い物件)")
    print("-" * 30)
    
    # 残差が小さい（マイナスに大きい）順にソート
    bargain_list = analysis_df.sort_values(by='residual').head(5)
    
    # 見やすいように表示項目を絞る
    output_cols = ['title', 'unit_price', 'predicted_unit_price', 'residual', 'age']
    print(bargain_list[output_cols])
    return results

if __name__ == "__main__":
    run_multiple_regression()