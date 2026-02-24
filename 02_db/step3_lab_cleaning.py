import pandas as pd
from sqlalchemy import create_engine
import re
import os
from dotenv import load_dotenv
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)

def run_cleaning_lab():
    print("実験開始")
    df = pd.read_sql("SELECT * FROM properties_integration_lab",engine)
    print("生データの確認")
    print(df.head())

    if df.empty:
        print("データが空です。")
        return
    
    print(f"{len(df)}件のデータを読み込みました、加工を開始します。")

    def clean_price(price_str):
        match = re.search(r'(\d+\.?\d*)', str(price_str))
        if match:
            val = float(match.group(1))
            if '万円' in price_str:
                return val*10000
            return val
        return 0.0
    
    df['price_num'] = df['price'].apply(clean_price)

    mean_price = df['price_num'].mean()
    std_price = df['price_num'].std()

    print("\n統計分析結果")
    print("-"*30)
    print(f"平均家賃($\bar{{x}}$): {mean_price:,.0f} 円")
    print(f"標準偏差($s$):{std_price:,.0f} 円")
    print("-"*30)

    print(df[['title','price','price_num']].head())

if __name__ == '__main__':
    run_cleaning_lab()



