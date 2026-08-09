# Forge

Forge is a reusable, production-quality Python engineering starter kit for
future AI systems. It establishes the operational foundation those systems
need without introducing model-provider integrations or application-specific
business logic.

> [!NOTE]
> Forge is under active development. The reproducible environment and project
> governance are available now; the installable Python package, quality gates,
> API, container support, and continuous integration are planned work.

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

When finished, leave the virtual environment with:

```bash
deactivate
```

## Repository Layout

```text
.
├── docs/               # Agenda, journal, decisions, and learning records
├── .python-version     # Required Python interpreter version
├── CHANGELOG.md        # Notable project changes
├── LICENSE             # MIT license
├── pyproject.toml      # Project metadata and dependency declarations
└── uv.lock             # Exact resolved dependency graph
```

The `src/forge` package will be introduced in the next project-foundation
feature. Packaging is intentionally disabled until that package exists.

## Project Documentation

- [`docs/AGENDA.md`](docs/AGENDA.md) — scope, sequence, status, and acceptance criteria
- [`docs/JOURNAL.md`](docs/JOURNAL.md) — chronological work-session record
- [`docs/DECISIONS.md`](docs/DECISIONS.md) — architectural decision record
- [`docs/LEARNINGS.md`](docs/LEARNINGS.md) — engineering concepts and lessons
- [`CHANGELOG.md`](CHANGELOG.md) — user-visible project changes

## License

Forge is available under the [MIT License](LICENSE).
