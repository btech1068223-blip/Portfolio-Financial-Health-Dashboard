# Phase 4: Advanced SQL Analytics - Context

**Gathered:** 2026-08-19
**Status:** Ready for planning

<domain>
## Phase Boundary

Write advanced SQL analytical queries targeting YoY growth, rolling average margins, and revenue growth deceleration, and save them as standalone `.sql` scripts under `sql/` for dashboard use and narrative generator scripting.

</domain>

<decisions>
## Implementation Decisions

### SQL Analytical Targets
- **D-01:** YoY Growth script (`sql/query_yoy_growth.sql`):
  - Calculates YoY revenue and net income growth rate by comparing a calendar quarter to the same quarter of the previous year (e.g. Q1 2024 vs Q1 2023).
- **D-02:** Rolling Average margins script (`sql/query_margins.sql`):
  - Calculates 4-quarter rolling average of gross margin and operating cash flow margin (defined as `operating_cash_flow / revenue`).
- **D-03:** Deceleration detection script (`sql/query_decel.sql`):
  - Identifies companies experiencing 2 or more consecutive quarters of decelerating revenue growth compared to the prior period (e.g., Growth_Q2 < Growth_Q1 AND Growth_Q3 < Growth_Q2).

### Execution environment
- **D-04:** Queries must execute successfully in standard SQLite 3.x using standard SQL CTEs (Common Table Expressions) and window functions (e.g., `LAG()`, `AVG() OVER()`).

### the agent's Discretion
- Exact layout of SQL CTEs and aliases.
- Additional sorting or limits in sample execution.

</decisions>

<specifics>
## Specific Ideas

- None.

</specifics>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

- `.planning/research/FEATURES.md` — Scopes YoY growth, rolling margins, and deceleration requirements.
- `.planning/research/ARCHITECTURE.md` — Mapped SQL scripts location.

</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets
- `quarterly_summary` and `annual_summary` pivoted views (created in Phase 3) — highly recommended to simplify the CTE joins.

### Established Patterns
- Database file `data/financial_health.db` (created in Phase 3).

### Integration Points
- Views created here will be read directly by Power BI and the GenAI stakeholder reporter script (`narrative.py` in Phase 6).

</code_context>

<deferred>
## Deferred Ideas

- None.

</deferred>

---

*Phase: 04-advanced-sql-analytics*
*Context gathered: 2026-08-19*
