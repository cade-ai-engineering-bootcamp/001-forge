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

## Decision 010 — Redact Sensitive Log Fields Before Rendering

- **Status:** Accepted
- **Date:** 2026-08-17

### Context

Context makes logs more useful, but arbitrary structured data can contain
credentials. Separate redaction behavior for each renderer or logging API would
create gaps, while scanning values cannot reliably distinguish secrets from
ordinary text.

### Decision

Merge async-safe context variables into each event and apply one recursive,
key-based redaction processor before human-readable or JSON rendering. Match a
documented set of case-insensitive field names and suffixes after normalizing
hyphens to underscores. Apply the same processor to Structlog records and
standard-library `extra` fields.

### Alternatives Considered

- Scan values using credential-like patterns.
- Redact only top-level fields.
- Maintain separate policies for each renderer.
- Depend entirely on callers to mask sensitive fields.
- Remove every field containing the word `token`, including safe metrics such
  as `token_count`.

### Consequences

- Named sensitive fields are masked consistently in supported nested data.
- Async tasks can bind context without sharing one mutable global dictionary.
- Safe fields that do not match the explicit policy remain useful.
- Secrets embedded in free-form messages cannot be detected reliably and are
  prohibited by documented usage rules.
- New credential field names must be added deliberately as the system evolves.

## Decision 011 — Separate Fixed Public Errors from Internal Diagnostics

- **Status:** Accepted
- **Date:** 2026-08-17

### Context

Callers need stable error codes and safe messages, while developers need enough
information to diagnose failures. Allowing arbitrary exception messages to
cross a system boundary can reveal implementation details, and adding HTTP
metadata would couple reusable application errors to one adapter.

### Decision

Define a framework-independent `ApplicationError` hierarchy with class-level
codes and fixed public messages. Store optional internal diagnostics separately
from the exception arguments, expose only code and public message through
`to_public_dict()`, and use Python exception chaining to retain low-level
causes. Leave HTTP translation to the API boundary.

### Alternatives Considered

- Return raw exception messages to callers.
- Put HTTP status codes on application exceptions.
- Accept a caller-provided public message for every error instance.
- Discard internal diagnostics and original causes.
- Create unrelated exception classes with no shared base contract.

### Consequences

- Callers can depend on stable, machine-readable codes.
- Normal strings, representations, and public dictionaries omit internal
  diagnostics.
- Workers, command-line tools, and HTTP services can reuse the same errors.
- Trusted code must treat `internal_detail` as diagnostic-only and keep it free
  of credentials.
- Framework adapters must explicitly map error types to their own transport
  semantics.

## Decision 012 — Separate Application Construction from the Runtime Module

- **Status:** Accepted
- **Date:** 2026-08-18

### Context

Forge needs one conventional ASGI object for Uvicorn while keeping application
construction testable. Loading settings and building the application only in a
module-level block would make alternate runtime contexts depend on hidden
process state.

### Decision

Create the FastAPI application in an injectable `create_app()` factory. Let the
factory accept an existing `Settings` instance or load a fresh one, configure
Forge logging, attach the resolved settings to application state, and create
the application with package-derived metadata and debug mode disabled. Keep
`forge.main` as a thin runtime module that exposes `app = create_app()`.

### Alternatives Considered

- Construct the application and load settings entirely at module import.
- Require Uvicorn's factory mode for every runtime invocation.
- Store one global settings singleton for both tests and runtime startup.
- Add routes and exception handlers during initial application construction.

### Consequences

- Uvicorn has one documented `forge.main:app` entry point.
- Tests and alternate runtimes can inject validated settings explicitly.
- Normal runtime import intentionally performs startup composition once.
- Application settings are available to later boundary components through
  `app.state.settings`.
- Routes and error translation remain independently reviewable features.

## Decision 013 — Translate Errors Only at the HTTP Boundary

- **Status:** Accepted
- **Date:** 2026-08-18

### Context

Forge's application errors deliberately contain no HTTP metadata, but API
clients still need meaningful status codes and safe response bodies. Framework
defaults for unexpected exceptions also do not provide Forge's stable JSON
error shape.

### Decision

Register exception handlers on each factory-created FastAPI application. Map
known application error categories to explicit HTTP status codes while using
their existing public dictionaries as response content. Map a base or unmapped
`ApplicationError` to HTTP 500. Return a fixed `internal_server_error` payload
for every unexpected exception without including exception text or traceback
data. Leave FastAPI's built-in validation and HTTP exception handling intact.

### Alternatives Considered

- Add HTTP status codes directly to application exceptions.
- Return raw exception strings from a catch-all handler.
- Depend entirely on FastAPI's default plain-text 500 response.
- Customize every framework validation and HTTP exception response.
- Add test-only production routes for triggering error behavior.

### Consequences

- Application errors remain reusable by non-HTTP runtimes.
- API clients receive stable JSON codes, messages, and status semantics.
- Internal diagnostics and unexpected exception details stay out of responses.
- New application error categories require an explicit adapter mapping.
- Integration tests create failing routes only on their local application
  instances; the production application still exposes only `/health`.

## Decision 014 — Build a Minimal Non-Root Runtime Image

- **Status:** Accepted
- **Date:** 2026-09-27

### Context

Forge needs a repeatable container artifact without copying the development
repository, build tools, or credentials into production. Dependency changes
should not invalidate source-independent layers, and the service must not run
with root privileges.

### Decision

Use an allowlisted Docker build context and a multi-stage Dockerfile. Build
against `python:3.14.7-slim-bookworm`, obtain uv 0.12.3 from its official image,
install frozen runtime dependencies before copying source, and install Forge
non-editably. Copy only the completed virtual environment into a fresh Python
runtime stage. Run Uvicorn as fixed UID and GID 10001, use exec-form startup,
and implement the image health check with Python's standard library.

### Alternatives Considered

- Copy the entire repository and exclude files individually.
- Install development dependencies in the runtime image.
- Run Uvicorn as the image's default root user.
- Install curl only for the health check.
- Copy uv and application source into the runtime stage.
- Use a single-stage Dockerfile.

### Consequences

- Secrets and development-only files are denied from the build context by
  default.
- Dependency installation remains cached when only Forge source changes.
- The final image contains neither uv nor the source repository layout.
- Runtime configuration remains external to the immutable image.
- The health check adds no operating-system package.
- Base-image and uv tags must be updated deliberately during maintenance.

## Decision 015 — Keep Local Compose Execution Immutable and Least-Privilege

- **Status:** Accepted
- **Date:** 2026-09-27

### Context

Local orchestration should make the secure image easy to operate without
quietly replacing its runtime model with source mounts, root access, or broad
host exposure. Developers also need predictable defaults and a clean lifecycle.

### Decision

Define one Compose service that builds the Dockerfile's runtime stage, binds
port 8000 only to the local host, and inherits the image health check. Supply
development-safe settings with shell and local dotenv overrides for non-secret
values. Reinforce UID and GID 10001, drop all Linux capabilities, prevent
privilege escalation, make the root filesystem read-only, and provide only an
ephemeral `/tmp` filesystem. Do not mount source or pass an API key.

### Alternatives Considered

- Publish the service on every host interface.
- Bind-mount source and run Uvicorn with reload enabled.
- Run Compose with the image's root default.
- Give the container its normal Linux capability set.
- Make the entire container filesystem writable.
- Pass every local dotenv value into the container automatically.

### Consequences

- One command builds, starts, and waits for a healthy local service.
- Local access remains available without exposing the port to the network.
- Compose cannot modify packaged application files.
- Non-secret settings can vary without rebuilding the image.
- Source-editing workflows require a rebuild instead of live reload.
- Secret delivery remains an explicit future-project responsibility.

## Decision 016 — Run CI with Least Privilege and Immutable Action References

- **Status:** Accepted
- **Date:** 2026-10-02

### Context

GitHub Actions workflows execute code from the repository and from reusable
third-party actions. Broad token permissions or mutable action tags would let a
routine quality workflow perform unnecessary repository mutations or silently
receive different action code in a later run.

### Decision

Run CI for pull requests targeting `main` and pushes to `main` on the fixed
`ubuntu-24.04` runner. Grant the workflow only read access to repository
contents. Pin every external action to a full commit SHA, retain the release
tag in a comment for maintainability, and disable persisted checkout
credentials. Bound jobs with a timeout and cancel superseded runs for the same
workflow and Git reference.

### Alternatives Considered

- Rely on GitHub's default workflow permissions.
- Grant write permissions in case they are useful later.
- Reference actions by a moving major-version tag.
- Allow checkout to persist the GitHub token in Git configuration.
- Run every historical commit even after a newer one supersedes it.

### Consequences

- CI can read the repository but cannot modify its contents.
- Reviewed action code cannot change until its pinned SHA is updated.
- Release comments make pinned actions understandable to maintainers.
- Future actions must declare and justify any additional permissions.
- Action upgrades require an explicit review and SHA change.
- Superseded work is canceled and stalled jobs cannot run indefinitely.
