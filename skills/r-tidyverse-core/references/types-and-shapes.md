# Tidyverse types and shapes

Use this reference when a transformation may change row count, column types, grouping, or list-column structure.

## Invariants to check

- Record `nrow()`, `ncol()`, key columns, and grouping variables before a nontrivial pipeline.
- Check that identifiers remain unique when uniqueness is required; do not infer uniqueness from column names.
- Use `vctrs::vec_size()` for vector size and `vctrs::vec_ptype_common()` when combining heterogeneous values.
- Treat a list-column as a deliberate column of objects. Inspect element sizes and classes before unnesting or simplifying.
- Use explicit prototypes or transformations when parsing or combining values whose type matters.
- Do not use `as.character()` as a generic fix for incompatible types; it often destroys dates, factors, and numeric meaning.
- Treat matrix- and data-frame columns as deliberate non-atomic columns. Their row extent must align with the data frame, but their inner dimensions and classes still matter.

## Data-frame and tibble contracts

- A data frame is a named list with a common row extent; `length()` counts
  columns, while `nrow()` and `ncol()` describe the rectangular view.
- Prefer ordinary identifier columns over row names. Convert legacy row names at
  the boundary with an explicit name such as `id`.
- Tibbles retain input types and names, only recycle length-one columns during
  construction, and keep a tibble when using `[`. These properties make
  programmatic pipelines more predictable, but they do not remove the need to
  validate row counts and column meaning.

## Subsetting and replacement

Use `[` for a data-frame or tibble collection and `[[` for one column or
element. In reusable code, make the result shape explicit and do not rely on
base data-frame partial matching or automatic dimension dropping. Validate
replacement sizes and duplicated indices before subassignment when those
operations represent row-wise alignment.

## Package routing

| Need | Owner |
| --- | --- |
| Filter, mutate, select, arrange, summarise, or join rows and columns | `r-dplyr` |
| Pivot, nest, unnest, or otherwise change rectangular shape | `r-tidyr` |
| Apply a function over vectors or list-columns | `r-purrr` |
| Parse a delimited or fixed-width file | `r-readr` |
| Build a chart from prepared data | `r-ggplot2` |

## Common traps

- A grouped tibble is still a tibble, but many verbs use its grouping metadata. Never assume `summarise()` leaves an ungrouped result.
- `NULL` removes or omits an object in many list and argument contexts; `NA` is a typed missing value.
- Recycling is not a substitute for validating row alignment. Prefer joins or explicit vector-size checks when data comes from separate sources.
- A wide table is not automatically untidy; decide from the observational unit and variable meaning, then use `r-tidyr` if the representation must change.
- Tidy data is a consistent working representation, not a permanent destination. It is reasonable to widen for a presentation or API boundary, then pivot again before an analysis that benefits from variables in columns.
- `NULL` commonly means an absent component or removal from a list-like object; it is not the same as an observed `NA` value.
