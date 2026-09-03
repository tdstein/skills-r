# Analysis and report layout

## Separate stages

Keep raw inputs, derived data, code, and rendered outputs distinguishable:

```text
data-raw/       # acquisition or derivation scripts
data/           # local or versioned inputs, if policy allows
R/              # reusable helpers
analysis/       # ordered analysis scripts
reports/        # Quarto/R Markdown sources and rendered documents
figures/        # intentional exported graphics
```

The exact names can follow the existing project, but each directory should have one responsibility. Do not let `data/` become a mixture of raw, cleaned, and final tables without naming or metadata.

## Reproducible paths

Resolve paths from the project root with `here::here()` or an explicit project-root function. Avoid absolute machine-specific paths and avoid `setwd()` in code that others must run.

Reports should call named helpers for substantial work. Keep parameters and input paths visible near the top, and write outputs to a known destination. Avoid relying on objects left in the interactive session.

## Scripts are the source of truth

An analysis should survive a session restart. Run each script from top to bottom in a clean R session before handing it off; if it fails, capture the missing setup, input, or dependency in code rather than relying on the workspace or command history.

Start scripts with the package attachments needed for an interactive analysis. Do not put `install.packages()` in a shared script: installation changes another person's machine and belongs in setup documentation or an explicit environment-management step.

Use relative paths from the project root and forward slashes in paths. Give scripts informative, machine-readable names; prefix ordered stages with numbers only when execution order is part of the workflow.

## Further reading

- [R for Data Science: Scripts and projects](https://r4ds.hadley.nz/workflow-scripts.html)
- [Quarto](https://quarto.org/docs/computations/r.html)
