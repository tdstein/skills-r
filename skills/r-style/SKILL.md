---
name: r-style
description: "Use for R naming, formatting, comments, pipelines, function layout, and Tidyverse style; improve readability without changing behavior."
license: MIT
compatibility: "R 4.1+ and the documented packages; compatible with Claude Code, Cursor, Gemini CLI, Codex, and similar Agent Skills clients."
user-invocable: true
allowed-tools: "Read Edit Write Glob Grep Bash(R:*) Bash(Rscript:*) Bash(git:*) Agent"
metadata:
  author: tdstein
  version: "0.1.0"
  openclaw:
    emoji: "🖊️"
    homepage: "https://github.com/tdstein/cc-skills-r"
    requires:
      bins:
        - R
        - Rscript
    install: []
---

# R style

Write R that is easy to scan, diff, test, and extend. Prefer the local project convention when it is consistent and documented; otherwise use the tidyverse style guide and let formatters enforce mechanical details.

## Naming and layout

- Use `snake_case` for functions, variables, and file names. Use descriptive nouns for data and verbs for transformations.
- Name predicate functions with a clear question or property, such as `is_valid_id()` or `has_missing()`.
- Keep one primary function or cohesive small group per source file in packages; name files after the public concept, not an arbitrary ticket.
- Use explicit namespaces in package code when ownership is unclear or a dependency is in `Suggests`.
- Keep functions small enough that input contract, transformation, and return value are visible without scrolling through unrelated helpers.

## Expressions and pipelines

- Break long calls one argument per line when that improves reviewability; use trailing commas only where the project formatter supports them consistently.
- Use a pipeline when each step transforms the previous result. Do not pipeline unrelated side effects or hide important branching in a long chain.
- Prefer `|>` for base-R code and `%>%` where tidyverse conventions or magrittr placeholders add real value. Do not mix pipe styles casually in one file.
- Keep joins, filters, and summaries close to the point where their assumptions are visible. Name intermediate data when it clarifies grain or prevents repeated computation.
- Put `library()` calls in scripts or interactive entrypoints, not inside reusable functions.
- Keep a shared analysis script reproducible from a fresh session: capture setup, inputs, and generated outputs in code instead of relying on objects in the global environment or console history.

## Comments and review

- Comment why a non-obvious choice is required, especially around type coercion, grouping, database translation, or statistical assumptions.
- Do not comment every obvious verb. Replace stale explanatory comments with clearer code.
- Document exported package functions with roxygen2; keep examples short and runnable.
- Avoid commented-out code, hidden global state, and unqualified `setwd()` in reusable code.

## Tooling and routing

- Run `styler::style_file()` or `styler::style_pkg()` for mechanical formatting when the project uses styler.
- Run `lintr::lint_package()` or the repository's configured lint command for review feedback; do not use lint suppressions to hide design problems.
- Read [references/style-review.md](references/style-review.md) for review heuristics and [references/package-code-style.md](references/package-code-style.md) for package-specific conventions.
- Use `r-core` for type/evaluation semantics, `r-project-layout` for directory decisions, and `r-testing` for test organization.
