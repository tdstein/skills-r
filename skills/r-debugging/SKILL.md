---
name: r-debugging
description: "Use to diagnose unexpected R errors, warnings, messages, hangs, and crashes with reproducible examples, tracebacks, interactive debugging, and non-interactive diagnostics; use r-errors for condition design and r-testing for regression tests."
license: MIT
compatibility: "R 4.1+ and the documented packages; compatible with Claude Code, Cursor, Gemini CLI, Codex, and similar Agent Skills clients."
user-invocable: true
allowed-tools: "Read Edit Write Glob Grep Bash(R:*) Bash(Rscript:*) Bash(git:*) Agent"
metadata:
  author: tdstein
  version: "0.1.0"
  openclaw:
    emoji: "🐞"
    homepage: "https://github.com/tdstein/skills-r"
    requires:
      bins:
        - R
        - Rscript
    install: []
---

# R debugging

Find the smallest reproducible cause of an unexpected R failure, confirm the
hypothesis, and leave a regression test when the behavior belongs in a
maintained codebase.

## Debugging loop

1. Make the failure repeatable. Record the exact input, R/package versions,
   session state, working directory, environment variables, and whether the
   failure is interactive or batch-only.
2. Minimise the example and data while preserving the failure. Keep examples
   that do not fail: contrasts often reveal the violated assumption.
3. Form a concrete hypothesis, change one relevant factor, and record the
   result. Use experiments instead of speculative patches.
4. Fix the root cause, rerun the reproducer, and add a focused regression test
   plus nearby tests for behavior that must remain valid.

## Locate the failure

- After an error, inspect `traceback()` from the bottom upward. For rlang
  errors or lazy-evaluation-heavy code, use `rlang::with_abort()` and
  `rlang::last_trace()` to preserve the call tree.
- Use `browser()` or an IDE breakpoint to inspect local state at the point of
  interest. `n`, `s`, `f`, `c`, and `Q` step, enter, finish, continue, and quit.
  Use `debugonce()` for a one-run pause and `undebug()` when finished.
- Use `options(error = recover)` to choose a frame interactively, and restore
  normal behavior with `options(error = NULL)`. Do not leave debugging options
  in package or shared-session code.
- Use `options(warn = 2)` to turn an unexpected warning into an error. To
  diagnose a suspicious message, promote it locally with an appropriate
  condition handler. Restore options after the investigation.

## Non-interactive failures

- Reproduce in a fresh process with `callr::r()` or an equivalent clean session
  when global objects, attached packages, directories, `PATH`, or `R_LIBS` may
  differ.
- In batch code, `dump.frames(to.file = TRUE)` can save frames for a later
  `load()` and `debugger()` session. Use print debugging with coarse markers
  first, then add values and finer-grained markers.
- For R Markdown or knitr failures, render explicitly with
  `rmarkdown::render()`. If interactive debugging is needed, remove knitr's
  output sink in the error handler; use a bounded `rlang::trace_back()` when a
  focused trace is enough.
- A hang, non-returning function, or complete R crash is a distinct failure
  mode. Terminate safely, preserve the smallest reproducer, and use print
  diagnostics or a native debugger for compiled C/C++ code.

## Boundaries

- Use `r-errors` to decide what a function should signal, which condition class
  callers should consume, and how recovery or restarts are designed.
- Use `r-testing` to turn a confirmed bug into a stable regression test and to
  test public warning/error behavior.
- Do not treat a debugger as a substitute for making new code small,
  testable, and repeatable.

Read [references/debugging-workflow.md](references/debugging-workflow.md) for
tool selection and batch/R Markdown recipes. The source synthesis is based on
[Debugging in Advanced R](https://adv-r.hadley.nz/debugging.html).
