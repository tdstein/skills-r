---
name: r-documentation
description: "Use to create, review, or publish R package documentation, vignettes, reports, books, and reproducible project docs, including examples, cross-references, and contribution workflows."
license: MIT
compatibility: "R 4.1+ and the documented packages; compatible with Claude Code, Cursor, Gemini CLI, Codex, and similar Agent Skills clients."
user-invocable: true
allowed-tools: "Read Edit Write Glob Grep Bash(R:*) Bash(Rscript:*) Bash(git:*) Agent"
metadata:
  author: tdstein
  version: "0.1.0"
  openclaw:
    emoji: "📚"
    homepage: "https://github.com/tdstein/skills-r"
    requires:
      bins:
        - R
        - Rscript
    install: []
---

# R documentation and publishing

Treat documentation as a maintained, reproducible artifact with a clear source
file, build command, audience, and publication target.

## Choose the documentation form

- **API documentation:** document exported functions, classes, data, and
  lifecycle contracts from roxygen2 source; let roxygen2 generate `man/` and
  `NAMESPACE` artifacts.
- **Long-form documentation:** use vignettes, Quarto, R Markdown, or bookdown
  when concepts, workflows, and rendered examples need more space.
- **Project reports:** keep analysis logic in named scripts or package
  functions and let the report orchestrate and explain the results.
- **Contributor documentation:** explain how to report confusion, fix source
  pages, propose changes, and satisfy the repository's attribution or licensing
  requirements.

## Write for reuse and verification

Make examples copyable and distinguish input from output. Use stable names,
explicit parameters, and cross-references so a reader can enter at a useful
section without losing the surrounding contract. Seed random examples or
otherwise record their inputs when output is intended to be reproducible.

Keep documentation source under version control and generated output
regenerable. Do not hand-edit generated `.Rd`, navigation, or site artifacts
when a source file or build configuration owns them. Review rendered output,
links, warnings, and code execution in a clean session.

## Reproducible publishing

Make the build environment explicit: record the R version and relevant package
versions, repositories, and system assumptions. Keep rendering dependencies
separate from package runtime dependencies, while declaring package examples
and vignette dependencies correctly. If publishing is automated, build from a
known commit and make the CI or hosting step observable and repeatable.

Include session information or an equivalent environment record when it is part
of the reproducibility claim. Keep external data and network-dependent examples
out of ordinary package examples unless the workflow explicitly controls them.

## Routing

- Use `r-project-layout` for where source, generated documentation, reports, and
  publishing artifacts live.
- Use `r-dependencies` for `DESCRIPTION`, `Suggests`, lockfiles, repositories,
  and rendering environments.
- Use `r-connections` for file, URL, pipe, socket, text, and binary I/O.
- Use `r-testing` for testing examples, vignettes, and rendered workflows.
