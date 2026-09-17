# Power BI Visual Dashboard Design & Connection Guide

This document describes how to connect, model, and visualize the portfolio company data stored in `data/financial_health.db` using Power BI.

---

## 1. Connecting Power BI to SQLite

To load data from `financial_health.db` into Power BI:

### Step 1: Install SQLite ODBC Driver
1. Download and install the **SQLite ODBC Driver** (e.g., from Christian Werner's SQLite ODBC page).
2. Install either the 32-bit or 64-bit version depending on your Power BI Desktop architecture (usually 64-bit).

### Step 2: Configure System DSN (Optional but Recommended)
1. Open **ODBC Data Source Administrator** on Windows.
2. Go to the **System DSN** tab and click **Add**.
3. Select **SQLite 3 ODBC Driver** and click **Finish**.
4. Configure the Data Source:
   - **Data Source Name (DSN):** `SQLite_SaaS_Portfolio`
   - **Database Name:** Browse and select the absolute path to `d:\portfolio-financial-health-dashboard\data\financial_health.db`.
5. Click **OK** to save.

### Step 3: Connect in Power BI Desktop
1. Click **Get Data** -> **ODBC**.
2. Select `DSN=SQLite_SaaS_Portfolio` or select **None** and enter the connection string:
   ```odbc
   driver={SQLite3 ODBC Driver};database=D:\portfolio-financial-health-dashboard\data\financial_health.db;
   ```
3. Under credentials, select **Default or Custom** and click **Connect** (no username/password needed for SQLite).
4. In the Navigator window, select the following views/tables:
   - `companies` (Dimension table)
   - `quarterly_summary` (Pivoted Quarterly View)
   - `annual_summary` (Pivoted Annual View)

---

## 2. Power BI Data Model (Star Schema)

In Power BI's Model View, establish relationships as follows:

- **Relationships:**
  - One-to-Many relationship from `companies(ticker)` to `quarterly_summary(ticker)`.
  - One-to-Many relationship from `companies(ticker)` to `annual_summary(ticker)`.
- **Cross Filter Direction:** Single (Company filters Financials).

---

## 3. Custom DAX Measures

Create a new table `_Measures` and implement the following measures:

### Total Portfolio Revenue (LTM)
```dax
Total Revenue = SUM(quarterly_summary[revenue])
```

### Portfolio Gross Margin %
```dax
Avg Gross Margin = AVERAGE(quarterly_summary[gross_margin])
```

### YoY Revenue Growth %
```dax
YoY Revenue Growth = 
VAR CurrentRevenue = SUM(quarterly_summary[revenue])
VAR PrevRevenue = 
    CALCULATE(
        SUM(quarterly_summary[revenue]),
        DATEADD(quarterly_summary[date].[Date], -1, YEAR)
    )
RETURN 
    DIVIDE(CurrentRevenue - PrevRevenue, PrevRevenue)
```

### Debt-to-Revenue Ratio %
```dax
Debt to Revenue = DIVIDE(SUM(quarterly_summary[total_debt]), SUM(quarterly_summary[revenue]))
```

### Growth Deceleration Alert Badge
```dax
Deceleration Alert = 
VAR CurrentQoQ = 
    DIVIDE(
        SUM(quarterly_summary[revenue]) - CALCULATE(SUM(quarterly_summary[revenue]), DATEADD(quarterly_summary[date].[Date], -1, QUARTER)),
        CALCULATE(SUM(quarterly_summary[revenue]), DATEADD(quarterly_summary[date].[Date], -1, QUARTER))
    )
VAR PrevQoQ = 
    CALCULATE(
        DIVIDE(
            SUM(quarterly_summary[revenue]) - CALCULATE(SUM(quarterly_summary[revenue]), DATEADD(quarterly_summary[date].[Date], -1, QUARTER)),
            CALCULATE(SUM(quarterly_summary[revenue]), DATEADD(quarterly_summary[date].[Date], -1, QUARTER))
        ),
        DATEADD(quarterly_summary[date].[Date], -1, QUARTER)
    )
VAR PrevPrevQoQ = 
    CALCULATE(
        DIVIDE(
            SUM(quarterly_summary[revenue]) - CALCULATE(SUM(quarterly_summary[revenue]), DATEADD(quarterly_summary[date].[Date], -1, QUARTER)),
            CALCULATE(SUM(quarterly_summary[revenue]), DATEADD(quarterly_summary[date].[Date], -1, QUARTER))
        ),
        DATEADD(quarterly_summary[date].[Date], -2, QUARTER)
    )
RETURN
    IF(CurrentQoQ < PrevQoQ && PrevQoQ < PrevPrevQoQ, "GROWTH SLOWDOWN", "STABLE")
```

---

## 4. Visual Dashboard Tab Layouts

### Tab 1: Executive Overview
- **KPI Cards:**
  - Total Portfolio Revenue (LTM) with YoY indicator (+12%).
  - Average Gross Margin Gauge chart (82%).
  - Aggregate Debt-to-Revenue Card (15%).
- **Revenue & Net Income Growth Trends:** Line chart plotting quarterly aggregate revenue and net income.
- **Top 10 Holdings Comparison:** Stacked column chart plotting Gross Margin % vs OCF Margin % per ticker.
- **Risk Alerts Panel:** Table showing tickers flagged with a "GROWTH SLOWDOWN" warning badge.

### Tab 2: Company Deep-Dive
- **Slicer:** Dropdown filter to select a specific company (`ticker`).
- **Financial Cards:** Displays quarterly details for Selected Company.
- **Historical Trends:** Area chart showing Revenue vs Gross Profit vs Operating Cash Flow.

### Tab 3: Risk Assessment
- **Deceleration Table:** Lists tickers with 2+ consecutive quarters of growth deceleration.
- **Leverage Scatter Plot:** Plots Debt-to-Revenue Ratio vs OCF Margin % to identify over-leveraged companies with weak cash flows.
