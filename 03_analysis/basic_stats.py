import pandas as pd
from sqlalchemy import create_engine
import matplotlib.pyplot as plt
import os
from dotenv import load_dotenv
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)

def run_analysis():
    print("統計分析フェーズ")

    df = pd.read_sql("SELECT * FROM properties_integration_lab",engine)
    
    if df.empty:
        print("データがありません")
        return
    
    df['total_price'] = df['price']+df['admin_num']
    # 平米単価
    df['unit_price'] = df['total_price']/df['menseki']

    stats={
        "平均家賃":df['total_price'].mean(),
        "中央値家賃":df['total_price'].median(),
        "平均平米単価":df['unit_price'].mean(),
        "物件数":len(df)
    }

    print("\n--- 新宿区 物件統計レポート ---")
    print(f"サンプルサイズ: {stats['物件数']} 件")
    print(f"実質平均家賃: {stats['平均家賃']:,.0f} 円")
    print(f"家賃中央値: {stats['中央値家賃']:,.0f} 円")
    print(f"平均平米単価: {stats['平均平米単価']:,.0f} 円/m2")
    print("-" * 30)

    correlation = df['age'].corr(df['total_price'])
    print(f"築年数と家賃の相関係数(r)：{correlation:.2f}")

    plt.scatter(df['age'],df['total_price'])
    plt.xlabel('Age(years)')
    plt.ylabel('Total Price (yen)')
    plt.title(f"Age vs Total Price (r={correlation:.2f})")
    plt.show()

if __name__ == "__main__":
    run_analysis()
    