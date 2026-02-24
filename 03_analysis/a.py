import pandas as pd
import statsmodels.api as sm
import matplotlib.pyplot as plt
import seaborn as sns
from sqlalchemy import create_engine
import os
from dotenv import load_dotenv
load_dotenv()

# Database Connection
DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)

def run_multiple_regression_viz():
    print("📈 Starting Visualization: Multiple Regression Analysis")
    
    # 1. Data Preparation
    df = pd.read_sql("SELECT * FROM properties_integration_lab", engine)
    df['total_price'] = df['price'] + df['admin_num']
    df['unit_price'] = df['total_price'] / df['menseki']
    
    # Filter out invalid records
    analysis_df = df[(df['unit_price'] > 0) & (df['menseki'] > 0) & (df['building_floor'] > 0)].copy()
    
    Y = analysis_df['unit_price']
    X = analysis_df[['age', 'room_floor', 'building_floor']]
    X_with_const = sm.add_constant(X)

    # 2. Model Fitting
    model = sm.OLS(Y, X_with_const)
    results = model.fit()

    # 3. Visualization
    fig = plt.figure(figsize=(15, 6))

    # --- Plot 1: Observed vs Predicted ---
    plt.subplot(1, 2, 1)
    predicted = results.predict(X_with_const)
    plt.scatter(predicted, Y, alpha=0.5, color='royalblue')
    
    # Ideal line (y=x)
    max_val = max(max(predicted), max(Y))
    min_val = min(min(predicted), min(Y))
    plt.plot([min_val, max_val], [min_val, max_val], color='darkorange', linestyle='--', linewidth=2)
    
    plt.xlabel('Predicted Unit Price (JPY/m2)')
    plt.ylabel('Observed Unit Price (JPY/m2)')
    plt.title(f'Observed vs Predicted (R-squared: {results.rsquared:.3f})')
    plt.grid(True, alpha=0.3)

    # --- Plot 2: Coefficients (Effect Size) ---
    plt.subplot(1, 2, 2)
    
    # Extract coefficients and confidence intervals (excluding constant)
    coef_df = results.params.drop('const').sort_values()
    conf_int = results.conf_int().drop('const')
    errors = conf_int[1] - results.params.drop('const')

    # Horizontal bar plot
    coef_df.plot(kind='barh', xerr=errors, color='seagreen', alpha=0.8)
    plt.axvline(0, color='black', linestyle='-', linewidth=1)
    plt.xlabel('Coefficient Value (Impact on Unit Price)')
    plt.title('Feature Importance (Regression Coefficients)')
    plt.grid(axis='x', linestyle='--', alpha=0.7)

    plt.tight_layout()
    plt.savefig('multiple_regression_analysis.png')
    print("✅ Visualization saved as 'multiple_regression_analysis.png'")
    plt.show()
if __name__ == "__main__":
    run_multiple_regression_viz()