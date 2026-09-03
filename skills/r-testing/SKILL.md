---
name: r-testing
description: "Use to write or review R tests with testthat, fixtures, snapshots, mocks, warnings, errors, optional dependencies, and deterministic integrations."
license: MIT
compatibility: "R 4.1+ and the documented packages; compatible with Claude Code, Cursor, Gemini CLI, Codex, and similar Agent Skills clients."
user-invocable: true
allowed-tools: "Read Edit Write Glob Grep Bash(R:*) Bash(Rscript:*) Bash(git:*) Agent"
metadata:
  author: samber
  version: "0.1.0"
  openclaw:
    emoji: "🧪"
    homepage: "https://github.com/samber/cc-skills-r"
    requires:
      bins:
        - R
        - Rscript
    install: []
---

# R testing

Tests should specify observable behavior and fail for the bug the test is intended to prevent. Prefer fast, isolated tests, then add explicit integration coverage for boundaries that unit tests cannot exercise.

## Test design

- Use `testthat` with descriptive `test_that()` names and one behavior per test block.
- Cover normal, empty, missing, malformed, boundary, and duplicate-key inputs when they affect the contract.
- Assert structure as well as values: class, names, dimensions, row count, column types, grouping, and ordering when meaningful.
- Prefer `expect_equal()` for exact values, `expect_identical()` for strict type/attribute contracts, and targeted expectations such as `expect_error()`, `expect_warning()`, and `expect_message()`.
- Test public behavior rather than private implementation details. Refactor production code to expose a stable contract instead of asserting internal environments or helper call counts.
- Use `withr` to isolate options, environment variables, working directories, graphics devices, and temporary files. Always clean up resources.
- Avoid real network, clock, randomness, and user-library state in unit tests. Inject boundaries or use deterministic fixtures.

## Test tiers

- Unit tests are local and fast; they belong in `tests/testthat/`.
- Integration tests may use databases, files, or external services, but must declare prerequisites and be explicitly selected or skipped in CI.
- Snapshot tests are useful for stable user-facing text, plots, or structured output; do not snapshot volatile timestamps, paths, or unordered data.
- Use `testthat::skip_if_not_installed()` for optional integrations, and make the skip visible rather than silently changing the behavior under test.

## Failure and evaluation

When testing warnings or errors, assert the condition class and stable message fragments, not incidental full backtraces. For data workflows, verify row multiplication, grouping retention, and type stability explicitly.

Read [references/testthat-patterns.md](references/testthat-patterns.md) for expectation and fixture choices. Read [references/integration-and-fixtures.md](references/integration-and-fixtures.md) for isolation and test tiers. Use `r-errors` when defining the conditions tests should consume.
