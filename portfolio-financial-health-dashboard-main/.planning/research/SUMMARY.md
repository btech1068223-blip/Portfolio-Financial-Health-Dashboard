# Project Research Summary

**Project:** Portfolio Company Financial Health Dashboard
**Domain:** Financial Data ETL & Analytics
**Researched:** 2026-08-19
**Confidence:** HIGH

## Executive Summary

This project implements an end-to-end data intelligence pipeline that extracts, cleans, analyzes, and visualizes financial health metrics for 10 SaaS companies. Designed as a professional portfolio deliverable, the system ensures raw data tracking, strict database constraints, complex analytical queries, dynamic BI visualization, and AI stakeholder summarization.

The core stack consists of Python, SQLite, Power BI, and the Google Gemini API. Key risks include yfinance rate limits (mitigated by a local JSON extraction cache) and metric name variations (mitigated by index mapping in the transformation stage).

## Key Findings

### Recommended Stack

A lightweight, zero-dependency stack provides the maximum portability for interview demonstrations, avoiding Docker or external server setup.

**Core technologies:**
- **Python (3.11+):** Run scripting and pipeline logic.
- **SQLite (3.x):** Embedded relational database store.
- **yfinance:** Financial statement scraper.
- **google-genai:** Official SDK to run Gemini 2.0 narratives.
- **pandas:** Dataframe manipulation.

### Expected Features

**Must have (table stakes):**
- Automated yfinance ticker statement extraction (`extract.py`).
- Long-format normalization and metric alignment (`transform.py`).
- Relational SQLite tables, view, and triggers (`load.py`).
- CTE, window function, and consecutive self-join queries (`sql/*.sql`).
- Power BI dashboard showing trend, rankings, and alert flags.
- Gemini script (`narrative.py`) outputting a text narrative of decelerating tickers.

**Defer (v2+):**
- Scheduled pipelines (Apache Airflow / Prefect).
- Production cloud data warehouses (Snowflake, BigQuery).

### Architecture Approach

A clean folder separation separates data raw files, database stores, SQL files, source code, and dashboard files.

**Major components:**
1. **Extraction (`src/extract.py`):** Saves raw JSON per ticker.
2. **Transformation & Load (`src/transform.py`, `src/load.py`):** Normalizes fields and inserts records.
3. **Database (`data/financial_health.db`):** Star schema layout with fact and dimension tables.
4. **Narrative Script (`src/narrative.py`):** Generates Gemini executive reports.

### Critical Pitfalls

1. **yfinance Throttling:** Throttled queries with 1.5s sleep and cached file execution.
2. **Metric Label Drift:** Standardize Yahoo keys dynamically with a dictionary mapper.
3. **Power BI DB Locks:** Ensure Python script closes database connections to prevent SQLite lock errors in Power BI.

## Implications for Roadmap

Suggested phase structure:

### Phase 1: Data Extraction & Cache Caching
- **Rationale:** Get the raw data down and secure first, establishing a local fallback before running transformer steps.
- **Delivers:** `extract.py` + raw JSON backups.
- **Avoids:** yfinance rate limiting issues.

### Phase 2: Normalization & Schema Design
- **Rationale:** Design database structure and write transformation script to pivot and normalize data.
- **Delivers:** `transform.py` + SQL DDL schemas.

### Phase 3: SQLite Loading & View/Trigger Setup
- **Rationale:** Write loader script to instantiate schema and load normalized tables.
- **Delivers:** `load.py` + populated SQLite database.

### Phase 4: Analytical SQL Writing
- **Rationale:** Create `.sql` files containing business query requirements (YoY growth, rolling margins, deceleration).
- **Delivers:** Query script files.

### Phase 5: Power BI Dashboard & Visual Design
- **Rationale:** Build dashboard visuals connected to SQLite view.
- **Delivers:** `dashboard.pbix` file.

### Phase 6: GenAI Narrative Generation
- **Rationale:** Implement `narrative.py` connecting the database alerts to Gemini API.
- **Delivers:** `narrative.py` script.

### Phase 7: Setup Packaging & Documentation
- **Rationale:** Write setup script and comprehensive README to package the deliverable.
- **Delivers:** `README.md` and complete repo package.

## Confidence Assessment

| Area | Confidence | Notes |
|------|------------|-------|
| Stack | HIGH | Python and SQLite standard tools. |
| Features | HIGH | Table stakes fully capture prompt objectives. |
| Architecture | HIGH | Simple extraction and database loading sequence. |
| Pitfalls | HIGH | Throttling and key mapping address typical yfinance issues. |

**Overall confidence:** HIGH

---
*Research completed: 2026-08-19*
*Ready for roadmap: yes*
