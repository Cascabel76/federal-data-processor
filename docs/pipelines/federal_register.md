## `docs/pipelines/federal_register.md`

# Federal Register Pipeline — Ingestion & Backfill

**Scope:** Ingest rules/notices/EO entries from the Federal Register API, map to canonical models, and persist via `core/db`. This document is specific to the Federal Register source.

---

## 1) Pipelines & IDs

* `federal_register.daily_ingest` — Incremental ingest using `last_modified` cursor.
* `federal_register.backfill` — Historical windowed ingest over a fixed date range.

> **Invocation:** All runs go through `app.run(pipeline_id, params)` (via CLI or scheduler).

---

## 2) Data Flow (Steps)

1. **Read Cursor** — `core/state.get("fr.last_modified_cursor")`.
2. **Fetch** — `ingest/federal_register/fetcher` computes window and calls `client` to page API.
3. **Parse** — `ingest/federal_register/parse` maps raw payloads → `core/models` (EO, Notice, Rule).
4. **Validate** — `core/dq` (generic) + `ingest/federal_register/dq` (FR‑specific) checks.
5. **Persist** — `core/db` repositories upsert records + related tables.
6. **Commit Cursor** — `core/state.set("fr.last_modified_cursor", new_value)`.

---

## 3) Ownership & Boundaries

* **HTTP behavior:** `core/net` only. FR `client` must not re‑implement retries/backoff.
* **Models:** `core/models` is the single source of truth.
* **DB access:** only through `core/db` repositories.
* **State:** cursors are namespaced under `fr.*` in `core/state`.

---

## 4) Inputs & Outputs

**Inputs**

* Federal Register API (base: `FR_BASE_URL`) filtered by `last_modified` or date range.
* Pipeline params (e.g., `since`, `until`, `batch_size`).
* Existing state cursor (`fr.last_modified_cursor`).

**Outputs**

* Canonical records persisted to DB.
* Updated state cursor.
* Telemetry counters (fetched, parsed, validated, persisted, skipped).

---

## 5) Environment & Config

* `FR_BASE_URL` (e.g., official API base)
* `FR_PAGE_SIZE` (default page size)
* `FR_USER_AGENT` (contact string per API TOS)
* `DEFAULT_LOOKBACK_HOURS` (used when no cursor yet)
* `HTTP_MAX_RETRIES`, `HTTP_BACKOFF_BASE_MS`, `RATE_LIMIT_RPS`
* `DB_URL`, `DB_SCHEMA`, `LOG_LEVEL`

> Document actual values in `.env.example` and keep secrets out of VCS.

---

## 6) State & Idempotency

* **State keys**

  * `fr.last_modified_cursor` — latest `last_modified` timestamp successfully committed.
  * `fr.last_successful_run` — ISO timestamp for observability.
  * Optional: `fr.content_hash_ledger` — prevent dupes across amendments.

* **Idempotency rules**

  * Upserts on stable identifiers (e.g., FR document number).
  * If `last_modified` moves backward (rare), skip/queue for re‑validation.

---

## 7) Error Handling & Retries

* **HTTP** — centralized in `core/net` with exponential backoff; client surfaces typed errors.
* **Parsing** — drop to quarantine queue (separate table) with raw payload + reason.
* **DB** — wrap upserts in transactions; on failure, retry N times then move to DLQ.
* **Pipeline** — runner enforces max attempts; emits failure event and exits non‑zero.

---

## 8) Scheduling & SLAs

* **Daily ingest**: every hour by default (adjustable in scheduler). Target freshness: ≤ 2h.
* **Backfill**: ad‑hoc; chunk by day/week. No freshness SLA; prioritize steady throughput.

---

## 9) Edge Cases (FR‑Specific)

* **Amended/Withdrawn documents** — treat as updates to existing records; rely on `last_modified` and stable IDs.
* **Large pages/pagination** — enforce `FR_PAGE_SIZE` and respect API caps.
* **Time zone drift** — normalize all timestamps to UTC in `core/models`.
* **Partial outages** — runner retries; if persistent, halt and alert.

---

## 10) Metrics & Observability

* **Counters**: `fr.fetched`, `fr.parsed`, `fr.validated`, `fr.persisted`, `fr.skipped`, `fr.quarantined`.
* **Latency**: `fr.http_ms_per_page`, `fr.parse_ms_per_record`, `fr.db_ms_per_batch`.
* **State**: `fr.cursor_timestamp`, `fr.lag_minutes` (now − cursor).

---

## 11) Data Contracts (Canonical Fields)

**Common fields across EO/Notice/Rule**

* `doc_id` (stable id), `title`, `type`, `abstract`, `agencies[]`, `topics[]`,
* `publication_date`, `effective_date?`, `last_modified`, `html_url`, `pdf_url?`,
* `docket_id?`, `comment_url?`, `supporting_docs[]`.

> Keep the canonical schema in `core/models/`; this section mirrors that for quick reference.

---

## 12) Parameters (Pipeline Runtime)

* `since` / `until` — ISO8601 timestamps; default `since` = cursor or `now-DEFAULT_LOOKBACK_HOURS`.
* `batch_size` — records per DB write batch.
* `max_pages` — safety cap during exploratory runs.
* `backfill_window` — for `backfill` pipeline (e.g., `P7D` or explicit dates).

---

## 13) Backfill Procedure (Operator Runbook)

1. Choose historical range (e.g., 2010-01-01 → 2015-12-31).
2. Run `federal_register.backfill` with a daily/weekly chunk size.
3. Monitor metrics; if `quarantined > 0`, inspect and add parser rules.
4. After completion, set `fr.last_modified_cursor` to the max `last_modified` in DB.

---

## 14) Testing Strategy

* **Unit tests**: client pagination, fetcher windowing math, parser field mapping, dq rules.
* **Integration tests**: end‑to‑end pipeline using local fixtures and temp DB.
* **Contract tests**: validate API shape assumptions against sampled live payloads.

---

## 15) Glossary

* **Cursor** — a durable pointer (timestamp or ID) marking progress through the source.
* **Idempotent upsert** — safe repeatable writes keyed by stable identifiers.
* **DLQ (dead‑letter queue)** — storage for failed records pending manual or automated reprocess.

---