# Conditions and recovery

## Error classes

```r
validate_id <- function(id) {
  if (length(id) != 1L || is.na(id) || !nzchar(id)) {
    rlang::abort(
      "ID must be one non-empty string.",
      class = "my_pkg_invalid_id"
    )
  }
  id
}
```

Classes are the programmatic contract. Keep them stable and specific enough for callers to decide whether to retry, prompt for input, or stop.

## Handler choice

Use `tryCatch()` to transform or recover:

```r
result <- tryCatch(
  read_file(path),
  error = function(cnd) {
    rlang::abort("Could not load configuration.", parent = cnd)
  }
)
```

Use `withCallingHandlers()` to observe or selectively muffle:

```r
withCallingHandlers(
  compute_report(data),
  warning = function(cnd) {
    log_warning(cnd)
    invokeRestart("muffleWarning")
  }
)
```

Only muffle a warning when the caller has deliberately chosen that policy and the condition is understood. Otherwise let it remain visible.

## Signaling and restarts

Use errors for failed contracts, warnings for recoverable or deprecated behavior,
and messages for user-facing progress or guidance. If several recovery policies
are valid, keep the recovery actions near the code that knows how to perform them
and let a higher-level handler select a named restart with
`withCallingHandlers()` and `invokeRestart()`. Put the most specific
`tryCatch()` handler first because handlers are selected in registration order.

## Cleanup

Use `on.exit()` immediately after acquiring a resource. Keep cleanup independent of whether the protected operation succeeds:

```r
con <- DBI::dbConnect(...)
on.exit(DBI::dbDisconnect(con), add = TRUE)
```

## Further reading

- [rlang abort](https://rlang.r-lib.org/reference/abort.html)
- [Conditions in Advanced R](https://adv-r.hadley.nz/conditions.html)
- [Beyond exception handling](https://adv-r.hadley.nz/beyond-exception-handling.html)
