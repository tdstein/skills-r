---
name: r-purrr
description: Use when an R task maps functions over vectors, lists, data frames, or list-columns, needs type-stable iteration, safely handles per-element failures, or uses map2/pmap/possibly/safely. Apply for functional iteration; use r-dplyr for column transformations and r-tidyr for table shape.
license: MIT
compatibility: "R 4.1+ and the documented packages; compatible with Claude Code, Cursor, Gemini CLI, Codex, and similar Agent Skills clients."
user-invocable: true
allowed-tools: "Read Grep Glob Bash(R:*) Bash(Rscript:*)"
metadata:
  author: "samber"
  version: "0.1.0"
  openclaw:
    emoji: "🔁"
    homepage: "https://github.com/samber/cc-skills-r"
    requires:
      bins:
        - R
        - Rscript
    install: []
---

# purrr functional iteration

Use purrr when the unit of work is applying a function to each element, especially when inputs or outputs are lists, heterogeneous objects, or list-columns.

## Choose the right tool

- Use `map()` for a list result, `map_chr()`, `map_int()`, `map_dbl()`, and `map_lgl()` when every result must be length one and the type is part of the contract.
- Use `map_vec()` when results are simple vectors and a common type should be determined.
- Use `map2()` or `pmap()` when each iteration consumes multiple aligned inputs; validate lengths and names.
- Use `imap()` when the element name or index is part of the computation.
- Use `walk()`/`pwalk()` for side effects when the input, not the side-effect result, should flow onward.
- Use `possibly()` when a fallback value is a valid result, `safely()` when callers need both result and error, and `quietly()` when output/messages must be captured.

## Reliability rules

- Prefer an explicit anonymous function `\(x) ...` for nontrivial work; do not rely on formula shortcuts in new code.
- Keep outputs type-stable. If failures are possible, choose a typed fallback or return a structured result that records the error.
- Expect purrr to annotate indexed errors; preserve that context when reporting or rethrowing.
- Do not use purrr merely to replace a simple vectorized operation or a dplyr `across()` transformation.
- `in_parallel()` is an explicit execution choice, not a synonym for `pmap()`. It also requires `carrier` (version 0.3.0 or newer); use it only when the function is self-contained, dependencies are explicit, and parallel overhead is justified.

Read [references/type-safety-and-errors.md](references/type-safety-and-errors.md) for typed mapping and failure handling. Read [references/parallel-and-side-effects.md](references/parallel-and-side-effects.md) when mapping performs I/O or parallel work.
