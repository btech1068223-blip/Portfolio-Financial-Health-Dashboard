# Stack Research

**Domain:** Portfolio Company Financial Health Dashboard
**Researched:** 2026-08-19
**Confidence:** HIGH

## Recommended Stack

### Core Technologies

| Technology | Version | Purpose | Why Recommended |
|------------|---------|---------|-----------------|
| Python | 3.11+ | Pipeline logic and ETL script execution | Standard data analysis language with rich yfinance, pandas, and SQLite bindings. |
| SQLite | 3.x | Relational database engine | Self-contained, file-based, zero-configuration database that makes the repository 100% portable for demo walkthroughs. |
| google-genai | latest (0.1.x+) | GenAI narrative generator | Official, lightweight Google SDK for accessing Gemini 2.0 models to write stakeholder summaries. |
| yfinance | latest (0.2.x) | Financial data source | Most popular open-source library for pulling Yahoo Finance market data without paid API keys. |
| pandas | 2.x | Data manipulation and cleaning | Standard library for structuring, transforming, and cleaning financial tables in Python. |

### Supporting Libraries

| Library | Version | Purpose | When to Use |
|---------|---------|---------|-------------|
| sqlite3 | (Built-in) | Database connection adapter | Core library for executing DDL/DML, views, triggers, and SQL analytical queries in SQLite. |
| python-dotenv | 1.0.x | API key environment loader | Loading Gemini API keys from `.env` files securely. |
| openpyxl | 3.1.x | Excel spreadsheet support | Optional backup export or raw data audit reporting. |

### Development Tools

| Tool | Purpose | Notes |
|------|---------|-------|
| Power BI Desktop | Dashboard creation and visualization | Connected directly to the SQLite database file to display financial health metrics. |
| VS Code / IDE | Coding environment | Used for Python script creation, SQL query writing, and documentation. |

## Installation

```bash
# Core
pip install yfinance pandas google-genai python-dotenv
```

## Alternatives Considered

| Recommended | Alternative | When to Use Alternative |
|-------------|-------------|-------------------------|
| SQLite | PostgreSQL | Use when deploying to a shared hosting environment, or when concurrency and multi-user writes are required. |
| google-genai | openai / langchain | Use langchain if integrating multiple agent behaviors, memory components, or other vector stores (overkill for simple stakeholder summaries). |

## What NOT to Use

| Avoid | Why | Use Instead |
|-------|-----|-------------|
| Raw REST scraping | Yahoo Finance API endpoints are undocumented and change frequently, causing scraper breakage. | `yfinance` library which actively updates to resolve breaking endpoint changes. |
| CSV files as final DB | Lacks relational constraints, views, indexes, triggers, and SQL capability required for analytical dashboard queries. | SQLite database. |

## Stack Patterns by Variant

**If offline / mockup mode:**
- Use cached JSON files containing historical ticker data.
- Because it allows the pipeline to execute even without internet or when yfinance is rate-limited.

**If cloud scale is needed:**
- Use Snowflake or BigQuery with DBT for transform and Airflow for orchestration.
- Because it supports enterprise-scale warehousing and scheduled pipeline execution.

## Version Compatibility

| Package A | Compatible With | Notes |
|-----------|-----------------|-------|
| google-genai@0.1.1 | Python >= 3.10 | Required for the new unified Google GenAI client syntax. |
| yfinance@0.2.40 | pandas >= 2.0 | Standard data-frame structure alignment. |

## Sources

- [yfinance on PyPI](https://pypi.org/project/yfinance/) — verified quarterly statements syntax (`ticker.quarterly_income_stmt`, `ticker.quarterly_cashflow`).
- [Google GenAI Python SDK Docs](https://googleapis.github.io/python-genai/) — verified `Client()` initialization and `models.generate_content` syntax.

---
*Stack research for: Portfolio Company Financial Health Dashboard*
*Researched: 2026-08-19*
