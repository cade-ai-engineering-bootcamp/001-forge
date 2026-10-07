# Clean-Room Reuse Validation

## Result

**Passed on 2026-10-07.** A clean committed snapshot reached the
derivative-ready milestone in **118 seconds (1 minute 58 seconds)**, below the
10-minute target. The complete local and container validation finished in
**214 seconds (3 minutes 34 seconds)** from temporary-directory creation.

These measurements are evidence from one environment, not a guarantee for every
machine or network.

## Source and Host

| Item | Value |
| --- | --- |
| Source commit | `99427cc045662d01258b3d88e56307d7009063a8` |
| Host | Darwin 25.6.0, arm64 |
| uv | 0.12.3, Homebrew build |
| Python | CPython 3.14.7, already available through uv |
| Docker | 29.6.2 |
| Docker Compose | 5.3.1 |

## Isolation Method

1. Created a uniquely named directory under `/private/tmp`.
2. Exported the committed source with `git archive HEAD`.
3. Extracted only tracked files into a new project directory.
4. Confirmed the copy contained no `.git`, `.venv`, `.env`, Python caches,
   test caches, type-checking caches, lint caches, or coverage data.
5. Used a new empty uv cache stored outside the project directory.
6. Created a fresh project `.venv` with `uv sync --frozen`.
7. Initialized a new Git repository only after the application was healthy.

The uv executable and managed Python installation were host prerequisites and
were not reinstalled. Python packages were downloaded through the empty trial
cache. Docker used the host's existing layer cache where applicable.

## Timed Bootstrap

| Checkpoint | Command time | Result |
| --- | ---: | --- |
| Create committed archive | 0.01 s | Passed |
| Extract tracked files | 0.01 s | Passed |
| Frozen sync with empty uv cache | 1.53 s | 36 packages installed |
| Verify Python | 0.02 s | Python 3.14.7 |
| Verify editable import | 0.05 s | Loaded `src/forge/__init__.py` |
| Start server and call health | Less than 1.01 s | HTTP 200, `{"status":"ok"}` |
| Initialize independent Git repository | 0.02 s | New `main`, no commits |

The 118-second milestone is wall-clock time from temporary-directory creation
through fresh Git initialization. It includes command orchestration and an
attempted optional browser-tool check, so it is more conservative than the sum
of command execution times.

## Complete Validation

| Check | Time | Result |
| --- | ---: | --- |
| Black | 1.40 s | 12 files unchanged |
| Ruff | 0.44 s | Passed |
| MyPy | 2.81 s | 6 source files passed |
| Focused unit tests | 0.82 s | 37 passed |
| Focused integration tests | 0.29 s | 6 passed |
| Full Pytest and coverage | 0.60 s | 43 passed, 100% coverage |
| Container smoke test | 13.32 s | Passed and cleaned up |

The full 214-second wall-clock measurement includes bootstrap, all checks,
command orchestration, diagnostics, and the smoke test's container and network
cleanup. The overall temporary directory was deleted immediately afterward.

## Friction and Observations

- The optional `agent-browser` verification command was unavailable. Forge is a
  JSON API with no visual interface, so the documented `curl` request and the
  Uvicorn HTTP 200 access log provided the scoped runtime evidence.
- The macOS editable-install hidden-flag issue documented in the README did not
  occur in the clean temporary directory.
- The fresh Git repository correctly reported every project file as untracked,
  ready for a derivative project's initial commit.
- The Docker build reused available host layers but rebuilt changed application
  layers and completed every runtime security assertion.

## What This Proves

- Forge can create a fresh environment from committed files and an empty uv
  package cache.
- The README's sync, import, run, health, quality, focused-test, and container
  commands work in an isolated project directory.
- Forge does not depend on its original Git history, existing `.venv`, local
  dotenv file, or repository-generated caches.
- A derivative project can reach a healthy starting point in under 10 minutes
  on the measured host.

## What This Does Not Prove

- Identical setup time on another host, architecture, network, or cold Python
  installation
- Cross-platform behavior beyond the measured macOS arm64 environment and the
  Ubuntu environment already exercised by CI
- A completely cold Docker build without host layer caching
- Automatic renaming of the distribution, import package, or product identity
- Production deployment readiness or behavior of deferred features

## Cleanup

The Uvicorn process stopped cleanly. The smoke test removed its temporary
container and network. The exact clean-room directory and isolated uv cache were
permanently deleted after evidence capture. The reusable `forge:local` image was
retained for inspection.
