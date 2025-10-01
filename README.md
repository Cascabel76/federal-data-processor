# Federal Data Processor (FDP)

A modular ETL platform for ingesting, normalizing, and querying U.S. federal public data (starting with the Federal Register). The repo emphasizes clear boundaries, testability, and source-agnostic core utilities so we can add new data sources without rework.
---
https://github.com/users/Cascabel76/projects/9
---

## Quickstart

### 1) Environment

Copy the template and configure secrets locally.

```
cp .env.example .env
# Edit .env
```

### 2) Install

* Requires Python 3.11+
* Managed with `uv`/`pipx`/`pip` (your choice)

```
# Example with pip
pip install -e .
```

### 3) First run (pipeline via CLI)

All executions go through `fdp.app` and the pipeline registry.

```
# Example (names only; see docs for real params)
fdp run --pipeline federal_register.daily_ingest --since 24h
```

> For more details, see `docs/pipelines/federal_register.md`.

---

## Repository Layout

```
src/fdp/
  app.py          # single orchestration entrypoint
  cli/            # thin CLI that calls app.py
  core/           # source-agnostic: config, logging, net, db, models, dq, state
  ingest/         # per-source adapters (e.g., federal_register/*)
  pipelines/      # declarative pipelines (wiring only), plus registry
  orchestration/  # scheduler + runner
  telemetry/      # metrics/events
```

* Full explanation in `docs/architecture.md`.

---

## Development Guidelines

* **One entrypoint**: all runs through `app.py`.
* **One registry**: `pipelines/registry.py`.
* **No direct I/O in sources**: source adapters use `core/net`, `core/db`, `core/state`.
* **Canonical models** in `core/models`; never redefine under `ingest/`.
* **Idempotent writes** via repositories; design for safe re-runs.

---

## Configuration

Documented in `.env.example` and consumed via `core/config/`.

Key variables:

* `FR_BASE_URL`, `FR_PAGE_SIZE`, `FR_USER_AGENT`
* `DEFAULT_LOOKBACK_HOURS`
* `HTTP_MAX_RETRIES`, `HTTP_BACKOFF_BASE_MS`, `RATE_LIMIT_RPS`
* `DB_URL`, `DB_SCHEMA`, `LOG_LEVEL`

---

## Docs

* Architecture: `docs/architecture.md`
* Federal Register pipeline: `docs/pipelines/federal_register.md`
* Ops runbook: `docs/ops/runbook.md`

---

## Roadmap

* ✅ Define architecture, pipeline IDs, and boundaries
* 🔜 Federal Register ETL (daily + backfill)
* 🔜 Frontend HTML client (read-only browsing of ingested data)
* 🔜 Additional sources (NOAA, etc.)

---

## License

TBD
