
import requests
import pandas as pd
from io import StringIO

URL = "https://stockanalysis.com/list/nairobi-stock-exchange/"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/120 Safari/537.36"
}

def scrape_nse():

    print("[+] Connecting to NSE listings source...")

    response = requests.get(
        URL,
        headers=HEADERS,
        timeout=30
    )

    response.raise_for_status()

    print("[+] Downloading listings page...")

    tables = pd.read_html(StringIO(response.text))

    records = []

    for table in tables:

        # Locate the company listings table
        table.columns = [
            str(col).strip() for col in table.columns
        ]

        if "Symbol" not in table.columns:
            continue

        if "Company Name" not in table.columns:
            continue

        for _, row in table.iterrows():

            symbol = str(row["Symbol"]).strip()
            name = str(row["Company Name"]).strip()

            if not symbol or symbol.lower() == "nan":
                continue

            if not name or name.lower() == "nan":
                continue

            records.append({
                "ticker": symbol,
                "query": symbol,
                "symbol": symbol,
                "name": name,
                "exchange": "Nairobi Securities Exchange"
            })

    if not records:
        print("[-] No listings found.")
        return

    # Remove duplicate symbols
    df = pd.DataFrame(records)
    df.drop_duplicates(subset=["symbol"], inplace=True)

    # Save CSV
    df.to_csv("nse_tickers.csv", index=False)

    print("\n[+] SCRAPING COMPLETE")
    print(f"[+] Stocks found: {len(df)}")
    print("[+] Saved to nse_tickers.csv")

    print("\n", df.to_string(index=False))


if __name__ == "__main__":
    scrape_nse()
