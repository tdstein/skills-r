# Evaluation plan

This document defines how the implemented R skills will be evaluated. No
evaluations have been run yet, so all results in this document are marked
**pending**. Empty result fields are intentional and must not be interpreted as
zero error rate, no improvement, or a completed baseline.

## Status

| Skill | Evaluation focus | Status | Results |
| --- | --- | --- | --- |
| [`r-core`](skills/r-core/) | Vector types, recycling, tibbles, missing values, and object-shape reasoning | Pending | — |
| [`r-style`](skills/r-style/) | Naming, formatting, readable pipelines, and style-boundary decisions | Pending | — |
| [`r-project-layout`](skills/r-project-layout/) | Package versus analysis-project structure and reproducible repository organization | Pending | — |
| [`r-dependencies`](skills/r-dependencies/) | `DESCRIPTION`, `renv`, lockfiles, version constraints, and environment restoration | Pending | — |
| [`r-testing`](skills/r-testing/) | `testthat`, fixtures, snapshots, mocks, and regression-test design | Pending | — |
| [`r-errors`](skills/r-errors/) | Conditions, `rlang` errors, diagnostics, backtraces, and failure boundaries | Pending | — |
| [`r-tidyverse-core`](skills/r-tidyverse-core/) | Tidy-data shape, tibbles, pipes, type semantics, and cross-skill routing | Pending | — |
| [`r-dplyr`](skills/r-dplyr/) | Grouping, summaries, joins, duplicate keys, and row multiplication | Pending | — |
| [`r-tidyr`](skills/r-tidyr/) | Pivoting, names, types, missingness, nesting, and unnesting | Pending | — |
| [`r-ggplot2`](skills/r-ggplot2/) | Aesthetic mapping versus setting, layers, statistics, scales, and coordinates | Pending | — |
| [`r-purrr`](skills/r-purrr/) | Type-stable mapping, list-columns, errors, and explicit iteration choices | Pending | — |
| [`r-readr`](skills/r-readr/) | Type inference, locales, missing values, malformed input, and parse diagnostics | Pending | — |

## Goals

The evaluation suite is intended to measure whether a skill improves observable
R work, not whether an answer repeats the wording of the skill. Each evaluation
should test at least one decision where a plausible but incorrect solution is
easy to produce.

The initial goals are:

1. Improve correctness on R and Tidyverse edge cases.
2. Preserve intended output types, shapes, grouping, and relationships.
3. Encourage current, maintainable R idioms without banning justified
   alternatives.
4. Route mixed requests to the narrowest applicable skill.
5. Keep package boundaries clear so one skill does not duplicate another.
6. Produce runnable artifacts when the prompt requests code.

## Methodology

### Test design

Each skill should have an `evals/evals.json` fixture once its implementation is
available. Cases should include:

- A realistic user prompt rather than a request to recite the skill.
- A natural trap that distinguishes robust guidance from a plausible shortcut.
- Assertions about the resulting artifact, code behavior, or routing decision.
- Enough context to make the task reproducible without requiring hidden project
  state.

Evaluation prompts should avoid testing generic R syntax that any competent
agent should know. They should target the skill's distinctive judgment, such
as duplicate-key joins, grouping retention, type stability, parsing
diagnostics, or mapping-versus-setting in a plot.

### A/B comparison

For every case, run two conditions:

1. **With skill:** the agent receives the relevant skill and directly linked
   references.
2. **Without skill:** the same agent receives the prompt without the target
   skill. Sibling skills should also be excluded unless the case explicitly
   evaluates routing across siblings.

Use the same model, prompt, repository fixture, tool permissions, and
randomness settings for both conditions. Keep each run isolated in a temporary
workspace so generated files and prior attempts cannot affect another case.

The without-skill condition is a baseline, not a claim that the agent lacks
general R knowledge. Results should report both conditions and the difference
between them.

### Assertions and grading

Prefer assertions over subjective prose quality. Depending on the skill, check:

- Code parses and runs in an isolated R environment.
- Output columns, rows, classes, dimensions, and grouping match the request.
- Joins do not silently multiply rows when the prompt implies unique keys.
- Missing values and malformed input are handled explicitly.
- Errors retain useful context and remain testable.
- Tests fail for the intended reason and pass for the correct implementation.
- The selected package and skill match the task's ownership boundary.
- Plots use the requested mapping, scale, statistic, coordinate system, and
  output behavior.
- Dependency and project changes are reproducible.

Human review is required for assertions that cannot be checked reliably by
execution alone. A reviewer should inspect the artifact and the evaluation
trace without being given the intended answer or the suspected trap.

### Reporting

When evaluations are actually run, add a result section for the relevant skill
containing:

- Date and repository revision.
- Model and evaluation configuration.
- Number of cases, runs per case, and assertion count.
- With-skill pass rate.
- Without-skill pass rate.
- Absolute and relative differences.
- Notable failures, false positives, and follow-up actions.

Do not fill a missing result with `0%`, `100%`, `—`, or an estimated value.
Use **pending** until a repeatable run and review exist.

## Scenario coverage

### Foundations

#### `r-core`

- Distinguish atomic vectors, lists, data frames, and tibbles for a requested
  operation.
- Identify unintended recycling or coercion.
- Preserve missing-value semantics and output types.
- Explain when a list-column is appropriate.

#### `r-style`

- Resolve naming and formatting choices in a mixed base R/Tidyverse file.
- Separate a style preference from a correctness requirement.
- Refactor a pipeline for readability without changing behavior.

#### `r-project-layout`

- Choose package, analysis-project, or report structure from stated
  maintenance and reproducibility needs.
- Place source, tests, data, generated artifacts, and documentation correctly.
- Identify files that should not be committed.
- Detect an analysis that relies on a saved workspace or absolute paths, and
  make it reproducible from a clean session.

#### `r-dependencies`

- Add a dependency with the correct package metadata and reproducibility
  implications.
- Choose between a project lockfile and a package dependency declaration.
- Diagnose a restore failure without silently changing unrelated versions.

#### `r-testing`

- Write a focused `testthat` regression test for a data transformation.
- Choose between an expectation, snapshot, fixture, mock, or integration test.
- Test errors and warnings without weakening the assertion.

#### `r-errors`

- Create a structured error with useful context and a stable class.
- Preserve a backtrace while adding user-facing context.
- Distinguish error handling from recovery, logging, and testing.

### Tidyverse workflow

#### `r-tidyverse-core`

- Recognize whether a requested result is tidy and identify its unit of
  observation.
- Track column types and shape across a multi-package pipeline.
- Distinguish observed missing values from structural missingness introduced by
  a reshape.
- Route a mixed request to `r-readr`, `r-tidyr`, `r-dplyr`, `r-purrr`, or
  `r-ggplot2` without duplicating package guidance.

#### `r-dplyr`

- Summarise grouped data with missing values and deliberate grouping
  retention.
- Detect duplicate keys before a join and explain unexpected row growth.
- Choose between `mutate()`, `summarise()`, `reframe()`, and a window
  operation.
- Preserve remote-table behavior when the data source is lazy.

#### `r-tidyr`

- Choose `pivot_longer()` or `pivot_wider()` from the desired observation
  unit.
- Preserve or explicitly control column types and names during a pivot.
- Handle duplicate widening keys rather than silently creating list-columns.
- Use nesting and unnesting without losing row identity.

#### `r-ggplot2`

- Distinguish an aesthetic mapping from a constant aesthetic setting.
- Decide whether a transformation belongs in data preparation, a statistic,
  or a scale.
- Choose a scale, facet, or coordinate transformation for the stated visual
  question.
- Preserve and investigate missing-value warnings, and export a named final
  plot with reproducible dimensions.
- Avoid hiding data-quality or grouping problems inside a plot call.

#### `r-purrr`

- Choose the correct `map_*()` variant for the required output type.
- Handle one failing element with an intentional error strategy.
- Work with list-columns without accidental simplification.
- Explain when vectorization or a regular loop is clearer than mapping.

#### `r-readr`

- Inspect or specify column types for ambiguous input.
- Parse dates, numbers, and locale-sensitive values deliberately.
- Configure missing values without converting valid strings accidentally.
- Surface malformed records through parse diagnostics and an appropriate
  failure policy.
- Retain source-file provenance when combining inputs, normalize source column
  names deliberately, and choose a serialization format that preserves the
  required types.

## Evaluation lifecycle

1. Implement the target skill and its directly linked references.
2. Add adversarial fixtures for the skill's distinctive decisions.
3. Validate fixture structure and run syntax checks before model evaluation.
4. Execute isolated with-skill and without-skill runs.
5. Review artifacts and assertions independently.
6. Record results in this document and update the skill's catalog status in
   [`README.md`](README.md).
7. Open follow-up work for repeated failure patterns or routing overlap.

Until this lifecycle has been completed for a skill, its status remains
**Pending**.
