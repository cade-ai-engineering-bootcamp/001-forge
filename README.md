# Forge

Forge is a reusable, production-quality Python engineering starter kit for
future AI systems. It establishes the operational foundation those systems
need without introducing model-provider integrations or application-specific
business logic.

> [!NOTE]
> Forge is under active development. The reproducible environment and project
> governance are available now, along with the minimal installable `forge`
> package. Quality gates, the API, container support, and continuous
> integration are planned work.

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

- [Git](https://git-scm.com/)
- [uv 0.12.3](https://docs.astral.sh/uv/)

uv installs and selects the project's required Python 3.14.7 interpreter from
the committed `.python-version` file.

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

Activate the environment in a POSIX-compatible shell:

```bash
source .venv/bin/activate
```

Verify the managed toolchain:

```bash
uv --version
python --version
```

Verify the installed package:

```bash
uv run python -c "import forge; print(forge.__file__)"
```

When finished, leave the virtual environment with:

```bash
deactivate
```

## Local Quality Checks

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

Black is the project's only formatter. Ruff is intentionally limited to
linting and import rules so the tools do not compete to rewrite the same code.
MyPy analyzes type relationships without changing files or validating runtime
input. Pytest discovers tests under `tests/` and measures the installed `forge`
package without adding `src` directly to Python's import path.

## Repository Layout

```text
.
├── docs/               # Agenda, journal, decisions, and learning records
├── src/
│   └── forge/           # Installable Python import package
├── tests/
│   └── unit/            # Fast, isolated package tests
├── .python-version     # Required Python interpreter version
├── CHANGELOG.md        # Notable project changes
├── LICENSE             # MIT license
├── pyproject.toml      # Project metadata and dependency declarations
└── uv.lock             # Exact resolved dependency graph
```

`forge-ai-starter-kit` is the distribution name recorded in project metadata;
`forge` is the shorter name used by Python imports. The `src/` layout keeps
importable code separate from repository-level files and requires the project
to be installed before it can be imported reliably.

## Project Documentation

- [`docs/AGENDA.md`](docs/AGENDA.md) — scope, sequence, status, and acceptance criteria
- [`docs/JOURNAL.md`](docs/JOURNAL.md) — chronological work-session record
- [`docs/DECISIONS.md`](docs/DECISIONS.md) — architectural decision record
- [`docs/LEARNINGS.md`](docs/LEARNINGS.md) — engineering concepts and lessons
- [`CHANGELOG.md`](CHANGELOG.md) — user-visible project changes

## License

Forge is available under the [MIT License](LICENSE).
