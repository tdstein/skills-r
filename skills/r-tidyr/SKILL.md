---
name: r-tidyr
description: Use when an R task changes the shape or nesting of tidy data with pivot_longer(), pivot_wider(), separate/unite, nest, unnest, or rectangling. Apply for row/column representation and list-column structure; use r-dplyr for values and relationships and r-readr for file parsing.
license: MIT
compatibility: "R 4.1+ and the documented packages; compatible with Claude Code, Cursor, Gemini CLI, Codex, and similar Agent Skills clients."
user-invocable: true
allowed-tools: "Read Grep Glob Bash(R:*) Bash(Rscript:*)"
metadata:
  author: "samber"
  version: "0.1.0"
  openclaw:
    emoji: "🧩"
    homepage: "https://github.com/samber/cc-skills-r"
    requires:
      bins:
        - R
        - Rscript
    install: []
---

# tidyr data shape

Use tidyr when the observational unit or representation of a table changes. State the input grain and desired output grain before choosing a verb.

## Workflow

1. Identify identifier columns, measured-value columns, and metadata encoded in names.
2. Choose `pivot_longer()` to increase rows and reduce columns, or `pivot_wider()` to increase columns and reduce rows.
3. Make name parsing explicit with `names_sep`, `names_pattern`, `names_prefix`, or `names_glue`.
4. Specify `values_transform`, `names_transform`, or prototypes when type inference is not sufficient.
5. Decide how duplicate combinations are summarized in `pivot_wider()`; do not accept list-columns accidentally.
6. Use `nest()`/`unnest()` only when a list-column is part of the intended data model.
7. Verify row count, key uniqueness, column names, and types after reshaping.

## Boundaries

- tidyr changes representation; dplyr changes values, rows, columns, and relationships within a representation.
- Use `separate_wider_*()`/`separate_longer_*()` for current splitting operations; use `unite()` when combining columns.
- Use `unnest_longer()` or `unnest_wider()` when a list-column is structured data; use `unnest()` for data-frame columns.
- Do not use `pivot_wider()` as a general aggregation shortcut without specifying or checking `values_fn`.
- Do not use `drop_na()` as a substitute for understanding why a pivot produced missing cells.

Read [references/pivoting.md](references/pivoting.md) for pivot design and duplicate-cell handling. Read [references/list-columns.md](references/list-columns.md) for nesting, unnesting, and rectangling.
