# Agent Skills for R and Tidyverse projects

Reusable Agent Skills for R development, reproducible analysis, and the
Tidyverse data workflow. Skills are loaded on demand so an agent can receive
focused R guidance without loading an entire language manual into every task.

This repository is an R counterpart to
[`samber/cc-skills-golang`](https://github.com/samber/cc-skills-golang). The
collection contains 23 implemented skills, including focused coverage derived
from Hadley Wickham's *Advanced R*. Evaluation results remain pending until
the independent evaluation lifecycle is completed.

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

The skills are atomic, cross-referencing units. Each skill should own one
coherent concern, state when it should trigger, and identify neighboring skills
that should handle adjacent concerns.

Status legend:

- **Implemented** — the skill directory and `SKILL.md` are available;
  evaluation is pending.
- **Evaluated** — the skill has a recorded evaluation result in
  [`EVALUATIONS.md`](EVALUATIONS.md).

All catalogued skills are Implemented. Evaluation status is tracked separately in
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

### Advanced R programming

| Skill | Status | Responsibility | Trigger examples |
| --- | --- | --- | --- |
| [`r-functions`](skills/r-functions/) | Implemented | Function contracts, calls, lexical scope, lazy evaluation, control flow, recursion, and composition | Designing an R function, debugging argument evaluation, or reviewing a loop |
| [`r-environments`](skills/r-environments/) | Implemented | Bindings, parent chains, namespaces, closures, caller context, and persistent state | Investigating lookup, closures, `<<-`, package namespaces, or caches |
| [`r-functional-programming`](skills/r-functional-programming/) | Implemented | Pure functions, higher-order design, factories, operators, memoisation, and effect boundaries | Building a function factory, operator, cache, or composable workflow |
| [`r-object-oriented`](skills/r-object-oriented/) | Implemented | S3, S4, and R6 representation, construction, validation, dispatch, inheritance, and system choice | Designing an R class, generic, method, or mutable object |
| [`r-metaprogramming`](skills/r-metaprogramming/) | Implemented | Expressions, calls, quotation, quasiquotation, quosures, data masks, evaluation, and translation | Capturing user code, generating calls, or building a small DSL |
| [`r-debugging`](skills/r-debugging/) | Implemented | Reproducible diagnosis, tracebacks, interactive debugging, batch failures, and crash investigation | Debugging an R error, warning, hang, or R Markdown failure |
| [`r-benchmarking`](skills/r-benchmarking/) | Implemented | Profiling, microbenchmarks, workload design, allocations, garbage collection, and scaling | Measuring an R bottleneck or comparing implementations |
| [`r-performance`](skills/r-performance/) | Implemented | Evidence-based optimization, vectorization, allocation control, and performance trade-offs | Improving a measured R hot path without changing behavior |
| [`r-interop`](skills/r-interop/) | Implemented | R/C/C++ boundaries, `.Call`, Rcpp, registration, protection, conversion, and portability | Adding or reviewing native R code |
| [`r-connections`](skills/r-connections/) | Implemented | File, URL, pipe, socket, text, binary, and encoding-aware connection I/O | Reading or writing through an R connection |
| [`r-documentation`](skills/r-documentation/) | Implemented | Package docs, vignettes, reports, books, reproducible examples, and publishing workflows | Writing or building R documentation and long-form project docs |

## Taxonomy

The taxonomy is organized around R language semantics, project boundaries, and
the Tidyverse workflow:

```text
R foundations
├── r-core
├── r-style
├── r-project-layout
├── r-dependencies
├── r-testing
├── r-errors
├── r-functions
├── r-environments
├── r-object-oriented
├── r-metaprogramming
└── r-debugging

Tidyverse workflow
├── r-tidyverse-core
├── r-readr       import
├── r-tidyr       reshape
├── r-dplyr       transform
├── r-purrr       iterate
└── r-ggplot2     visualize

Advanced R tooling
├── r-functional-programming
├── r-benchmarking
├── r-performance
├── r-interop
├── r-connections
└── r-documentation
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
| Reproducing and locating an unexpected failure | [`r-debugging`](skills/r-debugging/) | `r-errors`, which owns condition design rather than diagnosis |
| Tidy data shape, tibbles, pipes, or shared tidy evaluation | [`r-tidyverse-core`](skills/r-tidyverse-core/) | Any one package skill when the concern spans several packages |
| Filtering, selecting, mutating, grouping, summarizing, or joining tables | [`r-dplyr`](skills/r-dplyr/) | `r-tidyr`, which changes shape rather than table relationships |
| Long/wide reshaping, nesting, unnesting, or list-column shape | [`r-tidyr`](skills/r-tidyr/) | `r-dplyr`, which can place but does not own reshaping |
| Plot layers, mappings, scales, facets, themes, or coordinates | [`r-ggplot2`](skills/r-ggplot2/) | `r-dplyr` for complex aggregation that belongs before plotting |
| Mapping functions over vectors or lists and type-stable iteration | [`r-purrr`](skills/r-purrr/) | `r-dplyr` unless the core operation is table transformation |
| Parsing delimited or fixed-width text | [`r-readr`](skills/r-readr/) | `r-dplyr`, which operates after parsing |
| Function contracts, lazy arguments, control flow, or recursion | [`r-functions`](skills/r-functions/) | `r-purrr` unless iteration is the core operation |
| Environment identity, lexical lookup, namespaces, or persistent state | [`r-environments`](skills/r-environments/) | `r-functions` when the environment mechanics are the issue |
| Function factories, operators, purity, or memoisation | [`r-functional-programming`](skills/r-functional-programming/) | `r-functions` for ordinary function semantics |
| S3, S4, R6, constructors, or method dispatch | [`r-object-oriented`](skills/r-object-oriented/) | `r-core`, which supplies representation semantics but not OO design |
| Expressions, quosures, data masks, code generation, or translation | [`r-metaprogramming`](skills/r-metaprogramming/) | `r-functions` unless no code capture/evaluation is involved |
| Profiling or benchmarking an R workload | [`r-benchmarking`](skills/r-benchmarking/) | `r-performance`, which changes code after evidence exists |
| Optimizing a measured R bottleneck | [`r-performance`](skills/r-performance/) | `r-benchmarking`, which owns measurement design |
| R/C/C++ or Rcpp integration | [`r-interop`](skills/r-interop/) | `r-performance` unless the native boundary is justified by measurement |
| Connection-based file, URL, pipe, socket, text, or binary I/O | [`r-connections`](skills/r-connections/) | `r-readr`, which owns tabular parsing |
| R package docs, vignettes, reports, books, or publishing | [`r-documentation`](skills/r-documentation/) | `r-project-layout`, unless directory structure is the main issue |

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
- `r-benchmarking` measures; `r-performance` optimizes after evidence.
- `r-connections` transports bytes or characters; `r-readr` parses tabular data.
- `r-documentation` owns documentation content and publishing; project layout
  owns where those artifacts live.

## Roadmap

### Current collection

1. Maintain the R foundation, Advanced R, and Tidyverse skill families.
2. Keep focused references for joins and grouping, pivoting, type-stable
   mapping, ggplot2 mappings, parsing diagnostics, conditions, performance,
   native interop, and reproducible documentation current.
3. Expand adversarial evaluation coverage for the highest-risk boundaries.
4. Record results only after independent evaluation runs are complete.

### Follow-up skill families

The following remain outside the current collection:

- `r-stringr` for vectorized string processing and regular expressions.
- `r-forcats` for factor levels and categorical ordering.
- `r-lubridate` for dates, times, time zones, periods, and durations.
- `r-dbplyr` for lazy database tables and dplyr-to-SQL translation.
- `r-database` for DBI connections, transactions, drivers, and SQL boundaries.
- `r-tidymodels` for modeling, preprocessing, resampling, tuning, and metrics.
- `r-shiny` for reactive applications and server/UI behavior.
- `r-lint` for `lintr`, `R CMD check`, and automated enforcement.

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
