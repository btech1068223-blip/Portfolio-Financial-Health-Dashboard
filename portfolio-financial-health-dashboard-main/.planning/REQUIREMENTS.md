# Requirements: Portfolio Company Financial Health Dashboard

**Defined:** 2026-08-19
**Core Value:** A reliable, reproducible, and fully functional end-to-end pipeline that accurately extracts, normalizes, analyzes, and visualizes financial health metrics for SaaS companies.

## v1 Requirements

### Data Extraction (extract.py)

- [x] **EXTR-01**: Fetch 3-5 years of quarterly and annual financial statements (income, balance, cashflow) for 10 SaaS tickers: MSFT, CRM, ADBE, NOW, WDAY, DDOG, NET, HUBS, TEAM, OKTA.
- [x] **EXTR-02**: Save raw downloaded data as-is to local JSON files (`data/raw/`) before any transformation.
- [x] **EXTR-03**: Handle API errors, timeouts, rate limits, and missing tickers gracefully without halting execution.

### Data Transformation (transform.py)

- [x] **TRNS-01**: Clean period dates and map them to unified fiscal year/quarter identifiers.
- [x] **TRNS-02**: Pivot and reshape raw wide financial statements into a tidy long-format table (one row per company-period-metric).
- [x] **TRNS-03**: Handle null values, data anomalies, and standard currency/unit divisions.
- [x] **TRNS-04**: Log data quality indicators (null counts, duplicate rows, row counts processed).

### Database Storage (load.py)

- [x] **LOAD-01**: Create SQLite database `data/financial_health.db` with relational schema: `companies`, `date_dim`, and `financials_fact`.
- [x] **LOAD-02**: Implement a SQLite TRIGGER to auto-update a `last_refreshed` timestamp on table updates.
- [x] **LOAD-03**: Create a SQLite VIEW joining fact and dimension tables to provide clean quarterly aggregates.
- [x] **LOAD-04**: Load transformed pandas records into the database with foreign key integrity.

### Analytical SQL

- [x] **ASQL-01**: Write a CTE-based SQL query to compute YoY revenue growth per company.
- [x] **ASQL-02**: Write a window function SQL query to compute 4-quarter rolling average margins.
- [x] **ASQL-03**: Write a self-joining SQL query to identify companies with 2+ consecutive periods of decelerating growth.
- [x] **ASQL-04**: Write a SQL query demonstrating how to read metrics from the custom database VIEW.

### Business Intelligence Dashboard

- [x] **DASH-01**: Build a single-page Power BI dashboard showing trend lines, growth ranking bar charts, and operational flags.
- [x] **DASH-02**: Connect the dashboard directly to the local SQLite database.
- [x] **DASH-03**: Generate dashboard mockup screenshot files to represent the visuals in the README.

### GenAI Narrative Layer (narrative.py)

- [x] **GAIL-01**: Query the SQLite database for decelerating growth companies.
- [x] **GAIL-02**: Initialize the official `google-genai` client and send query data to Gemini 2.0.
- [x] **GAIL-03**: Output a clean, 2-3 sentence stakeholder-friendly report summary.

### Packaging & Documentation

- [x] **PACK-01**: Write `README.md` with problem statement, architecture flow diagram, database ER diagram, setup instructions, and future improvements.
- [x] **PACK-02**: Write `requirements.txt` with version-pinned pip packages.

## v2 Requirements

### Production Readiness

- **PROD-01**: Schedule ingestion using Apache Airflow or Prefect.
- **PROD-02**: Support incremental data loading instead of full pipeline refreshes.
- **PROD-03**: Migrate database target to Snowflake, BigQuery, or Databricks.

## Out of Scope

| Feature | Reason |
|---------|--------|
| Real-time stock prices | Out of scope for retrospective financial statement health analysis. |
| Multi-user credentials | Unnecessary complexity for a local portfolio demo package. |
| Full chatbot UI | A lightweight summary script is requested to fulfill prompt requirements. |

## Traceability

| Requirement | Phase | Status |
|-------------|-------|--------|
| EXTR-01 | Phase 1 | Complete |
| EXTR-02 | Phase 1 | Complete |
| EXTR-03 | Phase 1 | Complete |
| TRNS-01 | Phase 2 | Complete |
| TRNS-02 | Phase 2 | Complete |
| TRNS-03 | Phase 2 | Complete |
| TRNS-04 | Phase 2 | Complete |
| LOAD-01 | Phase 3 | Complete |
| LOAD-02 | Phase 3 | Complete |
| LOAD-03 | Phase 3 | Complete |
| LOAD-04 | Phase 3 | Complete |
| ASQL-01 | Phase 4 | Complete |
| ASQL-02 | Phase 4 | Complete |
| ASQL-03 | Phase 4 | Complete |
| ASQL-04 | Phase 4 | Complete |
| DASH-01 | Phase 5 | Complete |
| DASH-02 | Phase 5 | Complete |
| DASH-03 | Phase 5 | Complete |
| GAIL-01 | Phase 6 | Complete |
| GAIL-02 | Phase 6 | Complete |
| GAIL-03 | Phase 6 | Complete |
| PACK-01 | Phase 7 | Complete |
| PACK-02 | Phase 7 | Complete |

**Coverage:**

- v1 requirements: 23 total
- Mapped to phases: 23
- Unmapped: 0 ✓

---
*Requirements defined: 2026-08-19*
*Last updated: 2026-08-19 after initial definition*
