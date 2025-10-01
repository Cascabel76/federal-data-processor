# Federal Data Processor — Programming Rules & Conventions

This document captures the rules and conventions we’ve been developing together for clarity, specificity, and maintainability.

---

## 1. Naming & Specificity

* **Name files and classes by domain concept, not by technology.**

  * ✅ `document.py` → contains `Document`
  * ✅ `agency.py` → contains `Agency`
  * ❌ `types.py` or `utils.py` → too vague
* **Module names should let a newcomer guess contents instantly.**
* **Classes reflect real-world referents** (e.g., `FederalRegisterDocument`) instead of abstract “essences.”

---

## 2. Module Responsibilities

* **One responsibility per module.** If a file changes for two different reasons, split it.
* If two files are always changed together, merge them.
* **Write a docstring at the top** of every file explaining:

  * Scope (what it defines)
  * Non-goals (what it is not)

---

## 3. Abstraction Guardrails

* **Defer universal abstractions.**

  * Start with source-specific models (e.g., `FederalRegisterDocument`).
  * Extract minimal cross-source models (e.g., a base `Document`) *only* when multiple sources exist.
* **Be explicit about provenance.** Record what source produced a record, when it was ingested, and any official/legal status.
* **Prefer composition over inheritance.**

  * Don’t force everything into a deep class hierarchy.
  * Add related data via composition (`provenance`, `attachments`, etc.).

---

## 4. Contracts & Models

* **Contracts first.** Write down expected fields (data contracts) before building classes.
* **Optional vs required fields:** Use `Optional[...]` for values that aren’t guaranteed (e.g., `effective_date`, `pdf_url`).
* **Enums:**

  * Capture allowed values (e.g., `DocType`).
  * Parsers map raw source strings → enums.
* **Canonical models live in `core/models/`.**

  * Source-specific raw schemas + mappings live in `models/<source>/`.

---

## 5. File & Folder Structure

* **Canonical, source-agnostic:** `src/fdp/core/models/`

  * `document.py`, `agency.py`, `topic.py`, `attachment.py`
* **Source-specific:** `src/fdp/models/<source>/`

  * `document.py`, `enums.py`, `mappings.py`, `constants.py`
  * Always include a README.md explaining what belongs there

---

## 6. Programming Practices

* **Idempotency:** Upserts keyed by stable IDs (e.g., FR `document_number`).
* **Normalization:** Timestamps stored in UTC; enums normalized from raw.
* **Provenance:** Always capture source URLs, retrieval timestamps, and hashes for traceability.
* **Field hashes:** Use `raw_hash` to detect no-op updates.

---

## 7. Review Checklist

Before adding a new module or class, ask:

* Can I explain this file’s purpose in one sentence?
* Would a newcomer guess the contents from the name alone?
* Does this module change for one reason only?
* Am I adding a universal abstraction too early?
* Is there a docstring explaining scope and non-goals?

---

## 8. Philosophy

* **Expel vagueness:** Specificity aids clarity and reduces onboarding friction.
* **Stay pragmatic:** Don’t over-fragment into dozens of micro-files.
* **Abstractions emerge from reality, not ideals.** Build what the data requires, not what Aristotelian forms suggest.
