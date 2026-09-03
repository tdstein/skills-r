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
- Treat `message` as a side channel for progress or user guidance, not as the primary output of a function. Provide a deliberate way to quiet routine messages when appropriate.
- Keep condition classes stable and specific. Store machine-readable fields on custom conditions instead of forcing callers to parse message text; keep user wording free to improve.

## Catch and handle

- Use `tryCatch()` when a handler should handle or transform a condition and return from the protected computation.
- Use `withCallingHandlers()` when observing, enriching, logging, or muffling a condition while preserving the current call stack.
- Catch the narrowest class you can handle. Never catch all errors and return `NULL` unless that fallback is explicitly part of the API.
- When several `tryCatch()` handlers could match, put the most specific class first; matching uses the first applicable handler, not the best class automatically.
- Add context and rethrow when crossing a boundary, preserving the original condition as a parent where the chosen condition framework supports it.
- Use `cnd_muffle()` or the applicable muffle restart only for a known condition and an intentional policy. Do not suppress warnings or messages globally to make tests or users quiet.
- For cleanup, register `on.exit()` immediately after acquiring a resource; use `tryCatch(finally = ...)` for cleanup around a smaller protected expression.

## Recovery protocols

- Keep detection, recovery mechanisms, and recovery policy separate when a lower-level function can offer more than one valid response. Put local recovery actions in `withRestarts()` and let higher-level `withCallingHandlers()` code choose with `invokeRestart()`.
- Name restarts after the recovery action and pass only the arguments needed by that action. Use `findRestart()` when a handler may run outside the context that provides the restart; otherwise avoid inventing a fallback.
- Use calling handlers for protocols that should continue at the signaling site, such as recording or promoting warnings. Use exiting handlers when the protected computation must be abandoned.
- A condition that is neither an error, warning, nor message can be a deliberate event protocol with no default behavior; add a handler where that protocol is consumed.
- Be cautious with interrupt handlers: catching an interrupt can cause execution to continue in a state the user explicitly tried to stop.

## Debugging and tests

Keep backtraces available during development. Use `rlang::last_trace()` after an error from rlang-based code and `traceback()` for base-R call stacks; use the debugging skill for a systematic diagnosis workflow and interactive or batch investigation.

Tests should assert stable custom classes and structured fields, plus only stable message fragments when wording is part of the user contract. Use the testing skill for regression-test design, fixtures, and condition expectations.

Read [references/conditions-and-recovery.md](references/conditions-and-recovery.md) for handler choice and [references/errors-in-tidyverse.md](references/errors-in-tidyverse.md) for data-mask and pipeline context. Use `r-testing` for the test fixture and expectation strategy.
