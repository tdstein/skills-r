---
name: r-dependencies
description: "Use to declare, lock, upgrade, or audit R package dependencies with DESCRIPTION, NAMESPACE, renv, pak, and lockfiles."
license: MIT
compatibility: "R 4.1+ and the documented packages; compatible with Claude Code, Cursor, Gemini CLI, Codex, and similar Agent Skills clients."
user-invocable: true
allowed-tools: "Read Edit Write Glob Grep Bash(R:*) Bash(Rscript:*) Bash(git:*) Agent"
metadata:
  author: tdstein
  version: "0.1.0"
  openclaw:
    emoji: "📦"
    homepage: "https://github.com/tdstein/cc-skills-r"
    requires:
      bins:
        - R
        - Rscript
    install: []
---

# R dependencies

Treat dependencies as declared, reproducible inputs rather than packages that happen to be installed in one developer's library.

## Identify the dependency contract

Keep three contracts distinct:

- A package's `DESCRIPTION` and generated `NAMESPACE` describe what its code
  needs and what it exposes.
- An analysis or documentation project's lockfile describes the resolved
  environment used to run that project.
- A build or publishing workflow may need additional tools for rendering,
  examples, vignettes, or site generation; declare those separately from
  runtime imports.

Do not make a project lockfile substitute for package metadata, and do not
hide undeclared dependencies behind an interactive session or a broad
development environment.

## Package declarations

- Put runtime packages required by package code in `Imports` (or `Depends` only when attachment is intentionally part of the API).
- Put optional test, vignette, example, or development-only packages in `Suggests`, and guard optional code with `requireNamespace()` or appropriate test skips.
- Use version constraints only when a known API or behavior requires them; explain the constraint in project documentation or a comment.
- Regenerate `NAMESPACE` through roxygen2 after changing imports. Do not rely on `library()` in a development session to make package code work.
- Keep `DESCRIPTION` fields syntactically valid and run `R CMD check` after dependency changes.

## Environments and lockfiles

- Use `renv` when a project needs reproducible package versions across machines or time. Commit `renv.lock` when the project policy treats it as the source of environment truth.
- Use `pak` or the project's established installer for resolution and installation; do not add `install.packages()` calls to reusable code, tests, or reports.
- Separate package metadata dependencies from an analysis project's resolved environment. A package's `DESCRIPTION` is not replaced by an `renv.lock`.
- Record repositories and external sources when dependencies come from GitHub, R-universe, Bioconductor, or local paths. Pin an immutable commit, tag, or release when practical.
- Record the R version, repository configuration, and relevant system/toolchain
  assumptions when they affect reproducibility. A package list without its
  resolution context is not a complete environment description.

## Upgrade and removal workflow

Search direct imports and examples before removing a dependency. Upgrade the smallest relevant set, run tests and checks, inspect lockfile changes, and document behavior changes when an API or default has shifted. Do not solve conflicts by deleting the lockfile or widening every version constraint.

## Routing

- Read [references/package-dependency-workflow.md](references/package-dependency-workflow.md) for `DESCRIPTION`, `NAMESPACE`, and package checks.
- Read [references/reproducible-environments.md](references/reproducible-environments.md) for renv/pak and analysis environments.
- Use `r-project-layout` for where package, analysis, and build artifacts live.
- Use `r-documentation` for documentation dependencies, rendered outputs, and publishing metadata.
- Use `r-testing` for dependency-isolated tests.
