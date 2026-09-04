---
name: r-readr
description: "Use for readr import/export of delimited or fixed-width text, parsing, locales, column types, missing values, and diagnostics."
license: MIT
compatibility: "R 4.1+ and the documented packages; compatible with Claude Code, Cursor, Gemini CLI, Codex, and similar Agent Skills clients."
user-invocable: true
allowed-tools: "Read Grep Glob Bash(R:*) Bash(Rscript:*)"
metadata:
  author: "tdstein"
  version: "0.1.0"
  openclaw:
    emoji: "📥"
    homepage: "https://github.com/tdstein/skills-r"
    requires:
      bins:
        - R
        - Rscript
    install: []
---

# readr import and parsing

Treat data import as a reproducible schema boundary. Define how the file is delimited, encoded, typed, localized, missing, and diagnosed before downstream transformation.

## Workflow

1. Confirm delimiter, quote and escape rules, encoding, header behavior, and file origin.
2. Prefer explicit `col_types` for stable pipelines. Use guessing for exploration, then inspect and pin the resulting specification.
3. Define `na`, `locale()`, date formats, decimal marks, and grouping marks when the source is not unambiguous.
4. Read a representative sample, inspect the column specification, and check `problems()` immediately.
5. Rename non-syntactic or inconsistent source columns deliberately at the import boundary, preserving a traceable mapping to the source schema.
6. Decide whether malformed fields are errors, warnings requiring quarantine, or recoverable missing values.
7. When importing more than one file, retain a source identifier such as the path or file name before combining records.
8. Validate row counts, key columns, types, and sentinel values before handing data to `r-dplyr` or `r-tidyr`.
9. Use `write_csv()`/related writers with explicit output expectations; do not treat serialization as a neutral round trip for every R type.

## Important constraints

- Type guessing is a heuristic, not a data contract. It samples values and can miss rare values or malformed records.
- A parsing failure is not the same as an ordinary missing value. Keep the diagnostics and source row context.
- Locale is part of the parser configuration. A comma decimal mark, date order, or non-English month name must be explicit.
- Use `col_select` to limit imported data when appropriate, but confirm skipped columns are not needed for validation.
- CSV is a portable text interchange format, not a type-preserving cache. Use RDS when preserving an exact R object matters, or Parquet when a typed, cross-language intermediate format is appropriate.
- Do not clean malformed text with broad substitutions before determining whether the source format or parser specification is wrong.

Read [references/types-locales.md](references/types-locales.md) for column specifications, locales, and parsers. Read [references/diagnostics-and-contracts.md](references/diagnostics-and-contracts.md) for problems, validation, and reproducible import contracts.
