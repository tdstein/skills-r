---
name: r-core
description: "Use for R vectors, tibbles, data frames, missing values, recycling, pipes, and tidy evaluation; choose object types while preserving size and type semantics."
license: MIT
compatibility: "R 4.1+ and the documented packages; compatible with Claude Code, Cursor, Gemini CLI, Codex, and similar Agent Skills clients."
user-invocable: true
allowed-tools: "Read Edit Write Glob Grep Bash(R:*) Bash(Rscript:*) Bash(git:*) Agent"
metadata:
  author: tdstein
  version: "0.1.0"
  openclaw:
    emoji: "🧭"
    homepage: "https://github.com/tdstein/skills-r"
    requires:
      bins:
        - R
        - Rscript
    install: []
---

# R core

Treat R objects and their invariants as part of the interface. Prefer code whose input, output, missingness, and size behavior are explicit.

## Working rules

- Model assignment as binding a name to a value, not as giving an object a permanent name. When aliasing, mutation, or performance matters, remember that ordinary vectors and lists use copy-on-modify; environments are reference-like, and single-binding objects may be modified in place as an implementation optimisation. Measure surprising copy behavior with `tracemem()` or `lobstr::ref()` instead of relying on a guessed reference count.
- Distinguish atomic vectors, lists, matrices, data frames, and tibbles before choosing an operation. A tibble is a data frame with stricter printing and subsetting behavior; it is not a replacement for every matrix or list.
- Treat a scalar as a length-one vector. Check `typeof()`, `length()`, `class()`, `attributes()`, and dimensions when an object's representation affects behavior; `str()` is often the quickest compact inspection.
- Expect atomic combination to coerce toward a common type. Keep integer, double, logical, character, factor, date/time, and duration values distinct until the contract calls for conversion; do not use broad coercion as a repair for an unclear type mismatch.
- Check vector size and type deliberately. R recycles shorter vectors in many operations, but accidental recycling can silently produce wrong results. Use explicit length checks or `vctrs` helpers at boundaries where sizes must agree.
- Preserve missingness intentionally. `NA` is typed and propagates through many computations; use `is.na()`, `anyNA()`, `na.rm`, or explicit imputation rather than treating it as an empty string or zero.
- Use `[` when selecting a collection and `[[` when extracting or assigning one element. Reserve `$` for a literal, syntactic name; it is not suitable for a name stored in a variable and can partially match. Use `drop = FALSE` when matrix, array, or data-frame dimensionality must remain stable.
- Treat subassignment as a contract: validate the replacement size and avoid duplicated or missing indices unless their recycling and overwrite behavior is intentional. Use `x[] <- value` when replacing contents while preserving the outer structure; assigning a new object to `x` can change its type and attributes.
- Prefer `|>` for straightforward base-R pipelines. Use `%>%` only when the surrounding project already uses it or when magrittr-specific features are required.
- Keep transformations explicit about evaluation context. In tidyverse verbs, bare column names are data-masked expressions; external values should usually be named variables or injected with the appropriate tidy-evaluation mechanism.
- Preserve names, dimensions, classes, and other attributes when they carry meaning. Most attributes are not automatically stable under operations, so check them after transformations that must retain an S3 or rectangular contract. Avoid coercing a tibble to a matrix or character vector merely to pass it to a function without checking the resulting loss of structure.
- Make output shape part of the contract: state whether a function returns one value, one row per group, a vector matching input size, or a tibble.

## Routing

- Read [references/tidy-data-and-types.md](references/tidy-data-and-types.md) when data shape, vector coercion, recycling, missingness, object identity, attributes, or subsetting behavior is consequential.
- Read [references/tidy-evaluation.md](references/tidy-evaluation.md) when writing functions around dplyr/tidyr verbs, embracing column arguments, or constructing expressions.
- Use `r-style` for formatting and naming decisions, `r-testing` for behavioral verification, and `r-errors` for condition design.

## Verification

For non-trivial transformations, test representative zero-row, one-row, missing-value, and mixed-type inputs. Check both `typeof()`/class and dimensions, not only printed output.
