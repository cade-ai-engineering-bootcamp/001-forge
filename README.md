# Forge

[![CI](https://github.com/cade-ai-engineering-bootcamp/001-forge/actions/workflows/ci.yml/badge.svg)](https://github.com/cade-ai-engineering-bootcamp/001-forge/actions/workflows/ci.yml)

Forge is a reusable, production-quality Python engineering starter kit for
future AI systems. It establishes the operational foundation those systems
need without introducing model-provider integrations or application-specific
business logic.

> [!NOTE]
> Forge is under active development. The reproducible environment and project
> governance, quality gates, FastAPI boundary, and production container image
> are available now, together with Docker Compose and continuous integration.
> Documentation and reuse validation remain in progress.

## Project Goals

Forge is designed to provide a consistent starting point for AI engineering
projects with:

- Reproducible Python and dependency management
- A professional `src/`-layout package
- Typed environment configuration and secret-safe defaults
- Structured logging and framework-independent errors
- Automated formatting, linting, type checking, testing, and coverage
- A minimal FastAPI application boundary
- Docker and Docker Compose support
- GitHub Actions continuous integration
- Practical architecture and operational documentation

The project intentionally excludes LLM integrations, databases,
authentication, cloud deployment, and application-specific business logic.
See [`docs/AGENDA.md`](docs/AGENDA.md) for the approved scope and implementation
sequence.

## Prerequisites

For local Python development:

- [Git](https://git-scm.com/)
- [uv 0.12.3](https://docs.astral.sh/uv/)
- `curl` for command-line health checks

uv installs and selects the project's required Python 3.14.7 interpreter from
the committed `.python-version` file.

Container workflows additionally require:

- Docker Engine 29.6-compatible, with Docker Compose
- Bash and `curl` for `scripts/container_smoke_test.sh`

The commands below use a POSIX-compatible shell. Container commands work with
Docker Desktop or another compatible Docker Engine and Compose installation.

## Setup

Clone the repository and enter its directory:

```bash
git clone https://github.com/cade-ai-engineering-bootcamp/001-forge.git
cd 001-forge
```

Create the virtual environment and install the exact locked dependencies:

```bash
uv sync --frozen
```

Verify the managed toolchain and installed package:

```bash
uv --version
uv run python --version
uv run python -c "import forge; print(forge.__file__)"
```

The expected tool versions are uv 0.12.3 and Python 3.14.7. The package path
should end in `src/forge/__init__.py`, confirming the editable development
install. Commands prefixed with `uv run` do not require manual activation.

Optionally activate the environment when using `python` directly:

```bash
source .venv/bin/activate
```

When finished, leave the activated environment with:

```bash
deactivate
```

## Quick Start

Start Forge from the repository root:

```bash
uv run uvicorn forge.main:app --reload
```

In a second terminal, call the liveness endpoint:

```bash
curl --fail --silent http://127.0.0.1:8000/health
```

The expected response is `{"status":"ok"}`. Return to the server terminal and
press `Ctrl+C` to stop it. Forge uses safe development defaults when no `.env`
file exists.

## Environment Configuration

`.env.example` documents Forge's supported environment variables without
containing real secrets. Copy it to the ignored `.env` file for local values:

```bash
cp .env.example .env
```

| Variable | Purpose |
| --- | --- |
| `FORGE_ENVIRONMENT` | Runtime environment: `development`, `test`, or `production`. |
| `FORGE_LOG_LEVEL` | Minimum level: `DEBUG`, `INFO`, `WARNING`, `ERROR`, or `CRITICAL`. |
| `FORGE_LOG_JSON` | Selects JSON logs when `true` and human-readable logs when `false`. |
| `FORGE_API_KEY` | Optional secret used to demonstrate secret-safe configuration handling. |

The committed example is a contract, not a place for credentials. `.env` and
environment-specific variants such as `.env.local` remain ignored.

Load and validate the configuration where the application starts:

```python
from forge.config import load_settings

settings = load_settings()
```

`load_settings()` reads `.env` when it exists, then lets process environment
variables override file values. Pass `env_file=None` to read only the process
environment. Every call returns a fresh `Settings` instance so callers can
inject configuration explicitly instead of depending on global state. Invalid
enum or boolean values raise a Pydantic validation error, and `FORGE_API_KEY`
uses Pydantic's masked `SecretStr` representation.

## Structured Logging

Configure logging once at the application boundary using the validated
settings, then create loggers beneath the `forge` namespace:

```python
import structlog

from forge.config import load_settings
from forge.logging import configure_logging

settings = load_settings()
configure_logging(
    log_level=settings.log_level,
    json_output=settings.log_json,
)
logger = structlog.get_logger("forge.application")
logger.info("forge_started")
```

Human-readable mode produces deterministic, color-free console output for
local development. JSON mode emits one valid JSON object per line for log
collection systems. Both modes write to standard output and include UTC
timestamps and normalized levels. Repeated configuration replaces Forge's
existing handler instead of duplicating messages, and it does not take
ownership of the process root logger.

Bind fields that should accompany subsequent events in the current execution
context, then clear them at the boundary where that work ends:

```python
from forge.logging import bind_context, clear_context

bind_context(request_id="req-123", component="health")
logger.info("request_started")
clear_context()
```

Forge masks values stored under sensitive field names such as `api_key`,
`authorization`, `cookie`, `password`, `secret`, and `token`, including common
prefixed forms such as `access_token` or `client_secret`. Matching is
case-insensitive, works through nested mappings and sequences, and applies to
both Structlog fields and standard-library `extra` fields. Safe operational
fields such as `token_count` remain visible.

Redaction is field-name based. Never place credentials directly in an event
name or interpolate them into a free-form log message, where their meaning
cannot be identified reliably.

## Application Errors

Expected application failures use framework-independent errors with stable
codes and fixed public messages:

```python
from forge.errors import DependencyUnavailableError

raise DependencyUnavailableError(
    internal_detail="The vector service timed out after five seconds."
)
```

All known errors inherit from `ApplicationError`. Their normal string and
representation output remains public-safe, while trusted application code may
inspect `internal_detail` for diagnosis. `to_public_dict()` returns only the
stable `code` and public `message` intended for a system boundary.

Internal details must never contain credentials. Preserve a low-level failure
with Python exception chaining (`raise ... from error`) instead of exposing it
in a public message. Error classes intentionally contain no HTTP status codes;
the API adapter owns this transport-specific translation:

| Application error | HTTP status |
| --- | ---: |
| `InvalidInputError` | `400 Bad Request` |
| `ResourceNotFoundError` | `404 Not Found` |
| `ConflictError` | `409 Conflict` |
| `DependencyUnavailableError` | `503 Service Unavailable` |
| Base or unmapped `ApplicationError` | `500 Internal Server Error` |

Known application errors return only their stable public code and message.
Unexpected exceptions return a generic `internal_server_error` response with
HTTP 500; their exception text and stack traces never enter the HTTP body.
FastAPI's own request-validation and HTTP exception behavior remains intact.

## Running the Application

Forge constructs its FastAPI application through an injectable factory. The
runtime module exposes that configured application through one ASGI entry
point:

```bash
uv run uvicorn forge.main:app --reload
```

Uvicorn imports `forge.main:app`, which loads validated settings, configures
Forge logging, and creates the FastAPI application. The factory also accepts a
`Settings` instance directly so tests and alternate runtimes can control
configuration without changing process environment state:

```python
from forge.api import create_app
from forge.config import Settings

app = create_app(settings=Settings())
```

Check that the running HTTP process can respond:

```bash
curl http://127.0.0.1:8000/health
```

Forge returns a typed liveness response with HTTP status `200 OK`:

```json
{"status":"ok"}
```

This endpoint confirms only that the Forge process is running and responsive.
It does not report dependency readiness, and Forge intentionally has no
business routes.

## Container Image

Confirm Docker and Compose are available before using the container workflows:

```bash
docker info
docker compose version
```

Build the production image from the repository root:

```bash
docker build --tag forge:local .
```

Run Forge with production-oriented settings and publish it only on the local
host:

```bash
docker run --detach \
  --name forge \
  --publish 127.0.0.1:8000:8000 \
  --env FORGE_ENVIRONMENT=production \
  --env FORGE_LOG_JSON=true \
  forge:local
```

Inspect container health and application output:

```bash
docker inspect --format '{{.State.Health.Status}}' forge
curl http://127.0.0.1:8000/health
docker logs forge
```

Stop and remove the container when finished:

```bash
docker stop forge
docker rm forge
```

The image installs only locked runtime dependencies and runs as the fixed
unprivileged user `10001:10001`. The allowlisted build context excludes local
environments, credentials, Git history, tests, caches, and development records.
Runtime configuration is supplied through environment variables rather than
baked into image layers.

### Docker Compose

Validate the Compose configuration, then build and start Forge in the
background while waiting for its health check:

```bash
docker compose config --quiet
docker compose up --build --detach --wait
```

Inspect the service, call the API, and follow its logs:

```bash
docker compose ps
curl http://127.0.0.1:8000/health
docker compose logs --follow api
```

Stop the service and remove its container and network:

```bash
docker compose down
```

Compose uses development-safe settings by default. Set
`FORGE_ENVIRONMENT`, `FORGE_LOG_LEVEL`, or `FORGE_LOG_JSON` in the shell or an
ignored local `.env` file to override them. The service remains bound to the
local host, runs as `10001:10001`, drops all Linux capabilities, prevents
privilege escalation, and uses a read-only root filesystem with an ephemeral
`/tmp` scratch area. It does not mount the source tree or pass an API key.

### Container Smoke Test

Run the complete container acceptance check from the repository root:

```bash
./scripts/container_smoke_test.sh
```

The script requires Docker with Compose and `curl`. It builds and starts Forge
under the isolated `forge-smoke` project, waits for health, verifies the API,
runtime settings, non-root identity, filesystem restrictions, image contents,
and Linux security controls, then removes its temporary container and network.
If a check fails, it prints the service logs before cleanup and exits nonzero.

## Testing and Local Quality Checks

Tests are split by responsibility:

- `tests/unit/` checks individual Forge modules in isolation.
- `tests/integration/` checks the FastAPI application through real HTTP
  requests against an in-process test application.

Run every quality command below before committing. The complete Pytest run is
the authoritative test result because it enforces project-wide coverage.

Verify that Python files match Black's formatting rules:

```bash
uv run black --check .
```

Run Ruff's correctness, import-ordering, and modernization checks:

```bash
uv run ruff check .
```

Type-check the production package with MyPy:

```bash
uv run mypy src
```

Run the test suite with branch coverage and the 90% coverage gate:

```bash
uv run pytest
```

For focused diagnosis, run one test group without applying the project-wide
coverage threshold to that partial run:

```bash
uv run pytest tests/unit --no-cov
uv run pytest tests/integration --no-cov
```

Focused runs do not replace the complete `uv run pytest` gate.

Black is the project's only formatter. Ruff is intentionally limited to
linting and import rules so the tools do not compete to rewrite the same code.
MyPy analyzes type relationships without changing files or validating runtime
input. Pytest discovers tests under `tests/` and measures the installed `forge`
package without adding `src` directly to Python's import path.

## Continuous Integration

The [CI workflow](.github/workflows/ci.yml) runs for pull requests targeting
`main` and pushes to `main`. It recreates the pinned uv and Python environment,
synchronizes `uv.lock` without changing it, and runs the same Black, Ruff,
MyPy, Pytest, and coverage checks documented above.

If CI fails, open the workflow run, expand the first failed step, and reproduce
its displayed command from the repository root after running
`uv sync --frozen`. Fix the underlying code, configuration, test, or lockfile
issue locally; do not weaken or skip the failing check. Push the correction to
the same pull-request branch to start a new run.

## Troubleshooting

### uv or Python version mismatch

Confirm `uv --version` reports 0.12.3. Install the project interpreter with
`uv python install 3.14.7`, then rerun `uv sync --frozen`. Do not change
`.python-version` or the required uv version merely to bypass a local mismatch.

### Frozen synchronization fails

Run `git status` and review changes to `pyproject.toml` and `uv.lock`. A frozen
sync uses the existing lockfile without updating it and does not check whether
it reflects newer dependency edits. Run `uv lock --check` when freshness must
be verified. Dependency changes must deliberately update both project metadata
and the committed lockfile; otherwise restore the intended committed inputs.

### `forge` cannot be imported

Run `uv sync --frozen`, then use `uv run python` or activate `.venv`. Running a
different system Python will not necessarily see the installed Forge package.
If `uv pip list` shows `forge-ai-starter-kit` but imports still fail on macOS,
clear Finder's hidden flag from the environment and retry:

```bash
chflags -R nohidden .venv
uv run python -c "import forge; print(forge.__file__)"
```

This changes only local filesystem metadata. Rerun it after synchronization if
the hidden flag returns.

### Configuration validation fails

Compare `.env` with `.env.example`. Environment names are lowercase, log levels
are uppercase, and `FORGE_LOG_JSON` must contain a recognized boolean value.
Process environment variables override values from `.env`.

### Port 8000 is already in use

Stop the process or container currently using the port, or start a temporary
local server on another port:

```bash
uv run uvicorn forge.main:app --reload --port 8001
curl --fail --silent http://127.0.0.1:8001/health
```

### Docker is unavailable or Forge is unhealthy

Run `docker info` to confirm the daemon is available and
`docker compose version` to confirm Compose is installed. For a failed Compose
startup, inspect `docker compose ps` and `docker compose logs api`, then run
`docker compose down` before retrying. For the standalone `forge` container,
use `docker logs forge` and remove an existing stopped container with
`docker rm forge` before reusing that name.

### A CI check fails

Open the named failing step and run its exact command locally after
`uv sync --frozen`. The [Continuous Integration](#continuous-integration)
section lists CI behavior; do not skip or weaken a gate to obtain a green run.

## Repository Layout

```text
.
├── .github/
│   └── workflows/
│       └── ci.yml       # Hosted quality gates
├── docs/
│   ├── architecture/
│   │   └── overview.md   # System structure, flows, boundaries, and limits
│   ├── AGENDA.md         # Scope, sequence, and completion status
│   ├── DECISIONS.md      # Architecture decision record
│   ├── JOURNAL.md        # Chronological implementation evidence
│   └── LEARNINGS.md      # Concepts, mistakes, and best practices
├── scripts/
│   └── container_smoke_test.sh  # Container acceptance check
├── src/
│   └── forge/           # Installable Python import package
├── tests/
│   ├── integration/     # HTTP boundary tests
│   └── unit/            # Fast, isolated module tests
├── .dockerignore        # Allowlisted Docker build context
├── .env.example         # Safe environment-variable contract
├── .gitignore           # Local and generated-file exclusions
├── .python-version      # Required Python interpreter version
├── CHANGELOG.md         # Notable project changes
├── compose.yaml         # Secure local service orchestration
├── Dockerfile           # Multi-stage production container image
├── LICENSE              # MIT license
├── pyproject.toml       # Metadata, dependencies, and tool configuration
├── README.md            # Setup and operating guide
└── uv.lock              # Exact resolved dependency graph
```

`forge-ai-starter-kit` is the distribution name recorded in project metadata;
`forge` is the shorter name used by Python imports. The `src/` layout keeps
importable code separate from repository-level files and requires the project
to be installed before it can be imported reliably.

## Project Documentation

- [`docs/architecture/overview.md`](docs/architecture/overview.md) — system structure, boundaries, flows, and limitations
- [`docs/AGENDA.md`](docs/AGENDA.md) — scope, sequence, status, and acceptance criteria
- [`docs/JOURNAL.md`](docs/JOURNAL.md) — chronological work-session record
- [`docs/DECISIONS.md`](docs/DECISIONS.md) — architectural decision record
- [`docs/LEARNINGS.md`](docs/LEARNINGS.md) — engineering concepts and lessons
- [`CHANGELOG.md`](CHANGELOG.md) — user-visible project changes

## License

Forge is available under the [MIT License](LICENSE).
