# Learning Record

This document captures concepts learned while building Forge. Each entry
explains the concept plainly, why it exists, where it is used professionally,
common mistakes, and recommended practices.

## Local Repositories and GitHub Remotes

### Simple Explanation

A local Git repository stores history on one computer. A GitHub repository is a
remote copy used for collaboration, backup, review, and automation. The
`origin` remote connects the two repositories.

### Why It Exists

Separating local work from shared history allows changes to be developed and
reviewed before they affect other contributors.

### Professional Use

Teams use branches, commits, pull requests, and protected default branches to
review work and preserve an auditable history.

### Common Mistakes

- Assuming a local commit automatically appears on GitHub
- Committing generated environments or secrets
- Staging every file without reviewing the scope
- Working directly on the default branch after repository bootstrap

### Best Practices

- Inspect `git status` and the staged diff before committing.
- Stage only the files belonging to the approved feature.
- Use focused commit messages and short-lived feature branches.
- Treat commit, push, pull-request creation, and merge as separate actions.

## Virtual Environments

### Simple Explanation

A virtual environment is an isolated directory containing the Python
interpreter context and packages for one project. Forge's environment lives in
`.venv` and is generated rather than committed.

### Why It Exists

Projects often require different package versions. Isolation prevents one
project's dependencies from changing or breaking another project.

### Professional Use

Development machines, CI jobs, and build systems create isolated environments
from committed dependency metadata instead of sharing global packages.

### Common Mistakes

- Installing project dependencies globally
- Committing `.venv`
- Assuming activation changes the lockfile
- Trusting the prompt label instead of verifying the interpreter path

### Best Practices

- Generate the environment from `pyproject.toml` and `uv.lock`.
- Ignore `.venv` in Git.
- Verify with `python --version`, `which python`, or `uv run python`.
- Use `uv run` when explicit activation is unnecessary.

## Dependency Metadata and Lockfiles

### Simple Explanation

`pyproject.toml` declares the project's direct dependencies and allowed version
ranges. `uv.lock` records the exact direct and transitive versions selected for
a reproducible installation.

### Why It Exists

Compatible ranges allow controlled upgrades, while the lockfile makes today's
working environment repeatable.

### Professional Use

Teams review dependency changes in pull requests and use frozen installation in
CI so builds cannot silently select different versions.

### Common Mistakes

- Editing dependency declarations without refreshing the lockfile
- Committing a lockfile generated from unrelated requirements
- Deleting the lockfile when resolution fails
- Confusing a direct dependency with every transitive package it installs

### Best Practices

- Declare only dependencies the project imports or directly operates.
- Commit `pyproject.toml` and `uv.lock` together when dependencies change.
- Use `uv sync --frozen` for verification and CI.
- Review both dependency intent and resolved changes.

## Tool Versions and Reproducibility

### Simple Explanation

Reproducibility means another environment can recreate the same important
runtime and dependency state from versioned project files.

### Why It Exists

Uncontrolled interpreter, tool, and package upgrades can make a project behave
differently across machines or over time.

### Professional Use

Teams pin runtimes, lock application dependencies, and use explicit CI and
container baselines to reduce environmental drift.

### Common Mistakes

- Pinning nothing and relying on whatever is globally installed
- Pinning every declaration rigidly without an upgrade process
- Claiming reproducibility without testing a clean installation

### Best Practices

- Pin the Python patch version for this starter kit.
- Use compatible constraints for dependency intent and a lockfile for exact
  resolution.
- Verify with frozen synchronization.
- Upgrade versions deliberately in a focused change.

## Scope Control as an Engineering Practice

### Simple Explanation

Scope control means defining exactly what a change will accomplish and stopping
when that result is complete.

### Why It Exists

Unplanned additions make changes harder to review, test, explain, and reverse.

### Professional Use

Engineering teams use tickets, acceptance criteria, small pull requests, and
Definitions of Done to keep delivery predictable.

### Common Mistakes

- Treating nearby improvements as implicitly approved
- Refactoring unrelated code during a focused feature
- Adding abstractions for hypothetical future needs
- Continuing merely because time remains

### Best Practices

- Work on one approved feature at a time.
- Record good adjacent ideas without implementing them immediately.
- Keep diffs aligned with acceptance criteria.
- Stop for review at the declared boundary.

## Distribution Names, Import Packages, and the `src/` Layout

### Simple Explanation

A distribution name identifies an installable project to packaging tools,
while an import-package name identifies the module used in Python code. Forge's
distribution is `forge-ai-starter-kit`, while its Python import is `forge`.

The `src/` layout places that import package under `src/forge` rather than in
the repository root.

### Why It Exists

Separating installable source from repository files prevents Python from
finding a local module merely because the current directory happens to contain
it. Successful imports must come through the configured package installation.

### Professional Use

Libraries and service repositories use build backends to turn source trees
into installable distributions. Editable local installations preserve that
packaging behavior while allowing source changes to appear immediately during
development.

### Common Mistakes

- Assuming the repository, distribution, and import names must match
- Importing directly from the repository root without testing installation
- Adding `src` to `PYTHONPATH` to hide broken packaging
- Duplicating the project version manually inside `__init__.py`

### Best Practices

- Configure the build backend explicitly.
- Map nonmatching distribution and import names deliberately.
- Keep `__init__.py` small until a public package API is required.
- Test imports from an installed environment outside the repository root.
