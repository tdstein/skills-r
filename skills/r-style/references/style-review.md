# R style review checklist

Review in this order:

1. **Behavioral clarity** — Can a reader identify inputs, output shape, side effects, and failure behavior?
2. **Names** — Do names describe domain concepts and distinguish raw, cleaned, grouped, and final data?
3. **Control flow** — Is branching easier to understand as ordinary `if`/`else` or a named helper than as nested pipes?
4. **Data flow** — Does each pipeline step have one purpose? Are joins and grouping assumptions visible?
5. **Dependencies** — Are packages loaded at the right boundary and referenced through `pkg::fun()` where appropriate?
6. **Mechanical consistency** — Does styler agree with line breaks, indentation, and spacing?

Prefer a small refactor over a style comment when code is hard to understand. Keep a style comment when it records a project convention or prevents a recurring correctness problem.

## Common smells

- `df2`, `tmp`, or `x` surviving beyond a tiny local scope.
- A function that calls `setwd()`, changes options globally, or attaches packages.
- A pipeline that mixes data transformation, file writes, plotting, and global assignment.
- A script that works only because a previous session created an object, set an option, or changed the working directory.
- A comment that describes what a verb already says but omits the join key or statistical reason.
- A broad `suppressWarnings()` or `suppressMessages()` around a whole workflow.
- Repeated string literals, column names, or magic cutoffs that should be named constants.

## Useful commands

```r
styler::style_file("R/transform.R")
lintr::lint("R/transform.R")
```

Run the repository's configured commands when they differ. Formatting is a mechanical change; lint findings still require judgment.

## Further reading

- [The tidyverse style guide](https://style.tidyverse.org/)
- [styler](https://styler.r-lib.org/)
- [lintr](https://lintr.r-lib.org/)
