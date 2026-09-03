# tidyr pivoting

## Design the pivot

For `pivot_longer()`:

- Keep stable identifiers in `id_cols` or the non-selected columns.
- Select measured columns explicitly; avoid broad selectors that include identifiers.
- Use `names_to` with `names_sep` or `names_pattern` when column names encode multiple variables.
- Use `.value` in `names_to` when part of the original name determines the output value column.
- Use `values_drop_na = TRUE` only when missing cells represent structural absence created by the input layout, rather than meaningful missing observations.

For `pivot_wider()`:

- Identify the row identifiers and the columns that become names.
- Check whether each identifier/name combination has at most one value.
- Supply `values_fn` when duplicates are expected and the aggregation is part of the specification.
- Use `values_fill` only for a justified structural default, not to hide missing measurements. Document the interpretation of the fill value.
- Use `names_glue`, `names_sort`, or `names_vary` when stable output names matter.

After either pivot, verify the intended grain with `count()` and inspect names with `names()` or `tidyselect` helpers.
