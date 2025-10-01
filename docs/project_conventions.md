# Contributing Guidelines

Thanks for contributing! This document explains how we structure the project, organize issues, and use labels.

---

## 🏗️ Project Structure

We use a three-level hierarchy inspired by Agile:

- **Epic (Milestone)** → Large, time-bounded outcomes (e.g., `MVP-EO v0.1`).
- **Story (Target field in issue templates)** → Concrete deliverables that make up an Epic.
- **Issue** → The smallest actionable work item (task, bug, doc update, chore, etc.).

**Example**

``` 
    Epic (Milestone): MVP-EO v0.1
    ├─ Story (Target): Parser & Normalizer
    │  ├─ Issue: Define EO dataclass schema
    │  ├─ Issue: Add type hints & defaults
    │  └─ Issue: Write unit tests for schema
    └─ Story (Target): Storage Layer
    ├─ Issue: Create SQLite schema
    └─ Issue: Insert parsed records
```

---

## 📝 Issues

- Use the **issue templates** under “New Issue.”
- Every issue should have:
  - **Target (Story)** → select the deliverable or use `generic`.
  - **Priority** → Critical, High, Medium, Low, or Deferred.
- Add **at most 1 Planning label** and **1 Execution label**.
- Break large issues into **child issues** for better visibility.

---

## 🏷️ Labels

We divide labels into **Planning** and **Execution**.

### Planning (cool tones)
- `documentation` → `#1f77b4`
- `research / spike` → `#9467bd`
- `chore` → `#7f7f7f`
- `task (planning)` → `#17becf`

### Execution (warm tones)
- `bug` → `#d62728`
- `blocked` → `#ff9896`
- `enhancement / feature` → `#ff7f0e`
- `task (execution)` → `#2ca02c`

---

## 🔺 Priorities

We replace vague P0/P1 with clear words:

1. **Critical** → must be fixed immediately; blocks progress.  
2. **High** → needed for current iteration.  
3. **Medium** → useful, but can wait.  
4. **Low** → nice-to-have, cosmetic.  
5. **Deferred** → explicitly out of near-term scope.  

---

## 🎯 Targets

The **Target field** in issue templates maps to *Stories*.  
Examples:
- `Data Fetching Layer`  
- `Parser & Normalizer`  
- `Storage Layer`  
- `Docs`  
- `MVP-EO v0.1 (generic)` → catch-all for cross-cutting or ambiguous tasks  

---

## ⚖️ Workflow Guidelines

- Not every issue belongs to a Milestone/Epic — that’s fine.  
- Every issue **should** have a Target (Story), even if `generic`.  
- Labels are standardized — avoid creating new ones without discussion.  
- Review labels and milestones quarterly to prevent bloat.  

---

✅ With this structure, every issue is clear, trackable, and connected to the project’s larger goals.  
