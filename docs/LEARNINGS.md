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

## Editable and Non-Editable Installations

### Simple Explanation

An editable installation connects the environment to the working source tree,
so code changes are immediately visible. A non-editable installation places
the built package in the environment's `site-packages`, matching deployment
behavior more closely.

### Why It Exists

Editable installs make development fast, while non-editable installs prove the
package can stand on its built artifact rather than local repository behavior.

### Professional Use

Developers commonly use editable installations locally and non-editable
installations in deployment images or release validation. Testing both reduces
the chance that packaging omissions reach production.

### Common Mistakes

- Treating an import from an existing development environment as clean proof
- Relying on the repository root or a manual `PYTHONPATH`
- Testing with stale installed files from an earlier build
- Confirming the import name without checking distribution metadata

### Best Practices

- Start clean-install validation with a new checkout and environment.
- Use frozen synchronization so validation cannot rewrite the lockfile.
- Run the installed interpreter outside the checkout with `PYTHONPATH` unset.
- Confirm the imported file lives in the expected environment.

## Formatting and Linting

### Simple Explanation

A formatter decides how code should look and rewrites it consistently. A
linter analyzes code for likely mistakes, suspicious patterns, and project
conventions without owning the complete visual style.

### Why It Exists

Automated formatting removes subjective style debates, while linting catches
problems that valid syntax and consistent formatting cannot detect.

### Professional Use

Teams run the same formatting and linting commands locally and in CI. A failed
check blocks inconsistent or suspicious code before it reaches the shared
branch.

### Common Mistakes

- Enabling two formatters that repeatedly rewrite each other's output
- Treating a formatter as a correctness checker
- Selecting every lint rule without evaluating conflicts and false positives
- Duplicating the Python target in several places until the settings drift
- Silencing a warning without understanding the behavior it protects

### Best Practices

- Give each tool one explicit responsibility.
- Share settings, such as line length, where tool behavior overlaps.
- Infer Python compatibility from standard project metadata when supported.
- Begin with useful correctness rules and add stricter rules deliberately.
- Run check-only commands before committing.

## Static Type Checking

### Simple Explanation

Static type checking analyzes how values flow through annotated Python code
without executing the program. It can identify incompatible arguments,
incorrect return values, and incomplete function contracts before runtime.

### Why It Exists

Python's runtime flexibility is useful, but it can defer interface mistakes
until a particular path executes. Type checking provides earlier feedback and
makes module boundaries easier to understand.

### Professional Use

Teams type-check production modules locally and in CI. Editors also use the
same annotations for navigation, completion, and immediate diagnostics.

### Common Mistakes

- Assuming type annotations automatically enforce values at runtime
- Allowing untyped functions to create hidden `Any` values
- Globally ignoring missing imports instead of addressing one dependency
- Adding broad suppressions without an error code and explanation
- Treating static typing as a substitute for runtime input validation

### Best Practices

- Type production boundaries and return values explicitly.
- Keep error codes visible so each failure is actionable.
- Use narrow exceptions only when a real library incompatibility requires one.
- Pair static typing with runtime validation for external data.
- Run MyPy through the project's locked environment.

## Test Discovery and Coverage

### Simple Explanation

Test discovery is the set of rules Pytest uses to find test files and
functions. Coverage measures which executable source lines and branches run
during those tests.

### Why It Exists

Predictable discovery prevents tests from silently disappearing, while a
coverage gate reveals untested production paths before they reach the shared
branch.

### Professional Use

Teams centralize test options so local development and CI run the same suite.
Coverage reports help reviewers find missing behavior, especially around
errors and conditional branches.

### Common Mistakes

- Adding `src` to `PYTHONPATH` and hiding broken package installation
- Assuming installed distribution metadata proves its editable path is active
- Confusing a high coverage percentage with correct behavior
- Writing assertions only to execute lines rather than verify outcomes
- Allowing unknown markers or configuration keys to pass silently
- Measuring tests themselves instead of the production package

### Best Practices

- Use explicit test directories and conventional test names.
- Import the installed package instead of modifying Python's import path.
- Inspect `.pth` processing when editable metadata exists but imports fail.
- Enable branch coverage and enforce a documented minimum.
- Treat coverage as a navigation aid, not proof of correctness.
- Test behavior and failure paths as meaningful modules are introduced.

## Environment Configuration Contracts

### Simple Explanation

An environment configuration contract names the values an application accepts
from its runtime environment. A committed `.env.example` shows that contract
with safe defaults and empty secret placeholders, while a local `.env` stores
developer-specific values and stays out of version control.

### Why It Exists

Applications need different settings in development, tests, and production
without changing source code. A visible contract makes those inputs
discoverable while separating documentation from sensitive values.

### Professional Use

Teams commit an example file, inject real values through local environments or
deployment systems, and validate them at the application boundary. A shared
prefix such as `FORGE_` identifies which variables belong to the application.

### Common Mistakes

- Committing a populated `.env` file or real credentials in the example
- Inventing settings before the application has a concrete need for them
- Treating an empty secret placeholder as permission to add an integration
- Assuming an example file provides runtime type validation
- Letting documentation and the implemented settings model drift apart

### Best Practices

- Keep `.env.example` safe to commit and `.env` ignored.
- Use non-secret defaults only where development behavior is unambiguous.
- Leave secret placeholders empty.
- Give application variables a consistent prefix.
- Keep the contract minimal and add settings only when requirements demand
  them.
- Validate and type the contract in application code separately.

## Typed Settings and Controlled Loading

### Simple Explanation

A typed settings model turns environment-variable strings into application
values such as enums, booleans, and protected secrets. A loader function
controls when that conversion happens and returns the validated result.

### Why It Exists

Reading raw strings throughout an application spreads parsing, defaults, and
error handling across unrelated modules. Loading settings during import also
creates hidden global state that is difficult to replace or reload safely.

### Professional Use

Applications load settings at a composition root, then pass the resulting
object to the components that need it. Deployment environment variables take
precedence over optional local dotenv values, while secret types prevent
routine representations from exposing credentials.

### Common Mistakes

- Calling `os.getenv` throughout application code
- Creating a settings singleton as an import side effect
- Treating static type annotations as runtime validation
- Logging or printing a secret's revealed value
- Allowing an empty secret placeholder to become a meaningful credential
- Caching settings before tests or runtime contexts can control their inputs

### Best Practices

- Validate external configuration once at an explicit boundary.
- Represent closed sets of values with enums.
- Let process environment values override local dotenv files.
- Use secret-aware types and reveal values only at the integration boundary.
- Return fresh settings objects unless caching has a demonstrated need.
- Pass settings explicitly to keep dependencies visible and testable.

## Testing Environment-Driven Configuration

### Simple Explanation

Configuration tests temporarily control environment variables and dotenv
files, load a settings object, and then verify the resulting typed values or
validation errors. Each test must begin from a known environment.

### Why It Exists

A test that inherits a developer's shell variables or reads their local `.env`
can pass on one machine and fail on another. Cached settings can also preserve
values from an earlier test and make results depend on execution order.

### Professional Use

Teams remove relevant environment variables before each test, create dotenv
files under the test framework's temporary directory, and restore process
state automatically afterward. They test source precedence and failure paths
as part of the public configuration contract.

### Common Mistakes

- Reading the repository's real `.env` during a unit test
- Depending on whichever variables exist in the developer's shell
- Changing `os.environ` without automatic cleanup
- Reusing a cached settings object between test cases
- Testing only valid inputs and defaults
- Printing revealed secrets in assertions or diagnostic output

### Best Practices

- Clear every application-owned variable before each test.
- Disable dotenv loading when a test only needs process variables or defaults.
- Use temporary files for dotenv scenarios.
- Verify environment variables take precedence over file values.
- Assert validation errors identify the affected field.
- Exercise secret representations without emitting revealed values.
- Confirm repeated loads are independent and order-insensitive.

## Structured Logging Modes and Ownership

### Simple Explanation

Structured logging represents each event as named data instead of assembling
an unstructured sentence. The same event can be rendered for a person at a
terminal or as JSON for a log-processing system.

### Why It Exists

Consistent fields make production logs searchable and machine-readable.
Explicit logger ownership also prevents repeated setup or embedded libraries
from duplicating output and disrupting unrelated logging systems.

### Professional Use

Applications configure logging at their startup boundary, emit records beneath
an owned logger namespace, and send container-friendly output to standard
output. Local renderers favor readability, while production renderers favor
stable structured data.

### Common Mistakes

- Adding a new handler every time configuration runs
- Configuring logging as an import side effect
- Replacing the root logger inside reusable infrastructure
- Sending human-readable colors into machine log collectors
- Building unrelated pipelines for structured and standard-library records
- Assuming a log level changes records that were already created

### Best Practices

- Configure logging explicitly during application startup.
- Give the application a named logger hierarchy it owns.
- Share processors between structured and standard-library records.
- Emit UTC timestamps and normalized level names.
- Write service logs to standard output.
- Replace owned handlers during reconfiguration.
- Test the rendered output and repeated-configuration behavior.

## Contextual Logging and Redaction Boundaries

### Simple Explanation

Contextual logging attaches fields such as a request identifier to every event
created during one unit of work. Redaction replaces values under sensitive
field names before a renderer converts the event to text or JSON.

### Why It Exists

Context connects related events during debugging, while redaction reduces the
risk of credentials reaching log storage. Async-aware context prevents one
concurrent request from using another request's identifiers.

### Professional Use

Applications bind context at a request, job, or command boundary and clear it
when that work finishes. A shared processor enforces the same field policy for
local output, production JSON, and standard-library records.

### Common Mistakes

- Storing request context in one mutable global dictionary
- Forgetting to clear context at the end of a unit of work
- Redacting only the top level of nested payloads
- Applying different security rules to different renderers
- Removing safe metrics such as `token_count` through broad substring matching
- Interpolating credentials into free-form event messages
- Assuming key-based redaction can recognize an unlabeled secret value

### Best Practices

- Use context variables for concurrent or asynchronous work.
- Bind context at entry boundaries and clear it at exit boundaries.
- Prefer named structured fields over interpolated messages.
- Normalize field names before applying a documented policy.
- Redact recursively before rendering.
- Apply one processor to every supported logging path.
- Test with dummy values and assert they never reach rendered output.

## Public Errors and Internal Diagnostics

### Simple Explanation

An application error can carry two different kinds of information: a stable,
safe explanation for a caller and diagnostic information for trusted code.
Keeping them separate prevents internal implementation details from becoming
part of a public response by accident.

### Why It Exists

Raw exceptions may contain file paths, dependency names, query fragments, or
other operational details. Stable error codes let callers respond consistently
without depending on changing diagnostic text.

### Professional Use

Application layers raise framework-independent errors. Boundary adapters map
those errors to HTTP responses, command exit codes, job states, or other
transport-specific results. Low-level exceptions remain connected through
exception chaining for diagnosis.

### Common Mistakes

- Returning `str()` from an arbitrary exception to a user
- Allowing each error instance to invent a new public message
- Adding HTTP status codes to reusable application errors
- Dropping the original exception instead of chaining it
- Logging internal diagnostics without considering sensitive data
- Treating an internal-detail field as a safe place for credentials

### Best Practices

- Use fixed public messages and stable machine-readable codes.
- Keep internal diagnostics out of exception arguments and public payloads.
- Catch expected failures through one shared base type.
- Preserve root causes with `raise ... from error`.
- Translate errors only at the relevant system boundary.
- Test strings, representations, serialization, logging, and chaining.
