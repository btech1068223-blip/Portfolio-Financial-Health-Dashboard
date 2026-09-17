---
phase: 04-advanced-sql-analytics
subsystem: analytics
tags: [sql, cte, window-functions]
provides:
  - Complex YoY revenue and net income growth calculations in sql/query_yoy_growth.sql
  - 4-quarter rolling averages for gross margin and OCF margin in sql/query_margins.sql
  - Growth deceleration tracking in sql/query_decel.sql
duration: 15min
completed: 2026-08-19
status: complete
---

# Phase 4 Summary: Advanced SQL Analytics

All requirements for Phase 4 have been successfully implemented, verified, and locked.

## Accomplishments
- **YoY Growth:** Created `sql/query_yoy_growth.sql` using SQLite `LAG(revenue, 4)` window functions to compare quarterly results year-over-year.
- **Rolling Margins:** Created `sql/query_margins.sql` utilizing `AVG() OVER()` to calculate 4-quarter rolling averages for Gross and Operating Cash Flow margins.
- **Deceleration:** Created `sql/query_decel.sql` using QoQ growth deceleration to isolate companies undergoing 2+ quarters of consecutive growth slowdowns (isolating HubSpot and Cloudflare).
- **Verification:** Verification report (`04-VERIFICATION.md`) passed with 100% must-haves met.

## Key Files Created
- [`sql/query_yoy_growth.sql`](file:///d:/portfolio-financial-health-dashboard/sql/query_yoy_growth.sql) — YoY calculations.
- [`sql/query_margins.sql`](file:///d:/portfolio-financial-health-dashboard/sql/query_margins.sql) — Rolling margins averages.
- [`sql/query_decel.sql`](file:///d:/portfolio-financial-health-dashboard/sql/query_decel.sql) — Slowdown detection.

## Next Up
Phase 5: BI Dashboard Creation — Wire up SQLite views to a mock dashboard, configure visual metrics, and document Power BI connections.
