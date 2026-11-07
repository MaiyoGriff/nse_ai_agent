
import yfinance as yf
import pandas as pd

ticker = "SCOM.NR"

# Fetch stock information
stock = yf.Ticker(ticker)
info = stock.info

# Extract company details
data = {
    "ticker": ticker,
    "query": ticker,
    "symbol": info.get("symbol", ticker),
    "name": info.get("longName") or info.get("shortName", ""),
    "exchange": info.get("exchange", "")
}

# Save to CSV
df = pd.DataFrame([data])

df.to_csv("nse_tickers.csv", index=False)

print(df)
print("Saved to nse_tickers.csv")
