# Architecture Decision Record

This document records decisions that materially affect Forge's architecture,
tooling, security, maintainability, or workflow. Each record explains the
context, alternatives, decision, and consequences.

## Decision 001 — Separate the Repository Identifier from the Product Name

- **Status:** Accepted
- **Date:** 2026-08-08

### Context

The bootcamp uses numbered repository names, while the project brief names the
starter kit Forge.

### Decision

Use `cade-ai-engineering-bootcamp/001-forge` as the repository identifier and
Forge as the human-facing product name.

### Alternatives Considered

- Rename the repository to `forge` and lose the bootcamp sequence.
- Use `001-forge` as both the repository and product name.

### Consequences

- The bootcamp sequence remains visible on GitHub.
- Documentation must distinguish repository identifiers from product names.
- Python distribution and import-package names are separate decisions.

## Decision 002 — Use a Small Modular Monolith

- **Status:** Accepted
- **Date:** 2026-08-08

### Context

Forge must demonstrate professional boundaries without becoming a framework or
distributed system. Future AI projects need reusable infrastructure, not
premature service decomposition.

### Decision

Organize Forge as one installable Python package with focused modules for
configuration, logging, errors, and the HTTP boundary.

### Alternatives Considered

- Multiple services or repositories
- A plugin architecture
- A single script with no internal boundaries

### Consequences

- The architecture remains easy to understand, test, and extend.
- Modules can evolve independently without network boundaries.
- A future project may extract a service only when real operational needs
  justify it.

## Decision 003 — Use uv and a Locked Python 3.14 Environment

- **Status:** Accepted
- **Date:** 2026-08-08

### Context

The project needs reproducible Python installation, dependency resolution,
virtual-environment management, and command execution across local and CI
environments.

### Decision

Use uv 0.12.3, Python 3.14.7, compatible dependency constraints in
`pyproject.toml`, and exact resolutions in `uv.lock`.

### Alternatives Considered

- `venv` plus `pip` and manually maintained requirements files
- Poetry
- Conda
- Installing project tools globally

### Consequences

- One tool manages Python, `.venv`, dependency resolution, locking, and command
  execution.
- `uv sync --frozen` can detect lockfile drift.
- Contributors must install a compatible uv version.
- Version upgrades must deliberately update both metadata and the lockfile.

## Decision 004 — Separate Application Errors from FastAPI

- **Status:** Accepted
- **Date:** 2026-08-08

### Context

Central error handling is required, but coupling every application error to an
HTTP status would make the foundation harder to reuse from workers, command-line
tools, or scheduled jobs.

### Decision

Define framework-independent application errors and translate them into safe
HTTP responses only at the FastAPI boundary.

### Alternatives Considered

- Raise FastAPI `HTTPException` throughout the application.
- Catch every exception independently in each endpoint.

### Consequences

- Domain and infrastructure modules remain independent of HTTP.
- The API adapter owns status-code and response-shape decisions.
- Tests must cover both error behavior and HTTP translation.

## Decision 005 — Give Ruff and Black Different Responsibilities

- **Status:** Accepted
- **Date:** 2026-08-08

### Context

Ruff can format Python, making Black technically redundant, but both tools are
part of the required project stack.

### Decision

Use Ruff for linting and import rules and Black for formatting. Configure both
with compatible line-length, target-version, and exclusion settings.

### Alternatives Considered

- Use Ruff for both linting and formatting.
- Use Black plus separate Flake8 and isort tools.

### Consequences

- The required tools remain educationally distinct.
- Formatting ownership stays unambiguous.
- Configuration tests and CI must prevent the tools from disagreeing.

## Decision 006 — Enforce Feature-Level Scope Control

- **Status:** Accepted
- **Date:** 2026-08-08

### Context

Forge includes many adjacent opportunities for automation and polish. Allowing
those ideas into an active feature would weaken reviewability and learning.

### Decision

Implement one explicitly approved feature at a time. Record adjacent ideas as
future work, update the agenda after completion, and stop at the declared
boundary even when time remains.

### Alternatives Considered

- Complete entire steps in one uninterrupted change.
- Add related improvements whenever they are discovered.

### Consequences

- Diffs remain focused and easier to understand.
- Each design decision receives deliberate review.
- Progress may feel slower, but comprehension and maintainability improve.

