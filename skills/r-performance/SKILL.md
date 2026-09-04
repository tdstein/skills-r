---
name: r-performance
description: "Use to improve R performance after profiling or benchmarking identifies a bottleneck, balancing correctness, CPU time, allocation, memory, generality, and maintainability. Do not use this skill to make unmeasured speculative changes."
license: MIT
compatibility: "R 4.1+ and the documented packages; compatible with Claude Code, Cursor, Gemini CLI, Codex, and similar Agent Skills clients."
user-invocable: true
allowed-tools: "Read Edit Write Glob Grep Bash(R:*) Bash(Rscript:*) Bash(git:*) Agent"
metadata:
  author: tdstein
  version: "0.1.0"
  openclaw:
    emoji: "🚀"
    homepage: "https://github.com/tdstein/skills-r"
    requires:
      bins:
        - R
        - Rscript
    install: []
---

# R performance improvement

Use this skill after a profile, benchmark, or equivalent evidence identifies a bottleneck. Make the smallest change that meets the performance goal while preserving behavior, then remeasure the realistic workload and the focused alternative. Do not optimize every visible inefficiency: set a target, work on material bottlenecks, and stop when the target or a defensible limit is reached.

## Organize the optimization

- Write each candidate as a complete function or otherwise isolated implementation. This makes behavior comparison, timing, and rollback possible.
- Build a representative fixture that captures the real input size, shape, class, missingness, and repeated-work pattern without making every iteration prohibitively slow.
- Keep a record of alternatives and failed attempts in a reproducible script, R Markdown document, or project artifact. Future bottlenecks may resemble the current one.
- After every meaningful change, check correctness and benchmark again. A faster result on one input is not evidence that the implementation has the same contract or better scaling.

## Reduce work before reducing overhead

- Look for a more specific existing function or package implementation before hand-optimizing general code. Specialized operations such as row/column summaries, typed iteration, interval lookup, and direct vector operations often avoid work performed by general interfaces.
- Supply information the function would otherwise infer: known column types, known factor levels, disabled labels or names when they are not needed, and other arguments that narrow the task.
- Avoid coercions that are not required by the problem. For example, applying a matrix-oriented operation to a data frame can add conversion cost and can change semantics.
- Remove outputs and calculations the caller does not use. A general statistical or formatting function may compute much more than a hot path needs; a narrow implementation can be worthwhile when its input contract is explicit.
- Cache method lookup only when dispatch itself is measured as material and the input class is guaranteed. Direct class-specific methods or lower-level internals trade flexibility and safety for speed and must not silently replace a general API.
- Treat `.Internal()` calls and structure shortcuts as last-resort, tightly contained techniques. They can skip validation, missing-value handling, dispatch, or invariants and may produce corrupt results when assumptions fail.

## Prefer whole-object operations

- Vectorization means expressing the operation over whole vectors, matrices, or arrays so that the loop runs in compiled code; it does not mean replacing a loop with an opaque `map()` call.
- Prefer purpose-built vectorized functions such as `rowSums()`, `colMeans()`, `cumsum()`, `diff()`, `cut()`, and `findInterval()` when their contracts match the problem.
- Use matrix algebra or optimized BLAS-backed operations when the problem naturally has that form, but benchmark both time and memory because a vectorized expression may create large temporary objects.
- Vectorized operations can have setup costs and nonlinear scaling. Benchmark one, several, and many elements, and retain a simpler approach when it is faster or clearer for the actual input regime.
- Keep `r-purrr` mapping when the work is genuinely per-element, heterogeneous, failure-aware, or side-effectful. Do not use mapping solely as a performance substitute for a whole-object operation.

## Avoid allocation churn and copies

- Do not grow vectors, strings, matrices, or data frames repeatedly with `c()`, `append()`, `cbind()`, `rbind()`, or iterative `paste()` in a hot loop when the result can be constructed in one pass or in known-sized storage.
- Treat repeated modification as a possible copy-on-modify cost. Profile memory, inspect allocations, and benchmark at increasing sizes instead of assuming that an assignment is in-place.
- Compare CPU savings with memory cost. A single vectorized expression may be faster while allocating larger temporaries; a lower-allocation implementation may use more R-level instructions. Choose according to peak-memory limits, concurrency, and end-to-end throughput.
- Preserve output type, dimensions, names, classes, ordering, and missing-value behavior while changing storage or construction strategy.

## Use a staged transformation

For a repeated statistical or data operation, a reliable sequence is:

1. Keep the original implementation as the behavioral reference.
2. Remove work that is outside the required result.
3. Replace scalar summaries with row/column or other whole-object operations.
4. Eliminate repeated allocation and unnecessary coercion.
5. Benchmark each stage against the reference on representative sizes.
6. Test exact or contract-level equivalence, including edge cases, before adopting the result.

This staged approach helps separate a large gain from several risky micro-changes and makes regressions easier to locate.

## Balance the tradeoffs

- Prefer the fastest implementation that remains correct, understandable, and within the memory budget. A small speedup is not worthwhile if it makes the code fragile or consumes the saved time in maintenance.
- Accept generality costs when they are part of the public contract. Specialize only behind a validated boundary that rejects or routes unsupported inputs safely.
- Preserve numerical accuracy unless the user explicitly accepts a different tolerance. Faster one-pass or lower-level calculations can change floating-point results or missing-value behavior.
- Reconsider the algorithm or data representation when local tuning has plateaued. A different data structure, lookup strategy, batching boundary, or parallel design may dominate function-level tweaks, but measure setup and coordination overhead too.

## Routing

- Use `r-core` for vectors, matrices, data frames, coercion, recycling, attributes, missingness, and copy-on-modify behavior that must remain stable during optimization.
- Use `r-purrr` when the optimization concerns typed mapping, list-columns, per-element failure handling, or the overhead and correctness of sequential versus parallel iteration.
- Use `r-project-layout` for keeping optimization fixtures, benchmark scripts, profiling outputs, and reproducible performance notes in the right project locations.
- Use `r-testing` for regression tests, behavioral equivalence, edge cases, deterministic fixtures, and explicit performance-test boundaries; do not encode fragile machine-specific timing thresholds as ordinary unit tests.
