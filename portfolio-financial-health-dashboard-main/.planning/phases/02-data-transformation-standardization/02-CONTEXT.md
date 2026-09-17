# Phase 2: Data Transformation & Standardization - Context

**Gathered:** 2026-08-19
**Status:** Ready for planning

<domain>
## Phase Boundary

Parse the raw JSON financial statement files, clean the metrics, calculate missing figures, align different fiscal calendars to standard calendar dates, and output a standardized, tidy dataset (long format) ready for database loading.

</domain>

<decisions>
## Implementation Decisions

### Normalization Format
- **D-01:** Transform the hierarchical JSON structure into a long (tidy) format with columns: `ticker`, `period_type` (quarterly/annual), `date` (standardized calendar date), `metric`, `value`.

### Fiscal Calendar Alignment
- **D-02:** Use the closest standard calendar quarter-end date (March 31, June 30, Sept 30, Dec 31) to map different companies' fiscal dates. This ensures clean cross-company comparison in the database and dashboard.

### Calculated Fields
- **D-03:** Calculate `gross_margin` explicitly as `(revenue - cost_of_revenue) / revenue` if not directly provided in the raw dataset. If cost of revenue is missing, fallback to `gross_profit / revenue`.

### Missing Data Handling
- **D-04:** Store missing financial metrics as `NULL` (or `None` in Pandas) rather than filling with `0`, to avoid skewing rolling averages or margins.

### output Artifacts
- **D-05:** Write the standardized data to `data/processed/clean_financials.csv`.

### the agent's Discretion
- The exact mapping rules for slight date shifts (e.g., date ending on Jan 3 instead of Dec 31 maps to Q4).
- Internal Pandas DataFrame operations (e.g., melt vs stack).

</decisions>

<specifics>
## Specific Ideas

- Log a summary of the number of rows processed per ticker to stdout for visibility.

</specifics>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

- `.planning/research/STACK.md` — Verified python packages and versions.
- `.planning/research/PITFALLS.md` — Detailed fiscal calendar misalignment mitigations.

</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets
- None.

### Established Patterns
- `data/raw/` JSON structure (created by Phase 1).

### Integration Points
- Reads from `data/raw/{ticker}.json` and outputs `data/processed/clean_financials.csv` which will be read by Phase 3 (`load.py`).

</code_context>

<deferred>
## Deferred Ideas

- SQLite table structure and schema definitions — deferred to Phase 3.

</deferred>

---

*Phase: 02-data-transformation-standardization*
*Context gathered: 2026-08-19*
