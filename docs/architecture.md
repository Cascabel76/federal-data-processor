# Repository Docs — Ready to Commit

Below are two Markdown files formatted exactly as they should live in your repo. Copy each section into the corresponding path.

---

## `docs/architecture.md`

# Federal Data Processor — Architecture Overview

**Purpose:** A concise map of where to write code and how components interact. This document is source‑agnostic and applies to all data sources you add over time.

---

## 1) Top‑Level Layout

```
federal-data-processor/
├── pyproject.toml          # deps + tooling (ruff/black/mypy)
├── README.md               # one-page overview + quickstart
├── .env.example            # documented env vars
├── .gitignore
├── docs/                   # architecture & runbooks
├── scripts/                # dev helpers (no business logic)
└── src/
    └── fdp/
        ├── app.py          # SINGLE flow control point
        ├── cli/            # thin CLI that calls app.py
        ├── core/           # source-agnostic primitives
        ├── ingest/         # per-source adapters (e.g., Federal Register)
        ├── pipelines/      # declarative pipelines (wiring only)
        ├── orchestration/  # scheduler + runner concerns
        └── telemetry/      # metrics/events
```

---

## 2) Component Responsibilities (What goes where)

### `src/fdp/app.py` — Control Switchboard

* **Does:** load config, init logging, open resources (db/state), run a pipeline by ID via `pipelines.registry`.
* **Doesn’t:** contain business logic for fetching/parsing/persistence.

### `src/fdp/cli/`

* **Does:** parse CLI options and call `app.run(pipeline_id, params)`.
* **Doesn’t:** duplicate `app.py` logic; remains a thin wrapper.

### `src/fdp/core/` (shared, source‑agnostic)

* `config/` — env/settings → typed objects.
* `logging/` — one place to configure logging.
* `io/` — filesystem/object storage utils (local now; S3/minio later).
* `net/` — HTTP session builder, retries, backoff, rate limiting (**canonical**).
* `db/` — repository interfaces + migrations (SQLite→Postgres here).
* `models/` — canonical domain models (EO, Rule, Notice, etc.).
* `dq/` — generic validators (required fields, timestamp sanity, dups).
* `state/` — checkpoint/cursor store (keys are namespaced: `fr.*`).

### `src/fdp/ingest/<source>/` (source‑specific; example: `federal_register`)

* `client/` — thin API wrappers returning raw JSON, using `core/net`.
* `fetcher/` — decides **what** to read next using `core/state` + `client`.
* `parse/` — raw → `core/models/*` mapping only.
* `dq/` — source‑specific data‑quality checks.
* `tests/` — fixtures and tests close to the source.

### `src/fdp/pipelines/`

* `registry.py` — the **only** map: pipeline_id → factory/function.
* `<source>/` — e.g., `federal_register/daily_ingest.py`, `backfill.py`.
* **Pipelines do:** compose steps: state → fetcher → parse → dq → db → state.
* **Pipelines don’t:** embed HTTP, SQL, or source API shapes.

### `src/fdp/orchestration/`

* `runner/` — executes pipeline with retries, metrics, failure handling.
* `scheduler/` — cron/APS definitions that just call `app.run(...)`.

### `src/fdp/telemetry/`

* **Does:** counters, timings, events (wire from `app` + `runner`).

---

## 3) Interaction Diagram (Conceptual)

```
CLI / Scheduler
      │
      ▼
  app.py  ──► core/config + core/logging + core/db + core/state
      │
      ▼
pipelines.registry ──► build(pipeline_id, params)
      │
      ▼
Pipeline (wiring only)
  1) state.read()       ─► core/state
  2) fetcher.run()      ─► ingest/<source>/{client,fetcher}
  3) parse.map()        ─► ingest/<source>/parse
  4) dq.check()         ─► core/dq + ingest/<source>/dq
  5) repos.save()       ─► core/db (repositories)
  6) state.commit()     ─► core/state
```

---

## 4) Golden Rules (Boundaries)

1. **One entry:** all executions go through `app.py`.
2. **One registry:** `pipelines/registry.py` is canonical.
3. **HTTP only in `core/net`** (no ad‑hoc retry loops in clients).
4. **Models only in `core/models`** (never duplicated under `ingest/`).
5. **Persistence only via `core/db`** repositories (no “writers/” folders).
6. **State only via `core/state`**, keys namespaced per source (`fr.*`).

---

## 5) Env/Config Keys (Document in `.env.example`)

* `FR_BASE_URL`, `FR_PAGE_SIZE`, `FR_USER_AGENT`
* `DEFAULT_LOOKBACK_HOURS`
* `HTTP_MAX_RETRIES`, `HTTP_BACKOFF_BASE_MS`, `RATE_LIMIT_RPS`
* `DB_URL`, `DB_SCHEMA`
* `LOG_LEVEL`

---

## 6) First‑Run Checklist

1. Register pipeline IDs in `pipelines/registry.py`.
2. Add state keys in `core/state` (e.g., `fr.last_modified_cursor`).
3. Implement `ingest/<source>/client` using `core/net` session builder.
4. Implement `ingest/<source>/fetcher` to compute windows/cursors.
5. Implement `ingest/<source>/parse` to produce `core/models` objects.
6. Wire the pipeline (`daily_ingest.py`) to compose steps and call `core/db` repos.
7. Initialize logging/config in `app.py`; ensure CLI calls `app.run(...)`.

---

## 7) Naming & Import Hygiene

* Modules use nouns for packages (`parse`, `client`, `runner`); verbs for functions.
* Use absolute imports: `from fdp.core.db import Repos`; avoid `..` up‑walks.
* Config keys: flat, namespaced (`FR_*`, `HTTP_*`, `DB_*`).

---

## 8) Future Extensions

* Add new sources under `ingest/<new_source>/` and `pipelines/<new_source>/`.
* Swap SQLite→Postgres entirely within `core/db` (pipelines unchanged).
* Extend telemetry to OpenTelemetry exporters when needed.

---