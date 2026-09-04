# Style in R packages

## Public API

Export only stable user-facing functions. Keep internal helpers unexported unless consumers genuinely need them. Use roxygen2 comments for exported objects and keep documentation examples aligned with the current API.

Use `Imports` for packages required by the package API and call their functions with `pkg::fun()` unless the package deliberately imports symbols through `NAMESPACE`. Never depend on a package merely because it happens to be attached in a developer session.

## Files

Keep package source under `R/`, tests under `tests/testthat/`, and generated artifacts out of source control. Put data preparation scripts in `data-raw/` when the project needs reproducible data generation; do not make package loading execute data downloads.

## Error and side-effect boundaries

Functions should accept dependencies as arguments when practical, return values instead of mutating global state, and fail with context. Use `r-errors` for condition classes and user-facing messages. Use `r-dependencies` for `DESCRIPTION`, `NAMESPACE`, and environment decisions.

## Further reading

- [R Packages: Code](https://r-pkgs.org/code.html)
- [R Packages: Package metadata](https://r-pkgs.org/description.html)
