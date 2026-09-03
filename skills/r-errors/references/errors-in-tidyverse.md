# Errors in tidyverse workflows

## Add data context safely

When a failure occurs inside a grouped or mapped transformation, report the operation and safe identifiers:

```r
rlang::abort(
  "Could not parse amount.",
  class = "my_pkg_parse_amount",
  amount_name = column_name,
  row = row_number
)
```

Do not paste an entire row or input file into the error. Store structured fields for programmatic consumers when the condition may be handled.

## Preserve pipeline boundaries

Validate inputs before a long pipeline when failure should point to the caller's mistake. Inside a pipeline, use named intermediate variables when an error otherwise provides no clue which transformation failed. For remote tables, distinguish local validation failures from SQL translation or database execution failures.

Avoid wrapping every dplyr error in a generic message that erases its class and backtrace. Add context only at a boundary where the operation becomes meaningful to the caller, and preserve the parent condition.

## User-facing diagnostics

Use `cli::cli_abort()` or `cli::cli_warn()` when a CLI or application needs formatted bullets. Keep machine-readable classes independent from visual formatting. Do not make tests depend on ANSI styling, line wrapping, or terminal width.

## Further reading

- [rlang condition handling](https://rlang.r-lib.org/reference/topic-condition.html)
- [cli conditions](https://cli.r-lib.org/reference/cli_abort.html)

