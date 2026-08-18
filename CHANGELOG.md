# Changelog

All notable changes to Forge will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project intends to follow [Semantic Versioning](https://semver.org/).

## [Unreleased]

### Added

- Initial project scope, architecture, and implementation agenda.
- Reproducible uv environment using Python 3.14.7.
- Runtime and development dependency lockfile.
- Project journal, decision record, and learning record.
- MIT license and initial repository documentation.
- Minimal `forge` import package and uv build configuration.
- Verified frozen, non-editable installation and package metadata.
- Compatible Black formatting and Ruff linting configuration.
- Strict MyPy checking for production source code.
- Pytest discovery, branch coverage enforcement, and the first package test.
- Safe example contract for Forge environment variables and optional secrets.
- Typed settings model with validated values, masked secrets, and controlled
  dotenv loading.
- Isolated configuration tests for defaults, overrides, validation failures,
  fresh loading, and secret-safe representations.
- Idempotent Forge logging with human-readable and JSON renderers, UTC
  timestamps, level filtering, and standard-library interoperability.
- Async-safe contextual logging with recursive, key-based sensitive-field
  redaction across structured and standard-library records.
- Framework-independent application errors with stable codes, safe public
  messages, internal diagnostics, and explicit public serialization.
- Injectable FastAPI application factory and a conventional Uvicorn-compatible
  ASGI runtime entry point.

[Unreleased]: https://github.com/cade-ai-engineering-bootcamp/001-forge/commits/main
