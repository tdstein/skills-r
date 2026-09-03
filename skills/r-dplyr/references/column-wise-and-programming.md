# dplyr column-wise programming

## Column-wise operations

Use `across()` inside `mutate()`, `summarise()`, or `reframe()`:

```r
df |>
  summarise(
    across(where(is.numeric), \(x) mean(x, na.rm = TRUE)),
    .groups = "drop"
  )
```

Use `.names` when multiple functions or repeated transformations could create ambiguous names. Use `pick()` when a function needs the selected data frame rather than one vector at a time.

## Reusable functions

- Use `{{ column }}` when forwarding a data-masked column expression.
- Use `.data[[name]]` when callers provide a string.
- Use `all_of()` for a trusted character vector of names and `any_of()` when missing names should be ignored intentionally.
- Qualify `dplyr::` and `rlang::` functions in package code or declare imports.
- Test empty selections, missing columns, grouped input, and name collisions.

Avoid constructing expressions with string concatenation. It is harder to validate and more fragile than tidy-selection helpers or explicit data pronouns.
