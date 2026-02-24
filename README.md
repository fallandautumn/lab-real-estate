# Real Estate Arbitrage Lab: Statistical Property Valuation
## 統計的アプローチによる不動産適正価格の算出と市場の歪みの検知

本リポジトリは、統計検定2級で習得した知識を実務に応用し、東京都内の不動産市場における「理論価格」と「市場価格」の乖離を定量的に分析するための実験場（Lab）です。

## 1. プロジェクト概要 (Overview)
不動産市場における「情報の非対称性」が生む割安な物件（アービトラージ機会）を、主観を排除した統計モデルによって抽出します。
スクレイピングからデータベース構築、重回帰分析による残差分析までを一貫して実装しています。

## 2. データパイプライン (Data Pipeline)
実装されたコードは、以下の3フェーズで動作します 。

### A. Data Collection (Scraping)
- `requests` と `BeautifulSoup4` を用い、不動産ポータルサイト（SUUMO等）から最新の物件情報を動的に取得します。
- 正規表現（`re`）を用いたデータクレンジングにより、築年数や面積、所在階などの定性・定型データを数値化します。

### B. Data Persistence (DB)
- `SQLAlchemy` を ORM として採用。
- `PostgreSQL`（Docker環境）上に構築された `properties_integration_lab` テーブルに、収集したデータを正規化して保存します。

### C. Statistical Analysis (OLS)
- `statsmodels` を用いた最小二乗法（OLS）により、以下の回帰モデルを構築します。

$$Unit\_Price = \beta_0 + \beta_1 \cdot Age + \beta_2 \cdot Room\_Floor + \beta_3 \cdot Building\_Floor + \epsilon$$

- **目的変数**: 平米単価 ($Unit\_Price$)
- **説明変数**: 築年数 ($Age$), 所在階 ($Room\_Floor$), 建物の総階数 ($Building\_Floor$)
- **残差 ($\epsilon$) 分析**: 理論価格を下回る物件（残差が負に大きい物件）を「統計的なお買い得物件」として抽出します。

## 3. 技術スタック (Tech Stack)
- **Language**: Python 3.13 
- **Analysis**: `pandas`, `statsmodels`
- **Database**: `PostgreSQL 15`, `SQLAlchemy`
- **Infrastructure**: `Docker`, `Docker Compose`
- **Environment Management**: `python-dotenv` (Security-first approach)

## 4. 今後の展望 (Roadmap)
現在はプロトタイプ段階であり、以下の精度向上を計画しています。
- **特徴量モデルの精密化**: 
    ・駅徒歩分数や建物構造(RC/木造)、物件種別（マンション/アパート/その他）をカテゴリ変数として導入。
    ・多重共線性のチェックを行い、より信頼性の高い回帰係数の算出を目指す。
    ・決定係数 ($R^2$) の向上とともに、残差の分布（不均一分散性）の検証を実施。
- **アーキテクチャの進化**: FastAPI を導入し、分析結果をフロントエンドから即座に参照できる API エンドポイントの構築。
