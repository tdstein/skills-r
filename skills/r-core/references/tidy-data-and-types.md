# Tidy data and R types

## Shape first

Before transforming data, identify:

- What one row represents.
- Which columns are identifiers, measurements, and list-columns.
- Whether the input is local or a lazy remote table.
- Whether zero rows are valid and what schema should remain in that case.

Keep one observation per row and one variable per column when the downstream operation is relational or visual. Use `tidyr` when the problem is table shape; do not hide reshaping inside an unrelated helper.

## Size and type checks

Use the narrowest check that expresses the invariant:

```r
stopifnot(is.data.frame(x), nrow(x) >= 0L)
vctrs::vec_assert(id, character())
vctrs::vec_size_common(x, y)
```

For public helpers, prefer an informative `rlang::abort()` over an incidental base-R error. Check that returned vectors have the intended common type and size. Be especially careful with logical, integer, double, and date-time inputs: coercion can be valid R behavior while still violating the application contract.

## Missing values

- `is.na(x)` detects missing values; `x == NA` does not.
- `anyNA(x)` is useful for a fast presence check.
- `mean(x, na.rm = TRUE)` changes the denominator and can return `NaN` for all-missing input; decide whether that is acceptable.
- Do not use `coalesce()` or replacement as a generic fix without documenting the domain meaning of the substitute.

## Subsetting invariants

Use `[[` when a single element is required. Use `[` when preserving a vector, list, or data-frame container matters. In functions accepting user-selected columns, validate selection and preserve names rather than relying on accidental partial matching.

## Further reading

- [Tibble](https://tibble.tidyverse.org/)
- [vctrs size and type stability](https://vctrs.r-lib.org/articles/type-size.html)
- [Tidy data](https://r4ds.hadley.nz/tidy-data.html)

