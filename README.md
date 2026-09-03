# Agent Skills for R and Tidyverse projects

Reusable Agent Skills for R development, reproducible analysis, and the
Tidyverse data workflow. Skills are loaded on demand so an agent can receive
focused R guidance without loading an entire language manual into every task.

This repository is an R counterpart to
[`samber/cc-skills-golang`](https://github.com/samber/cc-skills-golang). The
initial collection contains 12 implemented skills. Evaluation results remain
pending until the independent evaluation lifecycle is completed.

## How to use

### Skills CLI

The universal [`skills`](https://skills.sh/) CLI is the recommended
installation method for any Agent Skills-compatible client:

```bash
npx skills add https://github.com/tdstein/cc-skills-r --all
# or install one skill:
npx skills add https://github.com/tdstein/cc-skills-r --skill r-dplyr
```

Install the complete collection when work crosses import, transformation,
visualization, and testing boundaries. Install a subset when a project needs a
narrower context.

### Claude Code

If the repository is published through a compatible marketplace, use that
marketplace's install command. Otherwise, clone it into a Claude-discoverable
skills directory:

```bash
git clone https://github.com/tdstein/cc-skills-r.git ~/.claude/skills/cc-skills-r
```

### OpenClaw

Clone the repository into either supported discovery directory:

```bash
git clone https://github.com/tdstein/cc-skills-r.git ~/.openclaw/skills/cc-skills-r
# or, for a workspace installation:
git clone https://github.com/tdstein/cc-skills-r.git ~/.openclaw/workspace/skills/cc-skills-r
```

### Gemini CLI

Install the extension directly:

```bash
gemini extensions install https://github.com/tdstein/cc-skills-r
```

Update an existing installation with:

```bash
gemini extensions update cc-skills-r
```

### Cursor

Clone into Cursor's cross-client discovery directory:

```bash
git clone https://github.com/tdstein/cc-skills-r.git ~/.cursor/skills/cc-skills-r
```

Cursor also discovers project-local skills from `.agents/skills/` and
`.cursor/skills/`.

### GitHub Copilot

Use the plugin command when supported by the Copilot client:

```text
/plugin install https://github.com/tdstein/cc-skills-r
```

Or clone into Copilot's discovery directory:

```bash
git clone https://github.com/tdstein/cc-skills-r.git ~/.copilot/skills/cc-skills-r
```

Copilot discovers skills from `.copilot/skills/`.

### OpenCode

Clone into a supported shared discovery directory:

```bash
git clone https://github.com/tdstein/cc-skills-r.git ~/.agents/skills/cc-skills-r
```

OpenCode discovers skills from `.agents/skills/`, `.opencode/skills/`, and
`.claude/skills/`.

### Codex

Clone into the shared Agent Skills directory:

```bash
git clone https://github.com/tdstein/cc-skills-r.git ~/.agents/skills/cc-skills-r
```

Codex discovers skills from `~/.agents/skills/` and project-local
`.agents/skills/`. Update a clone with:

```bash
cd ~/.agents/skills/cc-skills-r && git pull
```

### Antigravity

Clone into Antigravity's discovery directory:

```bash
git clone https://github.com/tdstein/cc-skills-r.git ~/.antigravity/skills/cc-skills-r
```

The exact discovery behavior can vary by client version. Prefer the universal
`skills` CLI when available, and use each client's native discovery directory
when installing manually.

## Skill catalog

The initial skills are atomic, cross-referencing units. Each skill should own
one coherent concern, state when it should trigger, and identify neighboring
skills that should handle adjacent concerns.

Status legend:

- **Implemented** — the skill directory and `SKILL.md` are available;
  evaluation is pending.
- **Evaluated** — the skill has a recorded evaluation result in
  [`EVALUATIONS.md`](EVALUATIONS.md).

All initial skills are Implemented. Evaluation status is tracked separately in
[`EVALUATIONS.md`](EVALUATIONS.md).

### R foundations

| Skill | Status | Responsibility | Trigger examples |
| --- | --- | --- | --- |
| [`r-core`](skills/r-core/) | Implemented | R vectors, data frames, tibbles, recycling, missing values, pipes, and shared language semantics | Choosing an R object type, understanding vector behavior, or deciding how a tidy workflow should represent data |
| [`r-style`](skills/r-style/) | Implemented | Readable R naming, formatting, project conventions, and Tidyverse style | Reviewing style, naming objects, formatting code, or choosing between equivalent idioms |
| [`r-project-layout`](skills/r-project-layout/) | Implemented | R package, analysis-project, Quarto/R Markdown, and reproducible project structure | Starting or reorganizing an R project, package, report, or analysis repository |
| [`r-dependencies`](skills/r-dependencies/) | Implemented | `DESCRIPTION`, `renv`, lockfiles, dependency selection, and reproducible package environments | Adding packages, pinning versions, restoring an environment, or auditing dependencies |
| [`r-testing`](skills/r-testing/) | Implemented | `testthat`, fixtures, snapshots, mocking, integration tests, and reproducible test design | Writing or reviewing R tests, diagnosing flaky tests, or adding regression coverage |
| [`r-errors`](skills/r-errors/) | Implemented | Conditions, `rlang` errors, structured diagnostics, backtraces, and user-facing failure messages | Designing errors, wrapping failures, inspecting backtraces, or handling conditions |

### Tidyverse workflow

| Skill | Status | Responsibility | Trigger examples |
| --- | --- | --- | --- |
| [`r-tidyverse-core`](skills/r-tidyverse-core/) | Implemented | Tidy data principles, tibbles, pipes, vector/type expectations, and shared tidy evaluation concepts | Choosing a tidy representation, clarifying data shape, or coordinating multiple Tidyverse skills |
| [`r-dplyr`](skills/r-dplyr/) | Implemented | Rows, columns, values, grouping, summaries, joins, and relational transformations | `filter()`, `select()`, `mutate()`, `summarise()`, `group_by()`, joins, or window operations |
| [`r-tidyr`](skills/r-tidyr/) | Implemented | Table shape, pivoting, nesting, unnesting, list-column structure, and missingness shape | `pivot_longer()`, `pivot_wider()`, `nest()`, `unnest()`, or reshaping data |
| [`r-ggplot2`](skills/r-ggplot2/) | Implemented | Grammar-of-graphics layers, mappings, scales, facets, coordinates, and themes | Creating or reviewing a chart, choosing an aesthetic mapping, or diagnosing a plot |
| [`r-purrr`](skills/r-purrr/) | Implemented | Type-stable iteration, mapping, list-columns, ad hoc functions, and iteration errors | `map_*()`, repeated function application, list-columns, or replacing an explicit loop |
| [`r-readr`](skills/r-readr/) | Implemented | Delimited-file import, parsing, locales, missing values, column specifications, and diagnostics | Reading CSV/TSV or fixed-width text, parsing dates/numbers, or investigating import problems |

## Taxonomy

The initial taxonomy is intentionally small and covers an end-to-end workflow:

```text
R foundations
├── r-core
├── r-style
├── r-project-layout
├── r-dependencies
├── r-testing
└── r-errors

Tidyverse workflow
├── r-tidyverse-core
├── r-readr       import
├── r-tidyr       reshape
├── r-dplyr       transform
├── r-purrr       iterate
└── r-ggplot2     visualize
```

The intended flow is:

```text
readr → tidyverse-core / tidyr → dplyr → purrr → ggplot2
              │                    │
              └──── r-core ────────┴──── r-testing / r-errors
```

The foundations skills apply across the workflow. `r-tidyverse-core` provides
shared data-shape and type vocabulary; it should not absorb every package's
API. The package-specific skills own the operations named in their catalog
entries.

## Routing boundaries

Use the narrowest skill that owns the requested behavior, and add
`r-tidyverse-core` when the task depends on shared tidy-data or type semantics.

| If the task is about... | Prefer | Do not route it primarily to... |
| --- | --- | --- |
| R vectors, tibbles, data frames, recycling, or missing-value representation | [`r-core`](skills/r-core/) | `r-dplyr` merely because a pipeline is present |
| Naming, formatting, or general code conventions | [`r-style`](skills/r-style/) | `r-core` or a package-specific skill |
| Package/project/report structure | [`r-project-layout`](skills/r-project-layout/) | `r-dependencies` unless environment reproducibility is the main issue |
| Dependency versions, lockfiles, or environment restoration | [`r-dependencies`](skills/r-dependencies/) | `r-project-layout` unless structure is the main issue |
| Correctness tests, snapshots, fixtures, or mocks | [`r-testing`](skills/r-testing/) | `r-errors`, which owns failure design rather than test strategy |
| Conditions, diagnostics, or backtraces | [`r-errors`](skills/r-errors/) | `r-testing`, unless the request is specifically about testing failures |
| Tidy data shape, tibbles, pipes, or shared tidy evaluation | [`r-tidyverse-core`](skills/r-tidyverse-core/) | Any one package skill when the concern spans several packages |
| Filtering, selecting, mutating, grouping, summarizing, or joining tables | [`r-dplyr`](skills/r-dplyr/) | `r-tidyr`, which changes shape rather than table relationships |
| Long/wide reshaping, nesting, unnesting, or list-column shape | [`r-tidyr`](skills/r-tidyr/) | `r-dplyr`, which can place but does not own reshaping |
| Plot layers, mappings, scales, facets, themes, or coordinates | [`r-ggplot2`](skills/r-ggplot2/) | `r-dplyr` for complex aggregation that belongs before plotting |
| Mapping functions over vectors or lists and type-stable iteration | [`r-purrr`](skills/r-purrr/) | `r-dplyr` unless the core operation is table transformation |
| Parsing delimited or fixed-width text | [`r-readr`](skills/r-readr/) | `r-dplyr`, which operates after parsing |

Examples of deliberate boundaries:

- `readr` parses input; it does not own downstream cleaning or analysis.
- `tidyr` changes table shape; `dplyr` changes rows, columns, values, and
  relationships.
- `purrr` owns iteration and list-column workflows; it is not the default
  replacement for every vectorized base R operation.
- `ggplot2` owns visualization; substantial aggregation should normally happen
  before plotting with `dplyr`.
- `r-errors` defines failure behavior; `r-testing` verifies that behavior.
- `r-dependencies` manages reproducibility of packages and environments;
  `r-project-layout` manages repository and project structure.

## Roadmap

### Initial release

1. Maintain the six R foundation skills.
2. Maintain the six Tidyverse workflow skills.
3. Keep focused references for joins and grouping, pivoting, type-stable
   mapping, ggplot2 mappings, parsing diagnostics, and R conditions current.
4. Expand adversarial evaluation coverage for the highest-risk boundaries.
5. Record results only after independent evaluation runs are complete.

### Follow-up skill families

The following are intentionally outside the first 12-skill release:

- `r-stringr` for vectorized string processing and regular expressions.
- `r-forcats` for factor levels and categorical ordering.
- `r-lubridate` for dates, times, time zones, periods, and durations.
- `r-dbplyr` for lazy database tables and dplyr-to-SQL translation.
- `r-database` for DBI connections, transactions, drivers, and SQL boundaries.
- `r-tidymodels` for modeling, preprocessing, resampling, tuning, and metrics.
- `r-shiny` for reactive applications and server/UI behavior.
- `r-documentation` for roxygen2, pkgdown, Quarto, and R Markdown publishing.
- `r-lint` for `lintr`, `R CMD check`, and automated enforcement.
- `r-performance` and `r-benchmarking` for measurement and optimization.

These additions should remain separate rather than expanding `r-tidyverse-core`
into a general R manual.

## Contributing

New skills should:

- Use `skills/<skill-name>/SKILL.md`.
- Keep the directory name and frontmatter `name` identical.
- State both capability and activation conditions in the description.
- Keep one concept or package boundary per skill.
- Put decision-heavy material in directly linked `references/` files.
- Add or update an entry in this catalog.
- Add evaluation cases to [`EVALUATIONS.md`](EVALUATIONS.md) without claiming
  results until they have actually been run.
- Use Conventional Commits, for example `feat: add dplyr skill`.

## License

This project is released under the MIT License.
