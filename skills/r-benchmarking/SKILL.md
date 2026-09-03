---
name: r-benchmarking
description: "Use to measure R performance with profiling and microbenchmarks, design representative workloads, and interpret CPU time, allocations, garbage collection, and scaling. Do not use this skill to choose or implement an optimization without measurement evidence."
license: MIT
compatibility: "R 4.1+ and the documented packages; compatible with Claude Code, Cursor, Gemini CLI, Codex, and similar Agent Skills clients."
user-invocable: true
allowed-tools: "Read Edit Write Glob Grep Bash(R:*) Bash(Rscript:*) Bash(git:*) Agent"
metadata:
  author: tdstein
  version: "0.1.0"
  openclaw:
    emoji: "⏱️"
    homepage: "https://github.com/tdstein/cc-skills-r"
    requires:
      bins:
        - R
        - Rscript
    install: []
---

# R performance measurement

Use this skill to establish where time and memory are spent, compare narrowly defined alternatives, and report evidence that can guide an optimization. Keep measurement separate from changing the implementation: after the bottleneck and a credible comparison are known, route the change to `r-performance`.

## Choose the measurement mode

- Use **profiling** for a realistic end-to-end workload when the slow part is not known. Use sampling rather than intuition to find hot call paths.
- Use **microbenchmarking** for a small, isolated operation when comparing already identified alternatives. Do not treat a microbenchmark as a prediction of total application time.
- Use both when appropriate: profile the real workflow to locate the bottleneck, then benchmark candidate implementations in isolation with representative inputs.

## Profile realistic work

- Profile the workload users actually run, including representative data size, shape, classes, missingness, and control-flow branches. A toy input can hide scaling and allocation behavior.
- Prefer `profvis::profvis()` for an interactive view tied to source lines; use `utils::Rprof()` and `summaryRprof()` when a textual or scriptable record is more useful. Put the workload in a source file when source-line mapping matters.
- Read the source-time view and the call-stack/flame-graph view together. A function may appear expensive because it is called repeatedly, not because one invocation is intrinsically slow; inspect callers before changing the callee.
- Treat sampling results as estimates. Timer resolution, system load, and short operations introduce variation, so rerun important profiles and focus on sustained hot paths.
- Name anonymous functions when a profile is hard to interpret. Remember that sampling profiles stop at the R/C boundary: they show calls into compiled code, not the internals of that compiled code.
- Account for lazy evaluation when interpreting call stacks. Work may appear under the function that forces an argument rather than under the expression that supplied it; force an argument earlier only when doing so clarifies or changes a deliberate evaluation contract.

## Inspect memory and garbage collection

- In a profile, treat `<GC>` as a signal to investigate allocation churn, not as an independent bottleneck. Large amounts of garbage collection often mean many short-lived objects are being created.
- Correlate time with the memory view and source lines. Repeated growth, concatenation, coercion, or copy-on-modify can allocate and discard large objects even when the source code looks simple.
- Measure allocation alongside CPU time. A change that reduces elapsed time by increasing peak memory may be appropriate for a batch job but unacceptable for a memory-constrained service; record the relevant operating constraint.

## Design a useful microbenchmark

- Encapsulate each complete alternative in a named function when behavior is nontrivial. Keep setup outside the timed expression unless setup cost is part of the user-visible operation.
- Construct inputs that are large enough to expose the real operation but small enough to run repeatedly. Benchmark multiple sizes when algorithmic scaling or vectorization is in question.
- Use `bench::mark()` for small operations. Preserve its equality check by default; use `check = FALSE` only when outputs intentionally differ and validate equivalence separately with `r-testing`.
- Inspect at least `min`, `median`, `itr/sec`, `mem_alloc`, and `n_gc`; use the raw `time` and `memory` list-columns when distribution or allocation details matter. The minimum estimates a best case, while the median is more representative than the mean for right-skewed timings.
- Check units and practical impact. A nanosecond-level difference matters only if the operation is called often enough, and a fast inner loop may be irrelevant if an outer step dominates.
- Use `system.time()` only as a coarse fallback. Repeat the expression enough times to rise above timer noise, then divide by the number of repetitions; distinguish that estimate from a high-precision microbenchmark.
- Compare across input sizes and realistic object types. Dispatch, setup, and allocation overhead can dominate small inputs and disappear for large ones; do not generalize a result outside the regime measured.

## Report evidence

State the workload, environment assumptions, expressions, correctness check, timing summary, allocation/GC observations, input sizes, and practical conclusion. Keep failed alternatives when the result will help future work. If the result does not identify a meaningful bottleneck or improvement opportunity, say so rather than forcing an optimization.

## Routing

- Use `r-core` for input type, size, missingness, attributes, recycling, and copy-on-modify semantics that determine whether two benchmark cases are comparable.
- Use `r-purrr` for mapping-based workloads, typed iteration, list-columns, and explicit analysis of per-element or parallel overhead.
- Use `r-project-layout` for locating benchmark scripts, reproducible fixtures, reports, and generated profiling artifacts.
- Use `r-testing` to verify that alternatives preserve values, classes, dimensions, names, ordering, warnings, errors, and edge-case behavior; performance evidence is not a substitute for behavioral tests.
