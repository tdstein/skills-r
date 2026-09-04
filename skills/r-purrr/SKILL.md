---
name: r-purrr
description: "Use for purrr functional iteration: map/reduce/predicate families, map2/pmap, typed outputs, list-columns, side effects, and per-element failures. Route closures, function factories, operators, and general composition to r-functional-programming."
license: MIT
compatibility: "R 4.1+ and the documented packages; compatible with Claude Code, Cursor, Gemini CLI, Codex, and similar Agent Skills clients."
user-invocable: true
allowed-tools: "Read Grep Glob Bash(R:*) Bash(Rscript:*)"
metadata:
  author: "tdstein"
  version: "0.1.0"
  openclaw:
    emoji: "🔁"
    homepage: "https://github.com/tdstein/skills-r"
    requires:
      bins:
        - R
        - Rscript
    install: []
---

# purrr functional iteration

Use purrr when the unit of work is applying a function to each element, reducing a sequence, testing elements with a predicate, or coordinating list-column workflows. Keep the callback small and let the functional express the iteration contract. For first-class functions, purity, closures, function factories, function operators, or memoisation, read `r-functional-programming`; for ordinary function signatures and lazy-evaluation mechanics, use `r-functions`.

## Choose the right tool

- Use `map()` for a list result, `map_chr()`, `map_int()`, `map_dbl()`, and `map_lgl()` when every result must be length one and the type is part of the contract.
- Use `map_vec()` when results are simple vectors and a common type should be determined.
- Use `map2()` or `pmap()` when each iteration consumes multiple aligned inputs; validate lengths and names.
- Use `imap()` when the element name or index is part of the computation.
- Use `walk()`/`pwalk()` for side effects when the input, not the side-effect result, should flow onward.
- Use `possibly()` when a fallback value is a valid result, `safely()` when callers need both result and error, and `quietly()` when output/messages must be captured.
- For many files, list paths with `full.names = TRUE`, preserve path or file names when they are data, and use `list_rbind(names_to = ...)` only after validating a compatible schema.
- Use `modify()`/`modify2()` when the result should retain the input container type; these return a modified copy rather than mutating the original object in place.
- Use `reduce()` for a binary operation applied across a sequence, `accumulate()` when intermediate states matter, and `reduce2()` only when a second varying input is genuinely needed.
- Use `some()`, `every()`, and `none()` for existential/all/none checks; they can stop as soon as the answer is known. Use `detect()`/`detect_index()` for the first match and `keep()`/`discard()` for filtering.
- Use `map_if()` or `modify_if()` when selection by a predicate is part of the iteration contract. If the operation is an ordinary vectorized transformation, use the vectorized operation or the owning data-manipulation skill instead.

## Reliability rules

- Prefer an explicit anonymous function `\(x) ...` for nontrivial work; do not rely on formula shortcuts in new code.
- Keep outputs type-stable. Typed mappers enforce both a common type and length-one results; use `map()` first when exploring heterogeneous or unexpectedly sized results, then make the contract explicit.
- Remember that `map()` varies only `.x`. Arguments after `.f` are passed unchanged to every call and are evaluated as ordinary call arguments; use `map2()`/`pmap()` for values that vary per element. An anonymous function can deliberately evaluate an expression on each call, so do not confuse `map(x, f, runif(1))` with `map(x, \(x) f(x, runif(1)))`.
- Name forwarded arguments such as `na.rm = TRUE`, especially when the callback has arguments that could collide with the mapper's formals. Name `pmap()` inputs to make callback matching visible.
- Expect purrr to annotate indexed errors; preserve that context when reporting or rethrowing.
- When failures should be reviewed, retain input identity plus both result and error (for example, map `safely()` and then `transpose()`). Use `possibly()` only when its fallback is a meaningful, typed result; condition design and recovery belong to `r-errors`.
- Make side effects explicit with `walk()` and keep paired inputs together with `walk2()`/`pwalk()`. Use `r-functions` for resource cleanup and `r-testing` for deterministic side-effect tests.
- For `reduce()` in reusable code, choose and document `.init` as the operation's identity or empty-input result. Test length-zero and length-one inputs, operation order, and whether the reducer is associative; do not assume every binary function can be safely reordered or parallelized.
- Do not use purrr merely to replace a simple vectorized operation or a dplyr `across()` transformation.
- Prefer several simple, inspectable mapping stages over one opaque per-element function when the same cleanup can be understood across all inputs. Bind earlier when the remaining work is ordinary table transformation.
- `in_parallel()` is an explicit execution choice, not a synonym for `pmap()`. It also requires `carrier` (version 0.3.0 or newer); use it only when the function is self-contained, dependencies are explicit, and parallel overhead is justified.

Read [references/type-safety-and-errors.md](references/type-safety-and-errors.md) for typed mapping and failure handling. Read [references/parallel-and-side-effects.md](references/parallel-and-side-effects.md) when mapping performs I/O or parallel work.
