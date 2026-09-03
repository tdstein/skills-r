# Integration tests and deterministic fixtures

## Isolate external state

Use `withr::local_tempdir()`, `withr::local_envvar()`, `withr::local_options()`, and `withr::local_dir()` to isolate filesystem and process state. Prefer `testthat::local_mocked_bindings()` for narrow, explicit mocks instead of globally replacing a package function.

External tests should make their prerequisites obvious:

```r
test_that("database import preserves schema", {
  testthat::skip_if_not(Sys.getenv("RUN_DB_TESTS") == "true")
  testthat::skip_if_not_installed("DBI")
  # Connect to a disposable test database and clean up with on.exit().
})
```

Do not make ordinary unit-test runs open production connections or mutate a developer's database. Use disposable services, temporary files, and test-specific credentials for integration runs.

## Randomness and time

Set a seed at the narrowest scope that needs reproducibility. Prefer dependency injection for current time and random generators when exact behavior matters. Do not use long sleeps to wait for asynchronous work; poll with a bounded timeout or use the framework's synchronization primitive.

## Data workflow fixtures

Construct small tibbles that isolate one invariant: duplicate keys, all-missing groups, zero rows, factor levels, date-time zones, or list-columns. Assert the expected row count and types, not only a few values.

## CI selection

Keep fast unit tests in the default suite. Select integration tests through an explicit environment variable, test tag, or CI job and document the required service. A skipped integration test should be reported as skipped, not passed as if it exercised the boundary.

## Further reading

- [withr](https://withr.r-lib.org/)
- [testthat mocking](https://testthat.r-lib.org/reference/local_mocked_bindings.html)
