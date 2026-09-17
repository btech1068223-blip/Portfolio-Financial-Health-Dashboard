# Feature Research

**Domain:** Portfolio Company Financial Health Dashboard
**Researched:** 2026-08-19
**Confidence:** HIGH

## Feature Landscape

### Table Stakes (Users Expect These)

Features users assume exist. Missing these = product feels incomplete.

| Feature | Why Expected | Complexity | Notes |
|---------|--------------|------------|-------|
| Multi-Ticker Extraction | Users need to track 8-10 companies in a single sector. | LOW | Handled via yfinance loop over ticker array. |
| Raw Data Preservation | Crucial for auditing extraction errors before transformation. | LOW | Save raw statements to JSON/CSV before cleaning. |
| Period Normalization | Financial quarters align differently for each company; data must be standardized. | MEDIUM | Standardize Yahoo dates to `YYYY-QQ` formats. |
| Long-Format Tidying | Clean fact-dimension model requires long-format tidy data. | MEDIUM | Reshape (melt) wide pandas DataFrames into rows. |
| Relational DB Storage | Keeps data organized and queryable with foreign key integrity. | LOW | Write data into SQLite dimension and fact tables. |
| Analytical SQL View | Facilitates clean joining of facts and dimensions for the BI dashboard. | LOW | Create a quarterly summary VIEW. |
| Last Refreshed Trigger | Keeps track of when database data was modified. | LOW | SQLite trigger updating `last_refreshed` timestamp. |
| Advanced SQL Queries | Investment teams require deep analytical metrics (growth, margins, trend flags). | MEDIUM | CTEs, window functions (AVG OVER), and self-joins. |
| BI Dashboard Visuals | Visual layout for quick inspection of trends, rankings, and alerts. | MEDIUM | Trend lines, YoY bar chart, RAG flags. |
| GenAI Stakeholder Summary | Automatic interpretation of data for non-technical leadership. | LOW | Simple script reading SQLite query and calling Gemini. |

### Differentiators (Competitive Advantage)

Features that set the product apart. Not required, but valuable.

| Feature | Value Proposition | Complexity | Notes |
|---------|-------------------|------------|-------|
| Offline Ticker Cache | Prevents yfinance API rate limiting and allows offline demos. | LOW | Cache extracted files locally; run pipeline from cache if offline. |
| Dynamic SQL Alert Views | Pre-computes deceleration flags directly in SQL for easy dashboard connection. | MEDIUM | Create a VIEW that implements consecutive deceleration joins. |
| Auto-install Requirements script | Ensures one-command setup for the interviewer. | LOW | Provide a setup shell script or a clear README installation instruction. |

### Anti-Features (Commonly Requested, Often Problematic)

Features that seem good but create problems.

| Feature | Why Requested | Why Problematic | Alternative |
|---------|---------------|-----------------|-------------|
| Real-time Price Tickers | "See current stock price" | Adds noise, doesn't reflect long-term portfolio financial statement health. | Focus on quarterly financial metrics. |
| Multi-user Dashboard Login | "Secure dashboard access" | Unnecessary overhead for a local portfolio project walkthrough. | Simple self-contained Power BI file. |

## Feature Dependencies

```
[yfinance Extraction]
    └──requires──> [Ticker Tidy Transformation]
                       └──requires──> [Relational Load to SQLite]
                                          ├──requires──> [Advanced SQL Views/Queries]
                                          │                  └──requires──> [GenAI Narrative Script]
                                          └──requires──> [Power BI Dashboard Visuals]
```

### Dependency Notes

- **Tidy Transformation requires Extraction:** Raw data must exist and contain required keys before reshaping.
- **SQLite Load requires Tidy Transformation:** The database schema is designed for normalized long-format records.
- **SQL Views and Queries require SQLite Load:** Tables must exist and be populated.
- **GenAI Narrative requires SQL Queries:** The script reads the output of the decelerating growth SQL query.
- **Power BI Dashboard requires SQLite Load:** The dashboard connects to the populated tables and view.

## MVP Definition

### Launch With (v1)

Minimum viable product — what's needed to validate the concept.

- [ ] Multi-Ticker Extraction (`extract.py`) — downloads SaaS financials.
- [ ] Financials Transformation (`transform.py`) — normalizes metrics and periods.
- [ ] Relational DB Loader (`load.py`) — creates tables, view, trigger, and loads data.
- [ ] Analytical SQL Scripts (`YoY_growth.sql`, `margins.sql`, `deceleration.sql`) — implements business logic.
- [ ] Power BI Dashboard — visualizes SQLite tables.
- [ ] GenAI Summary Script (`narrative.py`) — queries database and returns Gemini summary.
- [ ] Documentation — README with architecture flow and ER diagram.

## Feature Prioritization Matrix

| Feature | User Value | Implementation Cost | Priority |
|---------|------------|---------------------|----------|
| ETL Pipelines (`extract`, `transform`, `load`) | HIGH | MEDIUM | P1 |
| DB View & Trigger Schema | HIGH | LOW | P1 |
| Advanced SQL Queries | HIGH | MEDIUM | P1 |
| Power BI Dashboard | HIGH | MEDIUM | P1 |
| Gemini Stakeholder Narrative | HIGH | LOW | P1 |
| Offline Cache Fallback | MEDIUM | LOW | P2 |

**Priority key:**
- P1: Must have for launch
- P2: Should have, add when possible
- P3: Nice to have, future consideration

## Sources

- PE Data Analyst Standard Job Descriptions — focus on ETL pipelines, SQL views/window functions, and BI tools.
- Google Gemini API guide.

---
*Feature research for: Portfolio Company Financial Health Dashboard*
*Researched: 2026-08-19*
