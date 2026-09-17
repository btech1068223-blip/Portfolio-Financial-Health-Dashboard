import os
import sqlite3
import pandas as pd

DB_PATH = os.path.join("data", "financial_health.db")
SCHEMA_PATH = os.path.join("sql", "schema.sql")
CSV_PATH = os.path.join("data", "processed", "clean_financials.csv")

COMPANY_NAMES = {
    "MSFT": "Microsoft Corporation",
    "CRM": "Salesforce, Inc.",
    "ADBE": "Adobe Inc.",
    "NOW": "ServiceNow, Inc.",
    "WDAY": "Workday, Inc.",
    "DDOG": "Datadog, Inc.",
    "NET": "Cloudflare, Inc.",
    "HUBS": "HubSpot, Inc.",
    "TEAM": "Atlassian Corporation",
    "OKTA": "Okta, Inc."
}

def init_db(conn):
    print("Initializing database schema...")
    with open(SCHEMA_PATH, "r", encoding="utf-8") as f:
        schema_sql = f.read()
    conn.executescript(schema_sql)
    print("Schema initialized successfully.")

def populate_companies(conn, tickers):
    print("Populating companies dimension...")
    cursor = conn.cursor()
    for ticker in tickers:
        name = COMPANY_NAMES.get(ticker, f"{ticker} Inc.")
        cursor.execute(
            "INSERT OR IGNORE INTO companies (ticker, company_name) VALUES (?, ?)",
            (ticker, name)
        )
    conn.commit()
    
    # Retrieve mapping
    cursor.execute("SELECT ticker, company_id FROM companies")
    return dict(cursor.fetchall())

def load_financials(conn, df, company_map):
    print("Loading financials fact table...")
    cursor = conn.cursor()
    
    records = []
    for _, row in df.iterrows():
        ticker = row["ticker"]
        company_id = company_map.get(ticker)
        if company_id is None:
            print(f"Warning: Ticker {ticker} not found in companies table. Skipping record.")
            continue
            
        records.append((
            company_id,
            row["period_type"],
            row["date"],
            row["metric"],
            row["value"]
        ))
        
    # Batch insert/replace
    cursor.executemany(
        """
        INSERT OR REPLACE INTO financials (company_id, period_type, date, metric, value)
        VALUES (?, ?, ?, ?, ?)
        """,
        records
    )
    conn.commit()
    print(f"Successfully loaded {len(records)} financial records.")

def main():
    if not os.path.exists(CSV_PATH):
        print(f"Error: Processed data CSV not found at {CSV_PATH}. Run transform.py first.")
        return
        
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    
    df = pd.read_csv(CSV_PATH)
    unique_tickers = df["ticker"].unique()
    
    conn = sqlite3.connect(DB_PATH)
    
    try:
        # Enable foreign keys
        conn.execute("PRAGMA foreign_keys = ON;")
        
        # Initialize schema
        init_db(conn)
        
        # Populate companies
        company_map = populate_companies(conn, unique_tickers)
        
        # Load facts
        load_financials(conn, df, company_map)
        
        print("Database loading complete.")
    except Exception as e:
        print(f"Error loading database: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    main()
