# Portfolio Company Financial Health Dashboard

## What This Is

An end-to-end data pipeline that extracts quarterly/annual financial data for 8-10 SaaS companies using `yfinance`, cleans and normalizes the data with Python, stores it in a structured SQLite database, performs advanced SQL queries, displays results in a Power BI dashboard, and generates AI stakeholder narratives using the Google Gemini API.

## Core Value

A reliable, reproducible, and fully functional end-to-end pipeline that accurately analyzes financial metrics (YoY growth, rolling average margins, decelerating periods) and surfaces them in a clear BI dashboard and GenAI report for investment decision-making.

## Business Context

- **Customer**: Internal Investment / PE Deal Team
- **Success metric**: 100% data ingestion accuracy and a stakeholder-ready 15-minute demo repo
- **Strategy notes**: Simulated portfolio company and competitor tracking platform

## Requirements

### Validated

(None yet — ship to validate)

### Active

- [ ] **Data Source (extract.py)**: Fetch 3-5 years of raw quarterly and annual financial statements for 10 SaaS companies (MSFT, CRM, ADBE, NOW, WDAY, DDOG, NET, HUBS, TEAM, OKTA) using `yfinance` and save raw data.
- [ ] **ETL Pipeline (transform.py, load.py)**: Tidy data into a long-format table, run data quality audits (nulls, duplicates, bounds), and load clean tables into SQLite.
- [ ] **Database Schema**: Relational design with `companies`, `date_dim`, `financials_fact` tables, an ER diagram, a quarterly joining view, and a `last_refreshed` trigger.
- [ ] **Analytical SQL**: Implement YoY revenue growth CTE, rolling 4-quarter margins average, decelerating growth join (2+ consecutive periods), and view queries.
- [ ] **Dashboard Design**: Create a Power BI dashboard showing revenue/margin trends, growth rankings, and RAG status.
- [ ] **GenAI Layer**: Implement a Python script using the `google-genai` SDK that reads decelerating growth company data and generates a stakeholder summary.
- [ ] **Documentation**: Write README with problem statement, architecture diagram, setup instructions, screenshots, and future improvements.

### Out of Scope

- [ ] **Incremental Loads**: Greenfield full reload is sufficient for single-day proof of concept.
- [ ] **Production Cloud DB (Snowflake/BigQuery)**: SQLite is chosen for zero-setup portability.
- [ ] **Airflow Ingestion Orchestration**: Simple python scripts executed sequentially are sufficient.
- [ ] **Complex Interactive Chatbot**: A simple script-generated stakeholder narrative is enough.

## Context

- Building a portfolio deliverable representing data intelligence capability for asset managers.
- Sector chosen: SaaS, with a selected ticker list.
- Technologies: Python, SQLite, SQL, Power BI, Google Gemini API.

## Constraints

- **Timeline**: 1 day (Must be completable quickly and work end-to-end).
- **Environment**: Local desktop setup; must run without complex external dependencies.
- **API Limits**: Graceful handling of yfinance API timeouts and rate limits.
- **Portability**: Database must be SQLite to allow self-contained repository sharing.

## Key Decisions

| Decision | Rationale | Outcome |
|----------|-----------|---------|
| SQLite Database | Offers zero-setup, self-contained file database for interview portability. | — Pending |
| SaaS Sector | High interest for PE firms; predictable SaaS metrics (gross margin, revenue growth). | — Pending |
| Google GenAI SDK | Uses modern `google-genai` SDK for lightweight, state-of-the-art text generation. | — Pending |

## Evolution

This document evolves at phase transitions and milestone boundaries.

**After each phase transition** (via `/gsd-transition`):
1. Requirements invalidated? → Move to Out of Scope with reason
2. Requirements validated? → Move to Validated with phase reference
3. New requirements emerged? → Add to Active
4. Decisions to log? → Add to Key Decisions
5. "What This Is" still accurate? → Update if drifted

**After each milestone** (via `/gsd-complete-milestone`):
1. Full review of all sections
2. Core Value check — still the right priority?
3. Business Context check (if present) — customer, revenue model, success metric still accurate?
4. Audit Out of Scope — reasons still valid?
5. Update Context with current state

---
*Last updated: 2026-08-19 after initialization*
