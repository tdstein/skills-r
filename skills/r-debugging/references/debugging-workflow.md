# Debugging workflow

## Tool selection

| Symptom | First tool | What to inspect |
| --- | --- | --- |
| Ordinary error | `traceback()` | Call sequence, read from the initial caller toward the failing call |
| rlang error or lazy evaluation | `rlang::last_trace()` | Branching call tree and the last evaluated argument |
| Need local values | `browser()` or breakpoint | Current frame, promises, and the next expression |
| Warning | `options(warn = 2)` locally | The stack at the warning site |
| Message | Promote that message locally | The stack that emitted the message |
| Batch-only error | `dump.frames(to.file = TRUE)` | Saved frames in a later interactive session |
| Environment mismatch | `callr::r()` | Fresh global environment, search path, directory, and library paths |
| Hang or crash | print markers, then native debugger | Last completed phase and compiled-code boundary |

Read stack displays according to their tool: base `traceback()` starts with
the original call at the bottom, while `rlang::last_trace()` presents a
hierarchical tree. Ignore internal condition/restart frames until the
application frames are understood.

## Safe investigation

Keep temporary `options(error = ...)`, `options(warn = ...)`, breakpoints,
traces, and `browser()` calls local to the investigation. Restore options and
remove instrumentation before committing code. Do not add logging that leaks
secrets or large inputs merely to make a failure visible.

When a failure only appears in an automated job, compare the fresh process with
the interactive session: attached packages, objects in the global environment,
working directory, `PATH`, `R_LIBS`, input files, locale, and package versions.
Capture those differences in the minimal reproducer rather than assuming the
interactive session is authoritative.

## R Markdown

Render explicitly with `rmarkdown::render()` when the IDE knitting path hides
the session differences. For interactive recovery from a knitr error, an
error handler may need to call `sink()` before `recover()` so the debugger
output reaches the console. For a focused non-interactive trace, set
`rlang_trace_top_env` and print `rlang::trace_back()` from the error handler.

## Further reading

- [Debugging in Advanced R](https://adv-r.hadley.nz/debugging.html)
- [Conditions and recovery](https://adv-r.hadley.nz/conditions.html)
