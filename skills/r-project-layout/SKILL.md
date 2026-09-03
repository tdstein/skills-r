---
name: r-project-layout
description: "Use to design or reorganize R packages, analysis projects, reports, and reproducible workspaces, including R/, tests, Quarto, and R Markdown."
license: MIT
compatibility: "R 4.1+ and the documented packages; compatible with Claude Code, Cursor, Gemini CLI, Codex, and similar Agent Skills clients."
user-invocable: true
allowed-tools: "Read Edit Write Glob Grep Bash(R:*) Bash(Rscript:*) Bash(git:*) Agent"
metadata:
  author: tdstein
  version: "0.1.0"
  openclaw:
    emoji: "🗂️"
    homepage: "https://github.com/tdstein/cc-skills-r"
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

## Make the project the source of truth

Design the tree so a clean session can rebuild derived data, figures, tests, and
documents from version-controlled source. Distinguish source files from
generated artifacts, record the inputs and commands that produce derived
outputs, and keep transient build output out of the source tree unless the
project deliberately publishes it.

Use version control for code, project metadata, documentation source, and
reproducibility configuration. Prefer explicit project-root paths, stable
machine-readable names, and deterministic seeds or parameters over hidden
session state. When the project has meaningful performance or debugging work,
give benchmarks, profiles, and diagnostic fixtures an intentional home and
keep them separate from production outputs.

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

Treat scripts and their input data as the source of truth: a clean R session must be able to recreate derived data, figures, and reports without objects from a previous interactive session. Use a project root detected by `here` or an equivalent explicit path strategy. Avoid `setwd()` inside functions and reports, and use relative paths rather than machine-specific absolute paths. Keep raw data immutable when possible, record how derived data was produced, and write generated artifacts to named locations.

Name files so they are machine readable, describe their contents, and sort in execution order where that order matters, for example `01-import.R`, `02-clean.R`, and `report-2026-09-03.qmd`. Do not use spaces, case-only distinctions, or vague names such as `final.R` and `temp.R`.

## Routing

- Read [references/package-layout.md](references/package-layout.md) for package files and generated artifacts.
- Read [references/analysis-layout.md](references/analysis-layout.md) for scripts, reports, data, and reproducibility boundaries.
- Use `r-dependencies` for `DESCRIPTION`, `renv.lock`, repositories, and dependency resolution.
- Use `r-documentation` for documentation content, examples, rendering, publishing, and contribution workflows.
- Use `r-connections` for connection lifecycle and external I/O mechanics.
- Use `r-testing` for test placement and test tiers.
