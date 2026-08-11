# Project 001 — Forge Agenda

## Project Purpose

Forge is a reusable, production-quality Python engineering starter kit for
future AI systems. It provides a professional foundation for packaging,
configuration, logging, error handling, testing, containers, continuous
integration, and technical documentation without introducing application-
specific AI or business logic.

## Project Status

- **Repository:** `cade-ai-engineering-bootcamp/001-forge`
- **Visibility:** Public
- **Default branch:** `main`
- **Estimated duration:** 1 week
- **Estimated focused time:** 11–12 hours
- **Estimated work sessions:** 6–7
- **Overall progress:** 35% (11 of 31 features complete)
- **Completed steps:** Step 0 — Planning and Governance; Step 1 — Python Project Foundation; Step 2 — Local Quality and Test Harness
- **Current step:** Step 3 — Typed Configuration and Secret Safety
- **Current feature:** Feature 3.2 — Implement the typed settings model and controlled loading function
- **Estimated remaining focused time:** Approximately 7 hours 10 minutes

## Completed Work

- [x] Created the local Git repository and public GitHub remote.
- [x] Approved the project scope, architecture, stack, and agenda.
- [x] Installed uv 0.12.3 and uv-managed Python 3.14.7.
- [x] Created and verified the locked `.venv` environment.
- [x] Materialized the approved project agenda in this file.
- [x] Initialized the project journal, decision record, and learning record.
- [x] Added licensing, changelog, initial README, and repository hygiene.
- [x] Created the minimal `src/forge` package and enabled project packaging.
- [x] Proved clean installation and package import through uv.
- [x] Configured Black and Ruff with compatible responsibilities.
- [x] Configured strict-but-practical MyPy checking.
- [x] Configured Pytest, coverage, test discovery, and the first package test.
- [x] Defined the safe environment-variable contract in `.env.example`.

## Remaining Work

- [ ] Complete Steps 3–9 and the graduation review.
- [ ] Verify all local, container, and CI quality gates.
- [ ] Demonstrate that a new project can start from Forge in under 10 minutes.

## Scope-Control Rules

These rules are mandatory and take precedence over convenience or available
time:

1. Work on only the currently approved feature.
2. A completed feature does not authorize the next feature.
3. Do not add optional dependencies, files, abstractions, or polish unless they
   are required by the approved feature.
4. Record adjacent ideas as future improvements; do not implement them during
   the active feature.
5. Do not refactor unrelated code while completing a feature.
6. Do not expand documentation beyond what the active feature requires.
7. Do not lower or bypass quality checks to make a feature pass.
8. Any scope or sequence change requires explicit user approval and an agenda
   update.
9. Stop at the declared stopping point even when time remains.
10. Commit, push, and other remote mutations require explicit authorization.

## Approved Scope Boundaries

### Required

- Professional `src/`-layout Python package
- uv-managed dependencies and lockfile
- Environment-variable management and typed settings
- Structured logging
- Central, framework-independent error conventions
- Unit and integration test examples
- Ruff, Black, MyPy, Pytest, and coverage quality gates
- Minimal FastAPI application with a health endpoint
- Dockerfile and Docker Compose support
- GitHub Actions CI for quality checks and tests
- README, architecture notes, changelog, license, and learning records

### Deferred

- LLM-provider or model integration
- Databases and data persistence
- Authentication and authorization
- Cloud deployment
- Metrics, tracing, or hosted observability platforms
- Kubernetes
- PyPI publishing
- Pre-commit hooks
- Automated project-renaming generator
- Additional API endpoints or example business logic

Deferred work is not part of project completion unless explicitly promoted into
scope.

## Approved Architecture

Forge uses a small modular-monolith architecture:

```text
Environment variables
        |
        v
Typed settings -----> Logging configuration
        |
        v
Application factory -----> FastAPI health endpoint
        |
        v
Framework-independent errors -----> HTTP error adapter
```

Application exceptions remain independent of FastAPI. The API boundary maps
safe application errors to HTTP responses, allowing the same foundation to
support a CLI, worker, or scheduled process later.

## Approved Technology Baseline

Exact resolved Python dependency versions are recorded in `uv.lock`.

| Component | Version | Responsibility |
| --- | --- | --- |
| Python | 3.14.7 | Runtime |
| uv | 0.12.3 | Python, environment, dependency, and lockfile management |
| FastAPI | 0.141.1 | HTTP application boundary |
| Uvicorn | 0.52.1 | ASGI server |
| Pydantic | 2.13.4 | Runtime validation |
| pydantic-settings | 2.15.0 | Typed environment configuration |
| structlog | 26.1.0 | Structured logging |
| Ruff | 0.16.2 | Linting and import rules |
| Black | 26.5.1 | Formatting |
| MyPy | 2.3.0 | Static type checking |
| Pytest | 9.1.1 | Test framework |
| pytest-cov | 7.1.0 | Coverage reporting |
| HTTPX | 0.28.1 | API integration-test client |
| Docker Engine | 29.6-compatible | Container build and runtime baseline |
| Container image | `python:3.14.7-slim-bookworm` | Container Python and OS baseline |
| GitHub runner | `ubuntu-24.04` | CI execution environment |

Ruff is used for linting and import rules; Black is used for formatting. This
intentional separation preserves the required stack while preventing competing
formatters from changing the same files.

## Dependency Sequence

```text
Step 0
  -> Step 1
    -> Step 2
      -> Steps 3 and 4
        -> Step 5
          -> Step 6
            -> Step 7
              -> Step 8
                -> Step 9
```

## Risks

| Risk | Mitigation |
| --- | --- |
| Scope creep | Enforce one approved feature and a hard stop. |
| Premature abstraction | Prefer concrete modules and small functions. |
| Secret exposure | Ignore local secrets and test logs, errors, and images for leakage. |
| Logging duplication | Make logging setup idempotent and test repeated configuration. |
| Unsafe error responses | Separate public messages from internal diagnostics. |
| Ruff and Black overlap | Give each tool one explicit responsibility and shared settings. |
| Dependency drift | Use compatible constraints plus a committed uv lockfile. |
| Local/container mismatch | Use the same settings and application entry point everywhere. |
| Coverage gaming | Test behavior and failure paths, not only lines. |
| Unproven reuse claim | Conduct a timed clean-room reuse exercise. |
| Learning hidden by generated code | Explain every pattern, tradeoff, and command before use. |

---

## Step 0 — Planning and Governance

### Goal

Approve the architecture, establish a reproducible environment, and create the
living project-management records.

### Why This Step Matters

Written scope and reproducible tooling prevent architecture drift and preserve
the reasoning behind the repository.

### Features

- [x] **0.1** Approve the project scope, architecture, stack, and agenda.
- [x] **0.2** Bootstrap and verify the reproducible Python environment.
- [x] **0.3** Create `docs/AGENDA.md` with scope guardrails.
- [x] **0.4** Initialize the journal, decisions, and learning records.

### Learning Objectives

- Translate requirements into an implementation plan.
- Distinguish required scope from deferred improvements.
- Understand environment reproducibility and lightweight governance.

### Expected Files Created or Modified

- `.gitignore`
- `.python-version`
- `pyproject.toml`
- `uv.lock`
- `docs/AGENDA.md`
- `docs/JOURNAL.md`
- `docs/DECISIONS.md`
- `docs/LEARNINGS.md`

### Testing Requirements

- Verify frozen dependency synchronization.
- Verify the managed Python and direct dependency versions.
- Verify every project requirement appears in this agenda.
- Verify no implementation modules were introduced.

### Documentation Requirements

- Record the initial architecture, stack, scope, sequencing, and repository
  naming decisions.

### Estimated Focused Time

1 hour 30 minutes across 1–2 sessions.

### Prerequisites

- Project brief
- Initialized local and GitHub repositories
- User approval

### Definition of Done

The environment is reproducible, planning records exist, every required
capability is scheduled, and the next feature is unambiguous.

---

## Step 1 — Python Project Foundation

### Goal

Complete an installable Python project with essential repository metadata.

### Why This Step Matters

A professional project needs explicit metadata and a package that behaves the
same inside and outside its repository.

### Features

- [x] **1.1** Add licensing, changelog, initial README, and repository hygiene.
- [x] **1.2** Create the minimal `src/forge` package and enable project packaging.
- [x] **1.3** Prove clean installation and package import through uv.

### Learning Objectives

- Understand `pyproject.toml` and the `src/` layout.
- Understand distribution names versus import-package names.
- Understand direct dependencies, transitive dependencies, and lockfiles.

### Expected Files Created or Modified

- `LICENSE`
- `CHANGELOG.md`
- `README.md`
- `.gitignore`
- `pyproject.toml`
- `uv.lock`
- `src/forge/__init__.py`

### Testing Requirements

- Run `uv sync --frozen`.
- Import the installed `forge` package without modifying `PYTHONPATH`.
- Verify the package metadata from the managed environment.

### Documentation Requirements

- Document prerequisites, environment setup, and package-layout decisions.

### Estimated Focused Time

1 hour across 1 session.

### Prerequisites

- Step 0

### Definition of Done

A clean clone can reproduce the environment and import the installed package.

---

## Step 2 — Local Quality and Test Harness

### Goal

Establish automated formatting, linting, type checking, testing, and coverage
before application logic grows.

### Why This Step Matters

Quality tools prevent inconsistent patterns and provide rapid feedback while
the codebase is still small.

### Features

- [x] **2.1** Configure Black and Ruff with compatible responsibilities.
- [x] **2.2** Configure strict-but-practical MyPy checking.
- [x] **2.3** Configure Pytest, coverage, test discovery, and the first package test.

### Learning Objectives

- Distinguish formatting, linting, typing, and testing.
- Understand centralized tool configuration.
- Understand test discovery and the limitations of coverage percentages.

### Expected Files Created or Modified

- `pyproject.toml`
- `tests/unit/test_package.py`
- Relevant documentation records

### Testing Requirements

- `uv run black --check .`
- `uv run ruff check .`
- `uv run mypy src`
- `uv run pytest`
- Enforce at least 90% coverage for meaningful production modules.

### Documentation Requirements

- Record why Ruff and Black are both retained.
- Document the standard local quality commands.

### Estimated Focused Time

1 hour across 1 session.

### Prerequisites

- Step 1

### Definition of Done

Formatting, linting, typing, tests, and coverage execute successfully from the
managed environment.

---

## Step 3 — Typed Configuration and Secret Safety

### Goal

Load settings from environment variables with explicit types, validation,
defaults, and safe failures.

### Why This Step Matters

Configuration differs between environments while source code should not.
Secrets must never be committed or casually exposed.

### Features

- [x] **3.1** Define the environment contract in `.env.example`.
- [ ] **3.2** Implement the typed settings model and controlled loading function.
- [ ] **3.3** Test defaults, overrides, invalid values, and secret representation.

### Learning Objectives

- Understand twelve-factor configuration.
- Understand runtime validation and secret types.
- Understand dependency injection versus global state.

### Expected Files Created or Modified

- `.env.example`
- `.gitignore`
- `src/forge/config.py`
- `tests/unit/test_config.py`
- Relevant documentation records

### Testing Requirements

- Verify defaults and environment overrides.
- Verify invalid values fail with useful errors.
- Verify secrets do not appear in representations, logs, or test output.
- Run all established quality checks.

### Documentation Requirements

- Explain `.env.example` versus ignored `.env`.
- Record the configuration-loading decision and common mistakes.

### Estimated Focused Time

1 hour 15 minutes across 1 session.

### Prerequisites

- Steps 1–2

### Definition of Done

Configuration is typed, testable, environment-driven, and secret-safe.

---

## Step 4 — Structured Logging and Error Conventions

### Goal

Provide predictable structured logs and an application-level exception model
independent of HTTP.

### Why This Step Matters

Production debugging requires searchable context, while safe error boundaries
prevent internal details from leaking to users.

### Features

- [ ] **4.1** Configure idempotent human-readable and JSON logging modes.
- [ ] **4.2** Add contextual fields and explicit sensitive-data rules.
- [ ] **4.3** Define the application error hierarchy and test safe behavior.

### Learning Objectives

- Understand structured logging, log levels, and context.
- Understand exception taxonomy.
- Understand public messages versus internal diagnostics.

### Expected Files Created or Modified

- `src/forge/logging.py`
- `src/forge/errors.py`
- `tests/unit/test_logging.py`
- `tests/unit/test_errors.py`
- Relevant documentation records

### Testing Requirements

- Verify JSON logs are valid structured objects.
- Verify local logs remain readable.
- Verify repeated configuration does not duplicate messages.
- Verify exceptions retain stable codes and safe public messages.
- Verify sensitive values are not emitted.

### Documentation Requirements

- Record the logging-library and error-boundary decisions.
- Explain common logging and exception-handling mistakes.

### Estimated Focused Time

1 hour 30 minutes across 1 session.

### Prerequisites

- Steps 1–3

### Definition of Done

Logs are structured and contextual, errors are centrally defined, and neither
mechanism exposes secrets.

---

## Step 5 — FastAPI-Ready Application Boundary

### Goal

Demonstrate how the foundation supports a small HTTP service without embedding
business logic in infrastructure modules.

### Why This Step Matters

AI inference, RAG, and agent systems are commonly exposed through APIs. An
application factory keeps startup behavior testable and reusable.

### Features

- [ ] **5.1** Implement the FastAPI application factory and runtime entry point.
- [ ] **5.2** Add a typed `GET /health` endpoint.
- [ ] **5.3** Translate application errors at the API boundary and add integration tests.

### Learning Objectives

- Understand ASGI and application factories.
- Understand API schemas and status codes.
- Understand unit versus integration tests and framework adapters.

### Expected Files Created or Modified

- `src/forge/api.py`
- `src/forge/main.py`
- `tests/integration/test_api.py`
- Relevant documentation records

### Testing Requirements

- Verify application construction with valid settings.
- Verify `/health` response schema and status.
- Verify known errors map to safe responses.
- Verify unexpected errors do not leak stack traces.
- Run all established quality checks.

### Documentation Requirements

- Document local server startup and health-check usage.
- Update the architecture overview.

### Estimated Focused Time

1 hour 15 minutes across 1 session.

### Prerequisites

- Steps 3–4

### Definition of Done

The service starts through one documented entry point and its HTTP behavior is
integration-tested.

---

## Step 6 — Containerization

### Goal

Package and run the same application predictably through Docker and Compose.

### Why This Step Matters

Containers reduce environment drift and provide a consistent deployment
artifact.

### Features

- [ ] **6.1** Define a secure, cache-efficient Docker build context and image.
- [ ] **6.2** Add Compose configuration for local service execution.
- [ ] **6.3** Add and execute a container smoke test.

### Learning Objectives

- Understand images, containers, layers, and build contexts.
- Understand build-time versus runtime configuration.
- Understand least privilege, health checks, and service lifecycle.

### Expected Files Created or Modified

- `.dockerignore`
- `Dockerfile`
- `compose.yaml`
- `scripts/container_smoke_test.sh`
- Relevant documentation records

### Testing Requirements

- Build the image successfully.
- Verify the container runs as a non-root user.
- Verify the health endpoint responds from the container.
- Verify environment variables reach the process.
- Verify secrets and development-only files are absent from the build context.

### Documentation Requirements

- Document build, run, Compose, logs, and shutdown commands.
- Record base-image and container-security decisions.

### Estimated Focused Time

1 hour 15 minutes across 1 session.

### Prerequisites

- Step 5
- Working Docker installation

### Definition of Done

The image builds, the service runs through Docker and Compose, and the smoke
test passes.

---

## Step 7 — Continuous Integration

### Goal

Run the same reproducible quality gates automatically on GitHub.

### Why This Step Matters

CI protects the shared branch from code that only works on one developer's
machine.

### Features

- [ ] **7.1** Create a least-privilege CI workflow with immutable action pins.
- [ ] **7.2** Add frozen dependency synchronization and safe caching.
- [ ] **7.3** Run formatting, linting, typing, tests, and coverage in CI.

### Learning Objectives

- Understand workflow triggers, jobs, steps, and runners.
- Understand CI permissions and immutable action references.
- Understand dependency caching and local/CI parity.

### Expected Files Created or Modified

- `.github/workflows/ci.yml`
- `README.md`
- Relevant documentation records

### Testing Requirements

- Validate workflow syntax.
- Confirm checks run on pull requests and relevant pushes.
- Confirm `uv sync --frozen` prevents lockfile drift.
- Confirm the real GitHub workflow passes.

### Documentation Requirements

- Add CI status and troubleshooting instructions.
- Record action-pinning and permissions decisions.

### Estimated Focused Time

1 hour across 1 session.

### Prerequisites

- Steps 1–6
- Explicit authorization before commits and pushes

### Definition of Done

GitHub CI passes and enforces the same quality gates used locally.

---

## Step 8 — Documentation and Reuse Validation

### Goal

Make Forge understandable, demonstrable, and reusable without mentor
assistance.

### Why This Step Matters

A starter kit fails if only its author knows how to operate or adapt it.

### Features

- [ ] **8.1** Complete setup, usage, testing, container, and troubleshooting documentation.
- [ ] **8.2** Complete the architecture overview and decision records.
- [ ] **8.3** Conduct and time a clean-room reuse trial in a temporary copy.

### Learning Objectives

- Write task-oriented technical documentation.
- Explain architecture and tradeoffs.
- Separate current limitations from future enhancements.
- Validate usability with evidence.

### Expected Files Created or Modified

- `README.md`
- `docs/architecture/overview.md`
- `docs/DECISIONS.md`
- `docs/LEARNINGS.md`
- `CHANGELOG.md`

### Testing Requirements

- Follow README instructions from a clean temporary directory.
- Start a derivative project in under 10 minutes.
- Run local checks and the service using only documented commands.
- Record measured time and friction.

### Documentation Requirements

- Document every major file and directory.
- Make only measured or supportable claims.

### Estimated Focused Time

1 hour across 1 session.

### Prerequisites

- Steps 1–7

### Definition of Done

A new user can understand, run, test, containerize, and reuse Forge solely from
its documentation.

---

## Step 9 — Graduation Review

### Goal

Audit the complete project and prove it meets the brief before declaring
completion.

### Why This Step Matters

Passing tests does not automatically prove security, maintainability,
documentation quality, or understanding.

### Features

- [ ] **9.1** Run the complete functional and quality validation suite.
- [ ] **9.2** Review architecture, security, reliability, portability, and documentation.
- [ ] **9.3** Produce graduation, portfolio, demo, interview, and future-work materials.

### Learning Objectives

- Conduct an engineering readiness review.
- Distinguish defects from enhancements.
- Make supportable portfolio claims.
- Explain the system without assistance.

### Expected Files Created or Modified

- Documentation and changelog files only where justified by review findings

### Testing Requirements

- Pass all local quality gates.
- Pass unit and integration tests and the coverage threshold.
- Pass Docker build and smoke tests.
- Pass GitHub CI.
- Pass clean-room setup and reuse validation.

### Documentation Requirements

Produce the final checklist, defects and limitations, resume-ready bullets,
portfolio case-study outline, demo-video outline, interview questions, and
separated future improvements.

### Estimated Focused Time

45 minutes across 1 session.

### Prerequisites

- Steps 0–8

### Definition of Done

All required evidence is reviewed, remaining defects are explicit, and the
project owner can explain every major design decision.

---

## Graduation Checklist

- [ ] I understand every major file.
- [ ] I can explain the architecture.
- [ ] I can justify the dependency choices.
- [ ] A clean environment can run `uv sync --frozen`.
- [ ] Formatting, linting, and type checks pass.
- [ ] Unit and integration tests pass.
- [ ] Coverage meets the agreed threshold.
- [ ] Secrets are not committed, logged, or included in images.
- [ ] The Docker image builds and runs.
- [ ] Compose starts the service.
- [ ] GitHub CI passes.
- [ ] A derivative project can begin in under 10 minutes.
- [ ] Documentation is complete and accurate.
- [ ] Known limitations are recorded.
- [ ] The repository is portfolio-ready.
- [ ] Resume and demonstration claims are evidence-based.

## Progress Update Procedure

After every completed feature:

1. Mark its checkbox complete.
2. Recalculate overall progress from the 31 tracked features.
3. Update the current step and current feature.
4. Record completed and remaining work.
5. Show the refreshed agenda summary.
6. Stop for review.
