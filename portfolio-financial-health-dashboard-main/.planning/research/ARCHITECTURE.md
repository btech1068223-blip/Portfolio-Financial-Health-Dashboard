# Architecture Research

**Domain:** Portfolio Company Financial Health Dashboard
**Researched:** 2026-08-19
**Confidence:** HIGH

## Standard Architecture

### System Overview

```
┌─────────────────────────────────────────────────────────────┐
│                       Data Sources                          │
│                        [yfinance]                           │
├─────────────────────────────┬───────────────────────────────┤
│                             │ (extract.py)                  │
│                             ▼                               │
│                      [data/raw/*.json]                      │
├─────────────────────────────┬───────────────────────────────┤
│                             │ (transform.py)                │
│                             ▼                               │
│                 [Reshaped Tidy Pandas DF]                   │
├─────────────────────────────┬───────────────────────────────┤
│                             │ (load.py)                     │
│                             ▼                               │
│                 [data/financial_health.db]                  │
│             (SQLite Relational Schema, Views,               │
│                    and Update Triggers)                     │
├─────────────────────────────┼───────────────────────────────┤
│                             │                               │
│     (Power BI Dashboard)    │       (narrative.py)          │
│              ▼              │              ▼                │
│    [Trends, RAG Flags,      │      [Gemini 2.0 API]         │
│     Growth Rankings]        │              ▼                │
│                             │     [Stakeholder Report]      │
└─────────────────────────────┴───────────────────────────────┘
```

### Component Responsibilities

| Component | Responsibility | Typical Implementation |
|-----------|----------------|------------------------|
| `extract.py` | Connects to yfinance API, downloads quarterly/annual financials for SaaS companies, and serializes raw JSON to local files. | Python + yfinance |
| `transform.py` | Standardizes date columns, handles missing values, normalizes currency units, pivots wide data into clean long form. | Python + pandas |
| `load.py` | Sets up SQLite tables, view, and triggers; populates dimension tables and fact tables from clean dataframe. | Python + sqlite3 |
| `data/financial_health.db` | Stores structured transactional financial records. | SQLite File |
| `sql/` | Contains relational schemas and complex analytical queries (YoY growth, rolling averages, deceleration joins). | SQL Scripts |
| `dashboard/` | Contains the BI file connected directly to SQLite. | Power BI Desktop (.pbix) |
| `narrative.py` | Queries SQLite for decelerating companies and calls Gemini to format a narrative summary. | Python + google-genai |

## Recommended Project Structure

```
portfolio-financial-health-dashboard/
├── data/
│   ├── raw/                 # Raw extracted JSON files
│   └── financial_health.db  # SQLite database file
├── sql/
│   ├── schema.sql           # Database schema definition (tables, view, trigger)
│   ├── query_yoy_growth.sql # YoY growth CTE query
│   ├── query_margins.sql    # 4-quarter rolling margin query
│   ├── query_decel.sql      # Consecutive deceleration self-join query
│   └── query_view_summary.sql # Query that utilizes the custom view
├── src/
│   ├── extract.py           # Extract stage script
│   ├── transform.py         # Transform stage script
│   ├── load.py              # Load stage script
│   └── narrative.py         # GenAI narrative generation script
├── dashboard/
│   ├── dashboard.pbix       # Power BI Dashboard file
│   └── mock_dashboard.png   # Dashboard visual preview
├── .env.template            # API credentials template
├── README.md                # Project execution manual
└── requirements.txt         # Package dependencies
```

## Architectural Patterns

### Pattern 1: Tidy Data Ingest (Long-Format Fact Table)
- **What:** Storing financial records as a tall/long-format table (`company_id`, `period_id`, `metric`, `value`) instead of a wide table with separate columns for each financial metric.
- **When to use:** Keeps database schemas extensible when adding new metrics (e.g. Free Cash Flow) without requiring DDL table schema updates.
- **Trade-offs:** Requires joining facts and pivoting them for some simple dashboard representations, but highly normalized and standard.

### Pattern 2: Cache-first Ingest (Offline fallback)
- **What:** In `extract.py`, write raw data to `.json` files. If yfinance is offline or rate-limited during testing, the script can check for existing raw files and skip downloads.
- **When to use:** Crucial for presenting live interview demos where network speed/rate-limiting can break the pipeline.

## Data Flow

### Request Flow

```
[yfinance API]
      │
      ▼ (extract.py)
[data/raw/*.json]
      │
      ▼ (transform.py)
[Pandas Tidy Dataframe]
      │
      ▼ (load.py)
[SQLite DB Tables] ──(Triggers & Views)──► [Quarterly summary VIEW]
      │                                             │
      ├─────────────────────────────────────────────┤
      ▼ (sql/query_decel.sql)                       ▼
[Decelerating Growth Dataset]                [Power BI Dashboard]
      │
      ▼ (narrative.py)
[Google Gemini 2.0 API]
      │
      ▼
[Executive Stakeholder Narrative]
```

## Scaling Considerations

| Scale | Architecture Adjustments |
|-------|--------------------------|
| 10 tickers (Local Dev) | SQLite file storage (current design) is more than sufficient. |
| 100-500 companies | SQLite is still sufficient; add B-Tree indexes on `financials_fact(company_id, period_id, metric)`. |
| 10k+ companies (Enterprise) | Migrate ETL scripts to DBT + Snowflake/BigQuery with delta lake extraction. |

## Anti-Patterns

### Anti-Pattern 1: Hardcoding Ticker Metrics
- **What people do:** Write explicit columns in the fact table for `revenue`, `net_income`, etc., and manually parse indexes.
- **Why it's wrong:** Tickers often change accounting names or omit rows, breaking fixed-index extraction scripts.
- **Do this instead:** Parse metrics dynamically based on standard pandas row indexes and melt them.

## Integration Points

### External Services

| Service | Integration Pattern | Notes |
|---------|---------------------|-------|
| yfinance | Direct python import API client | Unofficial wrapper; rate limits can occur. |
| Google Gemini API | `Client()` from `google-genai` package | Requires `GEMINI_API_KEY` set in environment. |

---
*Architecture research for: Portfolio Company Financial Health Dashboard*
*Researched: 2026-08-19*
