# Phase 3: SQLite Storage & Schema Setup - Context

**Gathered:** 2026-08-19
**Status:** Ready for planning

<domain>
## Phase Boundary

Set up the relational SQLite database `data/financial_health.db` with a normalized schema (`companies` and `financials` tables), define custom summary views to pivot the long data, implement timestamp update triggers, and write a python script `src/load.py` to ingest the processed CSV into the database.

</domain>

<decisions>
## Implementation Decisions

### Relational Database Schema
- **D-01:** Implement a star-style schema with:
  - `companies` table: `company_id` (INTEGER PK), `ticker` (TEXT UNIQUE), `company_name` (TEXT).
  - `financials` table: `financial_id` (INTEGER PK), `company_id` (INTEGER FK), `period_type` (TEXT), `date` (TEXT), `metric` (TEXT), `value` (REAL), `last_refreshed` (TIMESTAMP DEFAULT CURRENT_TIMESTAMP).
- **D-02:** Store DDL definitions in a standard `sql/schema.sql` file.

### Views & Triggers
- **D-03:** Define custom SQL views (`quarterly_summary` and `annual_summary`) to pivot long-format metrics back into wide format (columns: revenue, net_income, operating_cash_flow, total_debt, gross_margin) for easier querying and BI integration.
- **D-04:** Create an AFTER INSERT trigger to automatically update `last_refreshed = CURRENT_TIMESTAMP` for loaded records.

### Loading Strategy
- **D-05:** `src/load.py` will read `data/processed/clean_financials.csv`, lookup company IDs, insert unique companies into the `companies` table, and write records to `financials` using transactions (`INSERT OR REPLACE`) for idempotency.

### the agent's Discretion
- The exact company name mapping (can fallback to yfinance info lookup or simply capitalize/default the ticker).
- Transaction commit batch size (recommend loading all records in a single transaction).

</decisions>

<specifics>
## Specific Ideas

- Fallback: Company name mapping can be derived by mapping tickers to names (e.g. MSFT -> Microsoft Corp, CRM -> Salesforce Inc) or by simply using the ticker string if lookups fail.

</specifics>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

- `.planning/research/STACK.md` — Relational SQLite connection details.
- `.planning/research/ARCHITECTURE.md` — Proposed database schema and views.

</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets
- None.

### Established Patterns
- Transformed CSV structure at `data/processed/clean_financials.csv` (created in Phase 2).

### Integration Points
- Consumes from `data/processed/clean_financials.csv` and outputs database file at `data/financial_health.db` which is queried by Phase 4 and Phase 6.

</code_context>

<deferred>
## Deferred Ideas

- Analytical SQL queries (YoY growth, rolling margin averages) — deferred to Phase 4.

</deferred>

---

*Phase: 03-sqlite-storage-schema-setup*
*Context gathered: 2026-08-19*
