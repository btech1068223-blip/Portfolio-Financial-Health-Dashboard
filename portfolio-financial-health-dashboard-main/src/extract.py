import os
import json
import time
import argparse
import yfinance as yf

TICKERS = ["MSFT", "CRM", "ADBE", "NOW", "WDAY", "DDOG", "NET", "HUBS", "TEAM", "OKTA"]
RAW_DIR = os.path.join("data", "raw")

def df_to_dict(df):
    if df is None or df.empty:
        return {}
    try:
        return json.loads(df.to_json(date_format="iso"))
    except Exception as e:
        print(f"Warning: Failed to convert DataFrame to dict: {e}")
        return {}

def extract_ticker_data(ticker_symbol):
    print(f"Fetching data for {ticker_symbol}...")
    ticker = yf.Ticker(ticker_symbol)
    
    # Fetch quarterly statements
    print(f"  Retrieving quarterly statements...")
    q_income = ticker.quarterly_income_stmt
    q_balance = ticker.quarterly_balance_sheet
    q_cashflow = ticker.quarterly_cashflow
    
    # Fetch annual statements
    print(f"  Retrieving annual statements...")
    a_income = ticker.income_stmt
    a_balance = ticker.balance_sheet
    a_cashflow = ticker.cashflow
    
    data = {
        "ticker": ticker_symbol,
        "extracted_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "quarterly": {
            "income_statement": df_to_dict(q_income),
            "balance_sheet": df_to_dict(q_balance),
            "cash_flow": df_to_dict(q_cashflow)
        },
        "annual": {
            "income_statement": df_to_dict(a_income),
            "balance_sheet": df_to_dict(a_balance),
            "cash_flow": df_to_dict(a_cashflow)
        }
    }
    return data

def main():
    parser = argparse.ArgumentParser(description="Extract raw financial data from Yahoo Finance.")
    parser.add_argument("--force", action="store_true", help="Bypass cache and force new download.")
    args = parser.parse_args()

    os.makedirs(RAW_DIR, exist_ok=True)
    
    for idx, ticker in enumerate(TICKERS):
        file_path = os.path.join(RAW_DIR, f"{ticker}.json")
        
        if os.path.exists(file_path) and not args.force:
            print(f"[{idx+1}/{len(TICKERS)}] {ticker} data found in cache. Skipping download.")
            continue
            
        try:
            data = extract_ticker_data(ticker)
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2)
            print(f"[{idx+1}/{len(TICKERS)}] Successfully saved {ticker} to {file_path}")
        except Exception as e:
            print(f"[{idx+1}/{len(TICKERS)}] Error fetching data for {ticker}: {e}")
            
        # Throttling delay to prevent rate limiting
        if idx < len(TICKERS) - 1:
            time.sleep(1.5)

    print("Extraction phase complete.")

if __name__ == "__main__":
    main()
