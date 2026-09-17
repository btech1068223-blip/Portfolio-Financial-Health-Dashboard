# Roadmap: Portfolio Company Financial Health Dashboard

## Overview

This roadmap defines the construction of a self-contained, end-to-end financial intelligence pipeline. It starts with downloading financial statements for 10 SaaS companies via yfinance, transforms and loads the data into an embedded SQLite database, executes advanced SQL queries, visualizes results in a Power BI dashboard, and calls Gemini 2.0 to write executive narrative summaries.

## Phases

- [x] **Phase 1: Data Ingestion & Local Caching** - Build extract.py script to fetch and cache raw yfinance statements. (completed 2026-08-19)
- [x] **Phase 2: Data Transformation & Standardization** - Clean periods, resolve labels, and melt statements into a tidy format. (completed 2026-08-19)
- [x] **Phase 3: SQLite Storage & Schema Setup** - Establish database tables, trigger, view, and implement loader script. (completed 2026-08-19)
- [x] **Phase 4: Advanced SQL Analytics** - Save CTE, window function, and consecutive deceleration self-join SQL scripts. (completed 2026-08-19)
- [x] **Phase 5: Power BI Visual Dashboard** - Establish database connection, design dashboard layouts, and generate screenshots. (completed 2026-08-19)
- [x] **Phase 6: GenAI Narrative Generation** - Build script using the official google-genai SDK to write stakeholder summaries. (completed 2026-08-19)
- [x] **Phase 7: Packaging & Documentation** - Compile installation requirements, ER diagrams, and complete README. (completed 2026-08-19)

## Phase Details

### Phase 1: Data Ingestion & Local Caching

**Goal**: Fetch 3-5 years of raw quarterly and annual financial statements for 10 SaaS companies and store them locally.
**Mode**: mvp
**Depends on**: Nothing
**Requirements**: EXTR-01, EXTR-02, EXTR-03
**Success Criteria**:

  1. Raw downloaded financial statement JSON files exist under `data/raw/` for all 10 tickers.
  2. yfinance client handles missing tickers and rate-limiting exceptions gracefully.

**Plans**: 2 plans

Plans:

- [x] 01-01: Set up folder structure and install base yfinance dependencies.
- [x] 01-02: Write `extract.py` script and verify it pulls and caches raw statement files.

---

### Phase 2: Data Transformation & Standardization

**Goal**: Standardize dates, map reporting periods to fiscal periods, normalize metric names, and shape the data into a tidy long-format.
**Mode**: mvp
**Depends on**: Phase 1
**Requirements**: TRNS-01, TRNS-02, TRNS-03, TRNS-04
**Success Criteria**:

  1. Transform script processes raw JSON statements and outputs a unified long-format DataFrame (company, period, metric, value).
  2. Metrics mapping dictionary correctly resolves Yahoo's label drift (e.g. "Total Revenue" vs "Revenue").
  3. Transformation run produces stdout logs detailing rows processed, duplicates, and null metrics.

**Plans**: 2 plans

Plans:

- [x] 02-01: Build transformation mappings and metrics standardizer logic.
- [x] 02-02: Write `transform.py` reshaping raw JSON files into structured pandas tidy tables.

---

### Phase 3: SQLite Storage & Schema Setup

**Goal**: Define SQLite tables, database triggers, quarterly view, and load clean data into the database.
**Mode**: mvp
**Depends on**: Phase 2
**Requirements**: LOAD-01, LOAD-02, LOAD-03, LOAD-04
**Success Criteria**:

  1. Relational database `data/financial_health.db` is initialized with foreign keys between `companies`, `date_dim`, and `financials_fact`.
  2. Trigger auto-updates the `last_refreshed` timestamp column upon new inserts.
  3. VIEW joining fact and dimension tables successfully aggregates quarterly records.
  4. Database is successfully populated with transformed data.

**Plans**: 2 plans

Plans:

- [x] 03-01: Write database schema file (`sql/schema.sql`) and verify tables, triggers, and views.
- [x] 03-02: Implement `load.py` database loader script.

---

### Phase 4: Advanced SQL Analytics

**Goal**: Create and save SQL scripts calculating YoY growth, rolling margins, and consecutive deceleration alerts.
**Mode**: mvp
**Depends on**: Phase 3
**Requirements**: ASQL-01, ASQL-02, ASQL-03, ASQL-04
**Success Criteria**:

  1. YoY revenue growth CTE query executes successfully.
  2. Rolling 4-quarter margins window function executes successfully.
  3. Self-join query identifies companies with 2+ consecutive deceleration periods.
  4. Query utilizing the custom VIEW returns correct rows.

**Plans**: 1 plan

Plans:

- [x] 04-01: Create and run `.sql` scripts against the SQLite database.

---

### Phase 5: Power BI Visual Dashboard

**Goal**: Connect Power BI to SQLite database, design dashboard visuals, and generate screenshot previews.
**Mode**: mvp
**Depends on**: Phase 4
**Requirements**: DASH-01, DASH-02, DASH-03
**Success Criteria**:

  1. Power BI connects to the SQLite file.
  2. Trend lines, growth ranking bar chart, and RAG status indicators are designed.
  3. Preview screenshot files are captured and stored.

**Plans**: 2 plans

Plans:

- [x] 05-01: Initialize Power BI file connection and visual structure.
- [x] 05-02: Populate dashboard mockups and screenshots.

---

### Phase 6: GenAI Narrative Generation

**Goal**: Build Python script to query DB alerts, send them to Gemini 2.0 API, and print an executive summary.
**Mode**: mvp
**Depends on**: Phase 4
**Requirements**: GAIL-01, GAIL-02, GAIL-03
**Success Criteria**:

  1. Script queries SQLite database for decelerating growth tickers.
  2. Client initializes using the official `google-genai` SDK and successfully retrieves response.
  3. A 2-3 sentence executive stakeholder summary is printed in plain English.

**Plans**: 1 plan

Plans:

- [x] 06-01: Implement `narrative.py` connecting SQL output to the Gemini model and printing the stakeholder narrative.

---

### Phase 7: Packaging & Documentation

**Goal**: Finalize requirements file, write comprehensive README, and prepare package.
**Mode**: mvp
**Depends on**: Phase 5, Phase 6
**Requirements**: PACK-01, PACK-02
**Success Criteria**:

  1. `requirements.txt` maps all required packages.
  2. `README.md` details architecture flow, ER diagram, running instructions, and screenshots.

**Plans**: 1 plan

Plans:

- [x] 07-01: Finalize README, generate system flow documentation, and verify the end-to-end run sequence.

## Progress

**Execution Order:**
Phases execute in numeric order: 1 → 2 → 3 → 4 → 5 → 6 → 7

| Phase | Plans Complete | Status | Completed |
|-------|----------------|--------|-----------|
| 1. Data Ingestion & Caching | 3/2 | Complete    | 2026-08-19 |
| 2. Data Transformation | 2/1 | Complete    | 2026-08-19 |
| 3. SQLite Storage | 2/1 | Complete    | 2026-08-19 |
| 4. SQL Analytics | 2/1 | Complete    | 2026-08-19 |
| 5. Power BI Dashboard | 2/1 | Complete    | 2026-08-19 |
| 6. GenAI Narrative | 2/1 | Complete    | 2026-08-19 |
| 7. Packaging & Docs | 2/1 | Complete    | 2026-08-19 |
