import yfinance as yf

ticker_code = "7203.T"
toyota = yf.Ticker(ticker_code)
df_toyota = toyota.history(start="2024-01-01", end="2024-06-30")
print(df_toyota.head())
print("Hello, yfinance!")
