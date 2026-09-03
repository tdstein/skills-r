---
name: r-core
description: "Use for R code that depends on vectors, tibbles, data frames, missing values, recycling, pipes, or tidy evaluation. Apply when choosing R object types or explaining shared tidyverse semantics. For package structure, use r-project-layout; for style, use r-style."
license: MIT
compatibility: "R 4.1+ and the documented packages; compatible with Claude Code, Cursor, Gemini CLI, Codex, and similar Agent Skills clients."
user-invocable: true
allowed-tools: "Read Edit Write Glob Grep Bash(R:*) Bash(Rscript:*) Bash(git:*) Agent"
metadata:
  author: samber
  version: "0.1.0"
  openclaw:
    emoji: "🧭"
    homepage: "https://github.com/samber/cc-skills-r"
    requires:
      bins:
        - R
        - Rscript
    install: []
---

# R core

Treat R objects and their invariants as part of the interface. Prefer code whose input, output, missingness, and size behavior are explicit.

## Working rules

- Distinguish atomic vectors, lists, matrices, data frames, and tibbles before choosing an operation. A tibble is a data frame with stricter printing and subsetting behavior; it is not a replacement for every matrix or list.
- Check vector size and type deliberately. R recycles shorter vectors in many operations, but accidental recycling can silently produce wrong results. Use explicit length checks or `vctrs` helpers at boundaries where sizes must agree.
- Preserve missingness intentionally. `NA` is typed and propagates through many computations; use `is.na()`, `anyNA()`, `na.rm`, or explicit imputation rather than treating it as an empty string or zero.
- Prefer `[[` for extracting one element and `[` for preserving a collection. Use `drop = FALSE` when matrix or data-frame dimensionality must remain stable.
- Prefer `|>` for straightforward base-R pipelines. Use `%>%` only when the surrounding project already uses it or when magrittr-specific features are required.
- Keep transformations explicit about evaluation context. In tidyverse verbs, bare column names are data-masked expressions; external values should usually be named variables or injected with the appropriate tidy-evaluation mechanism.
- Preserve names and classes when they carry meaning. Avoid coercing a tibble to a matrix or character vector merely to pass it to a function without checking the resulting loss of structure.
- Make output shape part of the contract: state whether a function returns one value, one row per group, a vector matching input size, or a tibble.

## Routing

- Read [references/tidy-data-and-types.md](references/tidy-data-and-types.md) when data shape, vector coercion, recycling, or missingness is consequential.
- Read [references/tidy-evaluation.md](references/tidy-evaluation.md) when writing functions around dplyr/tidyr verbs, embracing column arguments, or constructing expressions.
- Use `r-style` for formatting and naming decisions, `r-testing` for behavioral verification, and `r-errors` for condition design.

## Verification

For non-trivial transformations, test representative zero-row, one-row, missing-value, and mixed-type inputs. Check both `typeof()`/class and dimensions, not only printed output.
