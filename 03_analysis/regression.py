import pandas as pd
import matplotlib.pyplot as plt
from sqlalchemy import create_engine
from scipy import stats
import os
from dotenv import load_dotenv
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)

def regression_analysis():
    print("単回帰分析フェーズ:築年数vs平米単価")

    df = pd.read_sql("SELECT * FROM properties_integration_lab",engine)
    df['total_price'] = df['price']+df['admin_num']
    df['unit_price'] = df['total_price']/df['menseki']

    summary = df.groupby('title').agg({
        'unit_price':'mean',
        'age':'first'
    }).dropna()

    x = summary['age']
    y = summary['unit_price']

    slope,intercept,r_value,p_value,std_err = stats.linregress(x,y)

    r_squared = r_value**2

    print(f"回帰分析結果")
    print(f"回帰直線の式: y={slope:.2f}x + {intercept:.2f}")
    print(f"決定係数:{r_squared:.3f}")
    print(f"P値:{p_value:.5f}({'統計的に有意' if p_value < 0.05 else '有意ではない'})")

    plt.figure(figsize=(10,6))
    plt.scatter(x,y,alpha=0.5,label='aparts')

    regression_line = slope * x + intercept
    plt.plot(x, regression_line, color='red',linewidth=2,label=f'regression line({r_squared:.2f})')

    plt.xlabel('age')
    plt.ylabel('(yen/m2)')
    plt.title('Shinjuku:age and (yen/m2)')
    plt.legend()
    plt.grid(True,linestyle ='--',alpha=0.7)

    plt.savefig('regression_analysis.png')
    print("グラフ'regression_analysis.pngとして保存しました。")
    plt.show()
    
    return summary,slope,intercept


if __name__ == "__main__":
    summary,a,b = regression_analysis()