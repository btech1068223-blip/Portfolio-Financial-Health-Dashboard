# Pitfalls Research

**Domain:** Portfolio Company Financial Health Dashboard
**Researched:** 2026-08-19
**Confidence:** HIGH

## Critical Pitfalls

### Pitfall 1: yfinance Rate Limits and Connection Blocks

**What goes wrong:**
During bulk downloads for multiple tickers, Yahoo Finance may rate limit or temporarily block the extraction client IP, resulting in empty DataFrames or connection resets.

**Why it happens:**
yfinance uses scraping techniques under the hood. Frequent back-to-back requests trigger Yahoo rate limit thresholds.

**How to avoid:**
1. Introduce a delay (e.g. `time.sleep(1.5)`) between requests.
2. Implement local file-based caching in `extract.py` to check for raw downloaded files first, avoiding remote calls on subsequent development runs.

**Warning signs:**
Empty DataFrames returned by `ticker.quarterly_income_stmt` or HTTP 429/Too Many Requests exceptions.

**Phase to address:**
Phase 1 (Data Extraction).

---

### Pitfall 2: Disaligned Fiscal Calendars

**What goes wrong:**
Some companies have fiscal years that do not match the calendar year (e.g., MSFT's fiscal year ends on June 30, whereas CRM's ends on January 31). Storing them by calendar quarter might disalign actual comparable quarterly reporting periods.

**Why it happens:**
Companies align their quarters with operational seasons, not calendar months.

**How to avoid:**
Map reporting periods to a unified date scale using the exact calendar month of the report (e.g., March/April -> Q1, June/July -> Q2, Sept/Oct -> Q3, Dec/Jan -> Q4) or record the raw reporting date and allow the date dimension table to resolve the calendar year and fiscal quarter.

**Warning signs:**
Visual representations in Power BI showing misaligned time series lines or empty quarters for certain companies.

**Phase to address:**
Phase 2 (Transformation & Schema Design).

---

### Pitfall 3: Ticker-Specific Metric Key Drift

**What goes wrong:**
Yahoo Finance returns different row index labels for different companies or over time (e.g., "Total Revenue" vs "Operating Revenue" vs "Revenue").

**Why it happens:**
Drift in Yahoo Finance's schema and reporting structures per industry sector.

**How to avoid:**
Use a robust metric normalization dictionary in `transform.py` that maps multiple potential source strings to a single database metric label.
Example mapping: `{"Total Revenue": "revenue", "Revenue": "revenue", "Operating Revenue": "revenue"}`.

**Warning signs:**
`pandas` `KeyError` during mapping or fact table records missing revenue rows.

**Phase to address:**
Phase 2 (Transformation).

## Technical Debt Patterns

| Shortcut | Immediate Benefit | Long-term Cost | When Acceptable |
|----------|-------------------|----------------|-----------------|
| Skipping Local Caching | Faster initial script writing. | Rate limits block development work; testing is impossible offline. | Only for tiny 1-ticker scripts. |
| Storing raw dates as text dimensions | Avoids date conversion logic. | SQL date calculations (YoY, lag) become slow or impossible in SQLite. | Never. |

## Integration Gotchas

| Integration | Common Mistake | Correct Approach |
|-------------|----------------|------------------|
| Gemini API | Hardcoding API Keys in script. | Use `python-dotenv` and read keys from `os.environ`. |
| Power BI SQLite Connection | Keeping Power BI connection active, locking SQLite file during Python write. | Close Power BI file or disconnect refresh during database rebuilds. |

## Performance Traps

| Trap | Symptoms | Prevention | When It Breaks |
|------|----------|------------|----------------|
| Cartesian Joins | YoY growth queries take seconds to execute. | Ensure `financials_fact` has unique composite keys and joins are made on indexed integer IDs. | At 100+ tickers. |

## Security Mistakes

| Mistake | Risk | Prevention |
|---------|------|------------|
| Committing `.env` | Leak of Google Gemini API key to public GitHub repo. | Add `.env` to `.gitignore`. |

---
*Pitfalls research for: Portfolio Company Financial Health Dashboard*
*Researched: 2026-08-19*
