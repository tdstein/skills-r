---
name: r-project-layout
description: "Use when creating, reviewing, or reorganizing an R package, analysis project, report, or reproducible workspace. Apply to decisions about R/, tests, data-raw, vignettes, Quarto/R Markdown, and project boundaries. For dependency locking use r-dependencies."
license: MIT
compatibility: "R 4.1+ and the documented packages; compatible with Claude Code, Cursor, Gemini CLI, Codex, and similar Agent Skills clients."
user-invocable: true
allowed-tools: "Read Edit Write Glob Grep Bash(R:*) Bash(Rscript:*) Bash(git:*) Agent"
metadata:
  author: samber
  version: "0.1.0"
  openclaw:
    emoji: "🗂️"
    homepage: "https://github.com/samber/cc-skills-r"
    requires:
      bins:
        - R
        - Rscript
    install: []
---

# R project layout

Choose the layout from the deliverable first. A distributable package, an analysis project, and a report have different contracts; do not force package scaffolding onto an exploratory script or leave a package as an unstructured notebook collection.

## Choose a project shape

- **R package:** use when code has reusable functions, a public API, tests, metadata, or distribution requirements.
- **Analysis project:** use for a bounded analysis, data pipeline, dashboard, or research project that may not be a package.
- **Report/document:** use when the primary artifact is a rendered Quarto or R Markdown document; keep reusable data preparation and modeling code in scripts or a package rather than hiding everything in chunks.
- **Mixed project:** use a package for reusable logic plus a separate `analysis/`, `reports/`, or `inst/` area for project-specific execution. Keep the dependency and ownership boundaries explicit.

## Package baseline

Start a package with `DESCRIPTION`, `NAMESPACE` (usually generated), `R/`, `tests/testthat.R`, `tests/testthat/`, and documentation source. Add `man/` and `vignettes/` when generated documentation or long-form examples are part of the deliverable. Keep generated files generated; do not hand-edit `NAMESPACE` or `.Rd` files when roxygen2 owns them.

Use `data-raw/` for reproducible scripts that create package data. Store small package data under `data/` only when it is an intentional package asset and document it.

## Analysis baseline

Keep an analysis project organized around data stages or deliverables, for example:

```text
analysis/
data-raw/
data/
R/
reports/
figures/
```

Use a project root detected by `here` or an equivalent explicit path strategy. Avoid `setwd()` inside functions and reports. Keep raw data immutable when possible, and record how derived data was produced.

## Routing

- Read [references/package-layout.md](references/package-layout.md) for package files and generated artifacts.
- Read [references/analysis-layout.md](references/analysis-layout.md) for scripts, reports, data, and reproducibility boundaries.
- Use `r-dependencies` for `DESCRIPTION`, `renv.lock`, and dependency resolution; use `r-testing` for test placement and test tiers.
