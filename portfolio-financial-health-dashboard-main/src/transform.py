import os
import json
import pandas as pd
import numpy as np

RAW_DIR = os.path.join("data", "raw")
PROCESSED_DIR = os.path.join("data", "processed")

TICKERS = ["MSFT", "CRM", "ADBE", "NOW", "WDAY", "DDOG", "NET", "HUBS", "TEAM", "OKTA"]

def get_metric_value(statement_dict, date_key, keys):
    """Retrieve value from statement dictionary for given date using fallback keys."""
    date_data = statement_dict.get(date_key, {})
    for key in keys:
        if key in date_data and date_data[key] is not None:
            return date_data[key]
    return None

def align_date_to_calendar(date_str, period_type):
    """Align date string to the closest calendar quarter-end or year-end date."""
    dt = pd.to_datetime(date_str)
    year = dt.year
    
    if period_type == "annual":
        candidates = [
            pd.Timestamp(f"{year-1}-12-31"),
            pd.Timestamp(f"{year}-12-31"),
            pd.Timestamp(f"{year+1}-12-31")
        ]
    else:
        candidates = []
        for y in [year - 1, year, year + 1]:
            candidates.extend([
                pd.Timestamp(f"{y}-03-31"),
                pd.Timestamp(f"{y}-06-30"),
                pd.Timestamp(f"{y}-09-30"),
                pd.Timestamp(f"{y}-12-31")
            ])
            
    closest = min(candidates, key=lambda d: abs((d - dt).days))
    return closest.strftime("%Y-%m-%d")

def clean_ticker_data(ticker):
    file_path = os.path.join(RAW_DIR, f"{ticker}.json")
    if not os.path.exists(file_path):
        print(f"Warning: Raw file not found for {ticker}")
        return []
        
    with open(file_path, "r", encoding="utf-8") as f:
        raw_data = json.load(f)
        
    records = []
    
    # Fallback keys definition
    revenue_keys = ["Total Revenue", "Operating Revenue"]
    net_income_keys = ["Net Income", "Net Income Common Stockholders", "Net Income Continuous Operations"]
    ocf_keys = ["Operating Cash Flow", "Cash Flow From Continuing Operating Activities"]
    gp_keys = ["Gross Profit"]
    cor_keys = ["Cost Of Revenue", "Reconciled Cost Of Revenue"]
    
    for period_type in ["quarterly", "annual"]:
        period_data = raw_data.get(period_type, {})
        
        income_stmt = period_data.get("income_statement", {})
        balance_sheet = period_data.get("balance_sheet", {})
        cash_flow = period_data.get("cash_flow", {})
        
        # Get all unique date keys across all three statements
        dates = set(income_stmt.keys()) | set(balance_sheet.keys()) | set(cash_flow.keys())
        
        for date_key in dates:
            aligned_date = align_date_to_calendar(date_key, period_type)
            
            # Extract core metrics
            rev = get_metric_value(income_stmt, date_key, revenue_keys)
            ni = get_metric_value(income_stmt, date_key, net_income_keys)
            ocf = get_metric_value(cash_flow, date_key, ocf_keys)
            gp = get_metric_value(income_stmt, date_key, gp_keys)
            cor = get_metric_value(income_stmt, date_key, cor_keys)
            
            # Debt calculation: yfinance might have "Total Debt" directly, or we fall back
            total_debt = get_metric_value(balance_sheet, date_key, ["Total Debt"])
            if total_debt is None:
                lt_debt = get_metric_value(balance_sheet, date_key, ["Long Term Debt"]) or 0
                st_debt = get_metric_value(balance_sheet, date_key, ["Current Debt"]) or 0
                total_debt = lt_debt + st_debt if (lt_debt > 0 or st_debt > 0) else None
                
            # Gross margin calculation
            gm = None
            if gp is not None and rev is not None and rev > 0:
                gm = gp / rev
            elif cor is not None and rev is not None and rev > 0:
                gm = (rev - cor) / rev
                
            metrics = {
                "revenue": rev,
                "net_income": ni,
                "operating_cash_flow": ocf,
                "total_debt": total_debt,
                "gross_margin": gm
            }
            
            for metric_name, val in metrics.items():
                if val is not None:
                    records.append({
                        "ticker": ticker,
                        "period_type": period_type,
                        "date": aligned_date,
                        "metric": metric_name,
                        "value": float(val)
                    })
                    
    return records

def main():
    os.makedirs(PROCESSED_DIR, exist_ok=True)
    all_records = []
    
    for ticker in TICKERS:
        ticker_records = clean_ticker_data(ticker)
        all_records.extend(ticker_records)
        print(f"Processed {len(ticker_records)} records for {ticker}")
        
    if not all_records:
        print("Error: No records processed.")
        return
        
    df = pd.DataFrame(all_records)
    
    # Remove any duplicate records (same ticker, period_type, date, metric)
    df = df.drop_duplicates(subset=["ticker", "period_type", "date", "metric"])
    
    # Sort for cleanliness
    df = df.sort_values(by=["ticker", "period_type", "date", "metric"])
    
    output_path = os.path.join(PROCESSED_DIR, "clean_financials.csv")
    df.to_csv(output_path, index=False)
    print(f"Successfully saved {len(df)} rows to {output_path}")

if __name__ == "__main__":
    main()
