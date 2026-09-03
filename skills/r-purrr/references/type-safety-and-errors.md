# purrr type safety and errors

## Return contracts

- `map_*()` variants require each result to satisfy the declared type and length. Use them to fail close to the bad element.
- Use `map_vec(.ptype = ...)` when the common output type should be explicit, especially for Dates, factors, or custom vectors.
- Use `list_rbind()`/`list_cbind()` when combining data-frame results and validate schemas before binding.
- If a function can return multiple classes or sizes, use `map()` and validate each result explicitly rather than forcing a lossy simplification.

## Failure policies

```r
results <- inputs |>
  map(\(x) safely(parse_one)(x)) |>
  transpose()
```

Choose the policy based on the caller:

- `possibly(.f, otherwise = typed_default)` is appropriate when a fallback is meaningful and the failure should not stop the batch.
- `safely()` is appropriate when errors are data that must be reviewed.
- `possibly(..., quiet = FALSE)` or ordinary `map()` is preferable when failures should remain visible.
- Do not turn an error into `NA` without recording which input failed.

## Indexed errors

When a mapped function fails, report the element index/name and relevant input metadata. Preserve the original condition and backtrace when debugging.
