# testthat patterns

## Focused tests

```r
test_that("summarise keeps one row per group", {
  result <- summarise_scores(tibble::tibble(group = c("a", "a"), score = c(1, 3)))

  expect_s3_class(result, "tbl_df")
  expect_equal(result$group, "a")
  expect_equal(result$mean_score, 2)
})
```

Use descriptive names and keep setup close to the behavior. Use `local_edition()` or the project's configured testthat edition rather than changing global state.

## Conditions

```r
expect_error(
  parse_id(""),
  class = "my_pkg_invalid_id"
)

expect_warning(
  read_legacy_format(path),
  class = "my_pkg_deprecated_format"
)
```

Prefer custom condition classes in production code so tests can distinguish contract failures from unrelated wording changes. Match only stable message text when the message itself is part of the user contract.

## Snapshots and fixtures

Use snapshots for deliberately stable output such as CLI messages, printed objects, or plot specifications. Keep fixture data minimal and readable. For large or sensitive data, generate it deterministically in a helper rather than committing an opaque dump.

## Further reading

- [testthat reference](https://testthat.r-lib.org/reference/)
- [Testing functions](https://r-pkgs.org/testing-basics.html)

