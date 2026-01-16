# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- N/A.

## [0.0.3] - 2026-01-16

### Added

- CLI flags for dry-run and list-files, plus standardized summary logging.
- Encoding detection toggle for robust UTF-8 fallbacks.
- CLI flag to suppress non-essential output (--quiet).
- Optional markdownlint MD010 markers for Makefile blocks.
- Multiplatform CI workflow running ruff, mypy, and pytest with coverage.
- Governance documents and contribution guidance.

### Changed

- Deterministic directory scans with cached filter normalization.
- Updated README with Quickstart guidance and expanded filter semantics.
- Packaging metadata aligned with PEP 621, including classifiers and project URLs.

### Fixed

- Logger configuration idempotency and repeated log-level updates.
- Encoding detection edge cases with strict-first UTF-8 decoding.
- Tests for encoding samples, dry-run/list-files behavior, and string comparisons.

## [0.0.2] - 2026-01-13

### Added

- Initial CLI implementation and test suite.
