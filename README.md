# Federal Data Processor — MVP (EO → ETL → SQLite → CLI)

**Goal (v0.1):** Pull a small set of Executive Orders, parse them, load into SQLite, and expose a CLI for search/export.

## Project Board
We use a GitHub **Project (Board view)** with columns: Icebox, Backlog, Ready, In Progress, In Review, Verify/QA, Done, Blocked.
Definitions of Ready/Done live in `docs/process.md`.

## Quickstart
```bash
make setup    # install dev deps
make test     # run unit + integration (fixtures)
make run      # run CLI help
