# Project Journal

This journal records each focused work session, the work completed, decisions
made, blockers encountered, and the exact place where the next session should
begin.

## 2026-08-08 — Step 0: Planning and Governance

### Session Goal

Establish the project scope, repository, reproducible Python environment, and
living governance documentation without beginning application implementation.

### Features Completed

- Feature 0.1 — Approved the project scope, architecture, stack, and agenda.
- Feature 0.2 — Bootstrapped and verified the reproducible Python environment.
- Feature 0.3 — Created the complete project agenda and scope guardrails.
- Feature 0.4 — Initialized the project journal, decision record, and learning
  record.

### Work Completed

- Created the public `cade-ai-engineering-bootcamp/001-forge` repository.
- Connected the local repository to GitHub on the `main` branch.
- Installed uv 0.12.3 and uv-managed Python 3.14.7.
- Declared the approved runtime and development dependencies.
- Generated `uv.lock` and created the ignored `.venv` environment.
- Verified frozen synchronization and all direct dependency versions.
- Created the 31-feature project agenda with explicit scope boundaries.
- Established the initial decision and learning records.

### Decisions Made

- Use a small modular-monolith architecture.
- Keep the bootcamp repository name `001-forge` and the product name Forge.
- Use uv as the single Python environment and dependency-management workflow.
- Keep application errors independent of FastAPI.
- Use Ruff for linting and Black for formatting.
- Enforce one approved feature at a time with a mandatory hard stop.

See `docs/DECISIONS.md` for the context and consequences of these decisions.

### Validation Performed

- Confirmed Python 3.14.7 in the managed environment.
- Confirmed uv 0.12.3.
- Confirmed the exact approved direct dependency versions.
- Confirmed `.venv` is ignored by Git.
- Confirmed the lockfile supports frozen offline synchronization.
- Confirmed the agenda contains 31 features across 10 steps.
- Confirmed the repository is synchronized with `origin/main` before Feature
  0.4 began.

### Blockers and Limitations

- Docker is not installed. It is intentionally deferred until Step 6.
- The VS Code `code` shell command is not on `PATH`; this does not block the
  project.
- The Python package does not exist yet and project packaging remains disabled
  until Feature 1.2.
- No application tests exist because application code has not begun.

### Next Starting Point

Begin Feature 1.1 — Add licensing, changelog, initial README, and repository
hygiene. Do not begin Feature 1.2 in the same scope unless it is separately
approved.

## 2026-08-09 — Feature 1.1: Repository Foundation

### Session Goal

Establish the repository's public-facing metadata and hygiene without creating
the Python package scheduled for Feature 1.2.

### Feature Completed

- Feature 1.1 — Added licensing, changelog, initial README, and repository
  hygiene.

### Work Completed

- Added the standard MIT license with the project owner's copyright.
- Added an unreleased changelog that records the foundation built so far.
- Documented Forge's purpose, boundaries, prerequisites, reproducible setup,
  current repository layout, project records, and development status.
- Added narrow ignore rules for local editor files and runtime logs.
- Kept future package, quality, API, container, and CI capabilities clearly
  identified as planned rather than available.

### Validation Performed

- Re-synchronized the environment from the unchanged lockfile using frozen
  mode.
- Confirmed the managed environment still uses Python 3.14.7.
- Confirmed local environments, secrets, logs, and editor artifacts are
  ignored while `.env.example` remains trackable.
- Confirmed the patch has no whitespace errors.

### Scope Notes

- No Python source package or packaging configuration was introduced.
- No dependency declarations or resolved versions were changed.
- No work from Feature 1.2 or later was started.

### Next Starting Point

Begin Feature 1.2 — Create the minimal `src/forge` package and enable project
packaging. Do not begin it without separate approval.
