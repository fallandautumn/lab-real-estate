import pandas as pd
from sqlalchemy import create_engine
import os
from dotenv import load_dotenv
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)

def run_grouping_analysis():
    print("🏢 マンション単位での集計分析を開始します...")
    
    # 1. データの読み込み
    df = pd.read_sql("SELECT * FROM properties_integration_lab", engine)
    
    # 実質家賃と平米単価の計算
    df['total_price'] = df['price'] + df['admin_num']
    df['unit_price'] = df['total_price'] / df['menseki']

    # 2. groupby でマンション名ごとに集計
    # - count: そのマンションから何部屋出ているか
    # - mean: 平均平米単価
    # - min/max: 最安・最高価格の幅
    grouping_summary = df.groupby('title').agg({
        'unit_price':['mean','count'],
        'total_price':['mean','min','max'],
        'age':'first',
        'address':'first'

    })

    # カラム名をわかりやすく整理
    grouping_summary.columns = [
        '平均平米単価', '部屋数', '平均家賃', '最安家賃', '最高家賃', '築年数', '住所'
    ]

    # 3. 平均平米単価が安い順（お買い得順）にソート
    grouping_summary = grouping_summary.sort_values(by='平均平米単価', ascending=True)

    print("\n--- マンション別 集計レポート（平米単価が安い順） ---")
    pd.set_option('display.max_columns',None)
    pd.set_option('display.width',1000)
    pd.set_option('display.unicode.east_asian_width',True)
    grouping_summary.index = grouping_summary.index.str[:15]
    formatted_summary =grouping_summary.copy()
    formatted_summary['平均平米単価'] = formatted_summary['平均平米単価'].map('{:,.0f}円'.format)
    formatted_summary['平均家賃'] = formatted_summary['平均家賃'].map('{:,.0f}円'.format)

    print(grouping_summary.head(10)) # 上位10件を表示

    correlation = grouping_summary['築年数'].corr(grouping_summary['平均平米単価'])
    print(f"マンション単位での相関係数(r)：{correlation:.2f}")

    overall_unit_price_mean = grouping_summary['平均平米単価'].mean()
    overall_unit_price_median = grouping_summary['平均平米単価'].median()

    print(f"新宿全体での平均平米単価:{overall_unit_price_mean:,.0f}円/m2")
    print(f"新宿全体の平米単価中央値:{overall_unit_price_median:,.0f}円/m2")
    
    return grouping_summary

if __name__ == "__main__":
    summary = run_grouping_analysis()