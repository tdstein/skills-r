# Package dependency workflow

## DESCRIPTION fields

Use the narrowest field:

- `Imports`: required at runtime.
- `Suggests`: optional features, tests, vignettes, examples, and development workflows.
- `LinkingTo`: headers needed to compile dependent code.
- `Depends`: packages that must be attached or a minimum R version; use sparingly.

For a dependency used by a function, prefer:

```r
#' @importFrom dplyr filter
#' @importFrom rlang abort
```

or explicit calls:

```r
dplyr::filter(data, active)
rlang::abort("...")
```

Keep the corresponding `DESCRIPTION` declaration and roxygen source in sync.

## Optional dependencies

```r
run_plot <- function(data) {
  if (!requireNamespace("ggplot2", quietly = TRUE)) {
    rlang::abort("Install ggplot2 to use run_plot().", class = "my_pkg_missing_dependency")
  }
  ggplot2::ggplot(data, ggplot2::aes(x, y))
}
```

Tests for optional packages should use `testthat::skip_if_not_installed()` or the project's equivalent, while still checking the package's behavior when the dependency is present.

## Checks

After changing dependencies:

```r
devtools::document()
devtools::test()
devtools::check()
```

Use `R CMD check` in CI or release automation. Review warnings about undeclared packages, examples, vignettes, and missing imports rather than suppressing them.

Documentation and vignette code is part of the package's dependency surface:
packages used only there generally belong in `Suggests`, and examples should
remain runnable when optional dependencies are absent or should skip with a
clear condition. Keep rendering-tool dependencies in the documentation or
project environment when they are not needed by the installed package.

## Further reading

- [R Packages: Dependencies](https://r-pkgs.org/dependencies.html)
- [R Packages: Namespace](https://r-pkgs.org/namespace.html)
