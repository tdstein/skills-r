# Tidy evaluation in functions

## Choose the interface

Use ordinary function arguments when the caller supplies values:

```r
filter_threshold <- function(data, threshold) {
  dplyr::filter(data, value >= threshold)
}
```

Use data-masked column arguments when the caller should write a column name:

```r
summarise_mean <- function(data, column) {
  column <- rlang::enquo(column)
  dplyr::summarise(data, mean = mean(!!column, na.rm = TRUE))
}
```

For a character vector of column names, use `.data[[column_name]]` or the tidyselect API rather than turning strings into code. For names created by the function, use `.data` and `.env` pronouns or explicit injection so data columns cannot unexpectedly shadow environment variables.

## Avoid accidental capture

- Use `.data$column` or `.data[[name]]` when referring to a data column programmatically.
- Use `.env$value` when the value must come from the calling environment.
- Do not use `parse(text = ...)` or `eval(parse(...))` to implement ordinary column selection.
- Validate a user-supplied expression if it will be evaluated more than once or outside the normal data-mask.

## Test the contract

Test bare-name, character-name, and missing-column inputs separately. Include a data frame containing a column whose name matches an environment variable; this catches accidental lookup in the wrong scope.

## Further reading

- [rlang tidy evaluation](https://rlang.r-lib.org/reference/topic-data-mask.html)
- [Programming with dplyr](https://dplyr.tidyverse.org/articles/programming.html)
