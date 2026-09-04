---
name: r-dplyr
description: "Use for dplyr table transformations: filter, select, mutate, summarise, group, join, and column-wise operations; use tidyr for table shape."
license: MIT
compatibility: "R 4.1+ and the documented packages; compatible with Claude Code, Cursor, Gemini CLI, Codex, and similar Agent Skills clients."
user-invocable: true
allowed-tools: "Read Grep Glob Bash(R:*) Bash(Rscript:*)"
metadata:
  author: "tdstein"
  version: "0.1.0"
  openclaw:
    emoji: "🔧"
    homepage: "https://github.com/tdstein/skills-r"
    requires:
      bins:
        - R
        - Rscript
    install: []
---

# dplyr data transformation

Use dplyr verbs to express a small number of explicit table transformations. Before coding, identify the input table, intended row grain, key columns, and whether the result should remain grouped.

## Workflow

1. Inspect names, types, row counts, and candidate keys.
2. Use `filter()` for rows, `select()`/`relocate()` for columns, `mutate()` for derived columns, and `arrange()` for order.
3. Use `summarise()` only when reducing rows per group; use `reframe()` when a group may return multiple rows.
4. Use `across()` for repeated column-wise work instead of superseded scoped verbs.
5. Make missing-value policy explicit in summaries and predicates; pair an aggregate with `n()` when sample size changes its interpretation.
6. For joins, write the relationship in words first, use `join_by()`, and validate expected key cardinality.
7. Inspect output row count, key uniqueness, types, and grouping before handing the result to another skill.

## Important constraints

- A join can multiply rows when either side has duplicate matching keys. Do not call `distinct()` afterward unless duplicates are genuinely redundant and the loss is understood.
- Prefer `relationship =` and `unmatched =` checks where the expected relationship is known; use `na_matches =` deliberately when missing keys matter.
- Use `.by` for a one-off grouped operation when retaining grouping metadata is undesirable; use `group_by()` when several subsequent operations intentionally share groups.
- `filter()` keeps only `TRUE` rows, so an `NA` predicate drops the row. State whether missing values should be retained with an explicit `is.na()` condition.
- Use `.data` and `.env` in reusable functions when data columns and environment variables may collide.
- Prefer `pick()`/`across()` and current join helpers over deprecated scoped verbs and legacy `*_join` workarounds.
- Keep database translation concerns in `dbplyr`; dplyr owns the expression, not connection management or SQL-specific tuning.

Read [references/joins-and-groups.md](references/joins-and-groups.md) for cardinality, grouping, and summary decisions. Read [references/column-wise-and-programming.md](references/column-wise-and-programming.md) for `across()`, tidy selection, and reusable functions.
