# Phase 6: GenAI Narrative Generation - Context

**Gathered:** 2026-08-19
**Status:** Ready for planning

<domain>
## Phase Boundary

Write the Python script `src/narrative.py` that queries the SQLite database (focusing on decelerating companies, margins, and growth metrics), formats this data into a structured prompt, calls the Google Gemini 2.0 API using the official `google-genai` SDK, and outputs an executive stakeholder narrative report in markdown under `reports/`.

</domain>

<decisions>
## Implementation Decisions

### API Integration
- **D-01:** Use the official `google-genai` Python SDK (not legacy `google-generativeai`).
- **D-02:** Model choice: `gemini-2.0-flash`.
- **D-03:** Initialize the client as `client = genai.Client()`, which automatically resolves `GEMINI_API_KEY` from the environment.

### Script Execution & Data Gathering
- **D-04:** `src/narrative.py` queries:
  - List of companies flagged with consecutive growth deceleration (using the view or queries built in Phase 4).
  - Overall summary stats (aggregate revenue, average margins).
- **D-05:** Format SQLite query outputs as markdown tables inside the prompt to guide Gemini's generation.

### Report Output & Fallback
- **D-06:** Write output markdown file to `reports/stakeholder_narrative.md`.
- **D-07:** Provide a graceful fallback to a locally generated heuristic report if `GEMINI_API_KEY` is not present in the environment or if the API call fails due to rate limits/timeouts.

### the agent's Discretion
- Prompt engineering structure (e.g. system instructions, persona as a Principal Portfolio Analyst).
- Exact layout of local fallback heuristics.

</decisions>

<specifics>
## Specific Ideas

- The generated report should include a brief executive summary, key drivers of deceleration for flagged holdings (e.g., HubSpot, Cloudflare), and actionable investment recommendations (Hold/Sell/Audit).

</specifics>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

- `.planning/research/STACK.md` — Verified `google-genai` Python SDK syntax.
- `.planning/research/FEATURES.md` — GenAI report parameters.

</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets
- `data/financial_health.db` database and its views (created in Phase 3/4).
- `sql/query_decel.sql` logic (created in Phase 4).

### Established Patterns
- python-dotenv config loading.

### Integration Points
- Consumes database tables and writes output to `reports/stakeholder_narrative.md`.

</code_context>

<deferred>
## Deferred Ideas

- Orchestrator/ETL pipeline scripts compilation — deferred to Phase 7.

</deferred>

---

*Phase: 06-genai-narrative-generation*
*Context gathered: 2026-08-19*
