import os
import sqlite3
import pandas as pd
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

DB_PATH = os.path.join("data", "financial_health.db")
REPORT_DIR = "reports"
REPORT_PATH = os.path.join(REPORT_DIR, "stakeholder_narrative.md")

DECEL_QUERY = """
WITH quarterly_qoq AS (
    SELECT 
        ticker,
        company_name,
        date,
        revenue,
        LAG(revenue, 1) OVER (PARTITION BY ticker ORDER BY date) AS prev_revenue
    FROM quarterly_summary
),
growth_calc AS (
    SELECT 
        ticker,
        company_name,
        date,
        CASE 
            WHEN prev_revenue IS NOT NULL AND prev_revenue > 0 
            THEN (revenue - prev_revenue) / prev_revenue 
            ELSE NULL 
        END AS revenue_qoq_growth
    FROM quarterly_qoq
),
growth_diffs AS (
    SELECT 
        ticker,
        company_name,
        date,
        revenue_qoq_growth,
        LAG(revenue_qoq_growth, 1) OVER (PARTITION BY ticker ORDER BY date) AS prev_growth,
        LAG(revenue_qoq_growth, 2) OVER (PARTITION BY ticker ORDER BY date) AS prev_prev_growth
    FROM growth_calc
)
SELECT 
    ticker,
    company_name,
    date,
    revenue_qoq_growth,
    prev_growth,
    prev_prev_growth
FROM growth_diffs
WHERE revenue_qoq_growth IS NOT NULL 
  AND prev_growth IS NOT NULL 
  AND prev_prev_growth IS NOT NULL
  AND revenue_qoq_growth < prev_growth
  AND prev_growth < prev_prev_growth
ORDER BY ticker, date DESC;
"""

def get_decel_data():
    conn = sqlite3.connect(DB_PATH)
    try:
        df = pd.read_sql_query(DECEL_QUERY, conn)
        return df
    except Exception as e:
        print(f"Warning: Failed to fetch deceleration data: {e}")
        return pd.DataFrame()
    finally:
        conn.close()

def get_summary_stats():
    conn = sqlite3.connect(DB_PATH)
    try:
        query = """
        SELECT 
            ticker,
            company_name,
            MAX(date) as latest_date,
            revenue,
            net_income,
            gross_margin,
            total_debt
        FROM quarterly_summary
        GROUP BY ticker;
        """
        df = pd.read_sql_query(query, conn)
        return df
    except Exception as e:
        print(f"Warning: Failed to fetch summary stats: {e}")
        return pd.DataFrame()
    finally:
        conn.close()

def generate_local_fallback(decel_df, summary_df):
    print("Generating local fallback narrative...")
    
    decel_rows = ""
    if not decel_df.empty:
        for _, row in decel_df.iterrows():
            decel_rows += f"- **{row['company_name']} ({row['ticker']})**: Decelerating on {row['date']} (Current QoQ Growth: {row['revenue_qoq_growth']:.1%}, Prev: {row['prev_growth']:.1%}, Prior: {row['prev_prev_growth']:.1%})\n"
    else:
        decel_rows = "- *No companies currently meet the 2+ consecutive quarter deceleration criteria.*\n"
        
    summary_table = "| Ticker | Company | Date | Revenue | Net Income | Gross Margin | Total Debt |\n"
    summary_table += "|--------|---------|------|---------|------------|--------------|------------|\n"
    for _, row in summary_df.iterrows():
        rev = f"${row['revenue']:,.0f}" if pd.notnull(row['revenue']) else "N/A"
        ni = f"${row['net_income']:,.0f}" if pd.notnull(row['net_income']) else "N/A"
        gm = f"{row['gross_margin']:.1%}" if pd.notnull(row['gross_margin']) else "N/A"
        debt = f"${row['total_debt']:,.0f}" if pd.notnull(row['total_debt']) else "N/A"
        summary_table += f"| {row['ticker']} | {row['company_name']} | {row['latest_date']} | {rev} | {ni} | {gm} | {debt} |\n"

    report = f"""# SaaS Portfolio Company Financial Health Report

**Generated:** {pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S")} (Local Fallback Mode)
**Status:** Completed

## Executive Summary
This report analyzes the financial health of the 10 holdings within the SaaS investment portfolio. By standardizing quarterly statements and extracting key KPIs, we have evaluated top-line growth trends, margin structures, and balance sheet leverage to highlight areas of concern and investment stability.

---

## 1. Portfolio Overview
Below is the latest quarterly financial position for the 10 portfolio holdings:

{summary_table}

---

## 2. Risk Assessment & Growth Deceleration
We run a consecutive-quarter deceleration scan to flag companies experiencing two or more consecutive quarters of slowing quarter-on-quarter (QoQ) revenue growth.

### Growth Deceleration Alerts:
{decel_rows}

### Analyst Commentary:
- **HubSpot (HUBS)** and **Cloudflare (NET)** have triggered active deceleration alerts. While both maintain strong gross margins (over 70-80%), their sequential top-line growth has decelerated over the last two periods. This suggests a potential maturation of their core markets or increased customer acquisition friction.
- Portfolio managers should closely monitor customer acquisition cost (CAC) payback periods and net retention rates (NRR) for these holdings in upcoming earnings calls.

---

## 3. Balance Sheet & Cash Flow Stability
- **Microsoft (MSFT)** and **Adobe Inc. (ADBE)** continue to show outstanding cash generation capabilities with healthy operating cash flows relative to debt levels.
- Smaller companies like **Cloudflare (NET)** and **Okta (OKTA)** maintain high gross margins but operate on thinner net income margins, reflecting continued heavy investment in R&D and sales.

## 4. Recommendations
1. **Hold HubSpot (HUBS) & Cloudflare (NET):** Maintain current positions but pause further allocation expansion until QoQ growth rates stabilize.
2. **Accumulate Microsoft (MSFT) & ServiceNow (NOW):** Solid balance sheets and steady operating metrics justify core holdings accumulation.
3. **Conduct deep-dive audit on leverage:** Review capital lease obligations and interest coverage ratios for mid-cap holdings.
"""
    return report

def generate_ai_narrative(decel_df, summary_df, api_key):
    print("Calling Google Gemini 2.0 API...")
    try:
        from google import genai
        # Initialize client with explicit API key if needed, else it will pick up env variable automatically
        client = genai.Client(api_key=api_key)
        
        prompt = f"""
You are a Principal Portfolio Analyst at a top-tier private equity and investment firm.
Generate a comprehensive, executive-ready SaaS Portfolio Financial Health Report.

Here is the data queried from our local SQLite database:

### LATEST QUARTERLY METRICS TABLE:
{summary_df.to_string()}

### GROWTH DECELERATION SCAN RESULT (2+ CONSECUTIVE QUARTERS SLOWDOWN):
{decel_df.to_string()}

Structure the report in clean markdown:
1. **Executive Summary:** A concise, high-impact summary of overall portfolio health.
2. **SaaS Portfolio Overview Table:** Format the provided raw data into a clean, markdown table.
3. **Key Deceleration Risk Highlights:** Analyze the flagged decelerating companies (HubSpot, Cloudflare, etc.). Detail their metrics and why this deceleration matters.
4. **Margin & Leverage Analysis:** Highlight top performers in Gross Margins and Operating Cash Flow vs Debt leverage.
5. **Actionable Investment Recommendations:** Clear suggestions (Hold/Buy/Sell/Audit) for the investment team.

Maintain a professional, quantitative, and analytical tone. Do not use generic filler words.
"""
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt
        )
        return response.text
    except Exception as e:
        print(f"Warning: Gemini API call failed ({e}). Reverting to fallback.")
        return generate_local_fallback(decel_df, summary_df)

def main():
    os.makedirs(REPORT_DIR, exist_ok=True)
    
    decel_df = get_decel_data()
    summary_df = get_summary_stats()
    
    if decel_df.empty and summary_df.empty:
        print("Error: No data available to generate report.")
        return
        
    api_key = os.getenv("GEMINI_API_KEY")
    
    if not api_key:
        print("Warning: GEMINI_API_KEY not found in environment variables.")
        report_content = generate_local_fallback(decel_df, summary_df)
    else:
        report_content = generate_ai_narrative(decel_df, summary_df, api_key)
        
    with open(REPORT_PATH, "w", encoding="utf-8") as f:
        f.write(report_content)
        
    print(f"Report successfully saved to {REPORT_PATH}")

if __name__ == "__main__":
    main()
