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
Forge as the human-facing product name. Use `forge-ai-starter-kit` as the
Python distribution name and `forge` as the import-package name.

### Alternatives Considered

- Rename the repository to `forge` and lose the bootcamp sequence.
- Use `001-forge` as both the repository and product name.

### Consequences

- The bootcamp sequence remains visible on GitHub.
- Documentation must distinguish repository identifiers from product names.
- Packaging configuration must explicitly map the distribution to the shorter
  import-package name.

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

Use Black's stable style as the only formatter, with an 88-character line
length. Use Ruff for important pycodestyle errors, Pyflakes, import ordering,
common bug patterns, modern Python upgrades, and Ruff-specific correctness
rules. Both tools infer Python compatibility from `project.requires-python`
and enforce the versions declared in the project environment.

### Alternatives Considered

- Use Ruff for both linting and formatting.
- Use Black plus separate Flake8 and isort tools.

### Consequences

- The required tools remain educationally distinct.
- Formatting ownership stays unambiguous.
- Ruff does not enforce `E501`; Black owns line wrapping and intentionally does
  not rewrite every long string or comment.
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

## Decision 007 — Type-Check Production Source Strictly

- **Status:** Accepted
- **Date:** 2026-08-10

### Context

Forge will introduce typed configuration, logging, errors, and API boundaries.
Permissive type checking would allow partially annotated functions and hidden
`Any` values to weaken those contracts as the codebase grows.

### Decision

Run MyPy 2.3.0 in strict mode against `src` using Python 3.14 semantics. Keep
error codes visible, reject unused configuration, and add exceptions only for
specific evidence-backed incompatibilities.

### Alternatives Considered

- Use MyPy's default permissive settings.
- Enable every `disallow-any-*` option immediately.
- Ignore all missing third-party imports globally.
- Type-check tests before the test harness exists.

### Consequences

- Production functions must have complete type annotations.
- Type errors surface before runtime and before code reaches CI.
- Third-party typing problems require narrow, documented treatment rather than
  global suppression.
- Tests remain outside the current MyPy target unless a later need justifies
  expanding it.

## Decision 008 — Load Typed Settings Without Global State

- **Status:** Accepted
- **Date:** 2026-08-11

### Context

Forge needs validated environment configuration, optional local dotenv
loading, and safe secret representation. A module-level settings instance
would load configuration during import and make tests or alternate runtime
contexts dependent on hidden shared state.

### Decision

Define a Pydantic `BaseSettings` model with a `FORGE_` prefix, typed enums,
boolean parsing, and `SecretStr` for secret values. Load an optional `.env` file
through `load_settings()`, returning a new `Settings` instance on every call.
Let process environment variables take precedence over dotenv values.

### Alternatives Considered

- Construct one settings singleton when the module is imported.
- Read environment variables manually with `os.getenv`.
- Cache the loader globally.
- Require every caller to instantiate `Settings` directly.

### Consequences

- Configuration is validated at a single typed boundary.
- Callers can inject settings explicitly and isolate repeated loads in tests.
- Importing the module has no configuration-loading side effect.
- Each uncached call performs configuration loading again; callers own the
  lifetime of the returned object.
- Secret access remains explicit, and standard representations stay masked.

## Decision 009 — Configure Only the Forge Logger Namespace

- **Status:** Accepted
- **Date:** 2026-08-17

### Context

Forge needs consistent local and machine-readable logs without duplicating
messages when configuration runs more than once. Replacing the process root
logger would also interfere with handlers owned by a host application, test
runner, or server.

### Decision

Bridge Structlog through Python's standard logging system and configure the
named `forge` logger hierarchy. Write to standard output with UTC timestamps
and normalized levels. Select a color-free console renderer for local output
or a JSON renderer for machine processing. Replace Forge's existing handler on
each configuration call and leave the root logger untouched.

### Alternatives Considered

- Configure Structlog with a direct print logger.
- Replace the process root logger and all of its handlers.
- Add a handler on every configuration call.
- Maintain separate processing pipelines for standard-library and structured
  logs.

### Consequences

- Structlog and standard-library records under `forge` share one renderer.
- Repeated configuration does not multiply handlers or messages.
- Host applications retain control over their root and third-party loggers.
- Forge modules must use logger names in the `forge` hierarchy.
- Uvicorn and other framework logging remain separate until an application
  boundary explicitly integrates them.
