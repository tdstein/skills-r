---
name: r-errors
description: "Use to design or handle R errors, warnings, messages, rlang conditions, recovery, backtraces, and user-facing diagnostics."
license: MIT
compatibility: "R 4.1+ and the documented packages; compatible with Claude Code, Cursor, Gemini CLI, Codex, and similar Agent Skills clients."
user-invocable: true
allowed-tools: "Read Edit Write Glob Grep Bash(R:*) Bash(Rscript:*) Bash(git:*) Agent"
metadata:
  author: tdstein
  version: "0.1.0"
  openclaw:
    emoji: "🚦"
    homepage: "https://github.com/tdstein/cc-skills-r"
    requires:
      bins:
        - R
        - Rscript
    install: []
---

# R errors and conditions

Make failures actionable for both users and calling code. A condition should identify what failed, preserve machine-readable classification, and carry enough context to diagnose the input or operation.

## Raise conditions

- Use `rlang::abort()` for errors in modern R packages and applications. Give domain failures a stable subclass such as `my_pkg_invalid_id` or `my_pkg_missing_dependency`.
- Include the operation and relevant safe context in the message. Do not include secrets, full personal data, or enormous inputs.
- Use bullets or structured fields when several causes or remediation steps matter. Keep the primary message concise.
- Use `rlang::warn()` for recoverable problems and `rlang::inform()` for intentional user-facing progress or guidance. Do not turn expected control flow into warnings.
- Prefer returning a value for an expected branch when callers can handle it normally; reserve errors for contract violations or operations that cannot produce a valid result.

## Catch and handle

- Use `tryCatch()` when a handler should handle or transform a condition and return from the protected computation.
- Use `withCallingHandlers()` when observing, enriching, logging, or muffling a condition while preserving the current call stack.
- Catch the narrowest class you can handle. Never catch all errors and return `NULL` unless that fallback is explicitly part of the API.
- Add context and rethrow when crossing a boundary, preserving the original condition as a parent where the chosen condition framework supports it.
- Do not suppress warnings or messages globally to make tests or users quiet; handle the known condition at the smallest scope.

## Debugging and tests

Keep backtraces available during development. Tests should assert stable custom classes and only stable message fragments. Use `rlang::last_trace()` after an error from rlang-based code; use `traceback()` for base-R call stacks.

Read [references/conditions-and-recovery.md](references/conditions-and-recovery.md) for handler choice and [references/errors-in-tidyverse.md](references/errors-in-tidyverse.md) for data-mask and pipeline context. Use `r-testing` for the test fixture and expectation strategy.
