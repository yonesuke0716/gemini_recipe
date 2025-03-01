import os
import yfinance as yf
import duckdb
import pandas as pd
from datetime import datetime

from langchain_experimental.agents.agent_toolkits import create_pandas_dataframe_agent
from langchain_google_genai import GoogleGenerativeAI


api_key = os.environ["GOOGLE_API_KEY"]


# 日本株データの取得
def fetch_japanese_stocks():
    # TOPIX500をサンプルとして使用
    tickers = duckdb.read_csv(
        "https://raw.githubusercontent.com/datasets/japanese-stocks/main/data/stocks.csv"
    ).to_df()
    return tickers["Ticker"].tolist()


# 銘柄データを取得
def fetch_stock_data(ticker):
    try:
        stock = yf.Ticker(f"{ticker}.T")  # 日本株は`.T`が必要
        hist = stock.history(period="1y")
        if hist.empty:
            return None
        return {
            "Ticker": ticker,
            "Latest Price": hist["Close"].iloc[-1],
            "1M Change (%)": (
                (
                    (hist["Close"].iloc[-1] - hist["Close"].iloc[-22])
                    / hist["Close"].iloc[-22]
                )
                * 100
                if len(hist) >= 22
                else None
            ),
            "Volume": hist["Volume"].mean(),
        }
    except Exception as e:
        print(f"Error fetching data for {ticker}: {e}")
        return None


# LLMで評価
def evaluate_stock(stock_data):
    prompt = (
        f"Analyze the following stock data:\n"
        f"Ticker: {stock_data['Ticker']}\n"
        f"Latest Price: {stock_data['Latest Price']:.2f}\n"
        f"1 Month Change: {stock_data['1M Change (%)']:.2f}%\n"
        f"Average Volume: {stock_data['Volume']:.0f}\n"
        "Provide a score between 1-10 and justify your evaluation."
    )
    try:
        llm = GoogleGenerativeAI(
            model="gemini-1.5-flash", temperature=0, api_key=api_key
        )
        agent = create_pandas_dataframe_agent(
            llm,
            df,
            verbose=True,
            allow_dangerous_code=True,
        )
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a financial expert."},
                {"role": "user", "content": prompt},
            ],
            max_tokens=200,
        )
        return response["choices"][0]["message"]["content"]
    except Exception as e:
        return f"Error evaluating stock: {str(e)}"


# おすすめ銘柄を選定
def recommend_top_stocks(stock_list):
    evaluated_stocks = []
    for stock in stock_list:
        stock_data = fetch_stock_data(stock)
        if stock_data:
            analysis = evaluate_stock(stock_data)
            evaluated_stocks.append({"Ticker": stock, "Analysis": analysis})
    # ランキング形式（評価スコアや条件で並び替え可能）
    return evaluated_stocks[:3]  # 上位3銘柄を選定


# メイン処理
def main():
    print("Fetching Japanese stock data...")
    tickers = fetch_japanese_stocks()
    print(f"Total stocks to analyze: {len(tickers)}")

    print("Evaluating stocks...")
    top_stocks = recommend_top_stocks(tickers)

    # 結果表示
    print("\nRecommended Top 3 Stocks:")
    for stock in top_stocks:
        print(f"\nTicker: {stock['Ticker']}\nAnalysis:\n{stock['Analysis']}")

    # 結果をCSVに保存
    df = pd.DataFrame(top_stocks)
    df.to_csv(f"top_stocks_{datetime.now().strftime('%Y%m%d')}.csv", index=False)
    print("\nAnalysis saved to CSV!")


if __name__ == "__main__":
    main()
