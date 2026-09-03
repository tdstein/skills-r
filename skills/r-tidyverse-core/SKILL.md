---
name: r-tidyverse-core
description: "Use for shared Tidyverse data-shape, tibble, pipe, type, grouping, and tidy-evaluation decisions; route package-specific work to sibling skills."
license: MIT
compatibility: "R 4.1+ and the documented packages; compatible with Claude Code, Cursor, Gemini CLI, Codex, and similar Agent Skills clients."
user-invocable: true
allowed-tools: "Read Grep Glob Bash(R:*) Bash(Rscript:*)"
metadata:
  author: "samber"
  version: "0.1.0"
  openclaw:
    emoji: "🧹"
    homepage: "https://github.com/samber/cc-skills-r"
    requires:
      bins:
        - R
        - Rscript
    install: []
---

# Tidyverse core

Use this skill for the shared grammar and data model behind tidyverse code. Keep the result explicit about the input shape, output shape, column types, missingness, and grouping state.

## Working rules

- Treat tidy data as one observation per row, one variable per column, and one observational unit per table. If the task changes table shape, route to `r-tidyr`.
- Prefer tibbles for rectangular data. Preserve useful names and avoid converting to a bare matrix or silently dropping dimensions.
- Use the native pipe `|>` for ordinary function composition. Use `%>%` only when existing code or a package-specific feature requires it.
- Keep transformations in the package that owns them: `r-dplyr` for rows, columns, values, and joins; `r-tidyr` for shape; `r-ggplot2` for plots; `r-purrr` for mapping; `r-readr` for file parsing.
- Inspect types with `str()`, `dplyr::glimpse()`, `vctrs::vec_ptype()`, or targeted assertions before relying on implicit coercion.
- Make missing-value behavior explicit. `NA` is not the same as `NULL`, an empty character value, or a missing column.
- Preserve grouping intentionally. After a grouped operation, inspect `dplyr::group_vars()` and use `.groups` or `ungroup()` when downstream code must not inherit grouping.
- Use tidy evaluation only where it improves a reusable interface. In package functions, distinguish data-masked arguments from ordinary strings and use `.data`/`.env` pronouns when ambiguity is possible.

## Routing

- Read [references/types-and-shapes.md](references/types-and-shapes.md) when a task involves coercion, recycling, list-columns, grouping, or deciding which sibling package owns a transformation.
- Read [references/tidy-evaluation.md](references/tidy-evaluation.md) when writing reusable functions with data-masked arguments, tidy selection, or dynamic column names.
- Do not turn this skill into a general R style guide, statistical modeling guide, database guide, or visualization guide.
