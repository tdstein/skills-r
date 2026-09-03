---
name: r-functional-programming
description: "Use for R functional-programming design beyond package-specific iteration: pure functions, composition, higher-order functions, closures, function factories, function operators, memoisation, and deliberate state. Route purrr iteration to r-purrr, ordinary function semantics to r-functions, environments to r-environments, conditions to r-errors, and verification to r-testing."
license: MIT
compatibility: "R 4.1+ and current releases of the documented packages; compatible with Claude Code, Cursor, Gemini CLI, Codex, and similar agents."
user-invocable: true
allowed-tools: "Read Edit Write Glob Grep Bash(R:*) Bash(Rscript:*) Bash(git:*) Agent"
metadata:
  author: tdstein
  version: "0.1.0"
  openclaw:
    emoji: "🧠"
    homepage: "https://github.com/tdstein/cc-skills-r"
    requires:
      bins:
        - R
        - Rscript
    install: []
---

# R functional programming

Use functional programming to decompose a problem into small functions with
explicit contracts, then combine those functions through composition or
higher-order interfaces. R does not enforce purity, so make the boundary
between deterministic computation and I/O, randomness, logging, mutation, or
other effects visible.

## Choose the higher-order shape

- Use a **functional** when a function should apply a callback across inputs,
  reduce a sequence, or search with a predicate. For `purrr::map*()`,
  `map2()`, `pmap()`, `reduce()`, and related list workflows, use `r-purrr`.
- Use a **function factory** when configuration, data, or precomputation should
  produce a reusable function. The returned function is a closure over the
  factory's execution environment.
- Use a **function operator** when behavior should wrap or modify another
  function: logging, timing, retrying, delaying, tracing, caching, or
  converting failures into data. Operators are factories whose input is a
  function and should compose cleanly with functionals.
- Use ordinary named functions when the behavior has a reusable contract,
  substantial branching, or its own tests. An anonymous `\(x) ...` function is
  appropriate for short local behavior.

## Design rules

- Prefer pure functions for transformations: the result should depend on the
  inputs and the function should not change external state. Isolate impure
  boundaries such as file/network I/O, random draws, time, messages, and
  assignment so the pure core is easy to test and reason about.
- Compose small functions around named intermediate results when a step needs
  inspection or has an important contract. Use a pipe for a linear sequence of
  transformations, not to hide branching, unrelated side effects, or multiple
  independent inputs.
- Treat a function's formals, body, and enclosing environment as part of its
  behavior. Make dependencies explicit with namespaces or injected arguments;
  avoid accidental reliance on mutable globals.
- In a factory or operator, force captured arguments when their value must be
  fixed at construction time. Otherwise R's lazy promises can observe a
  changed binding only when the manufactured function is later called.
- Keep factory setup separate from repeated work. Precompute values that depend
  only on the configuration or data, then return a function for the varying
  parameter. Remove large temporary objects from the retained environment when
  the returned closure does not need them.
- Treat stateful closures as a narrow abstraction, not a default style. Keep
  mutable state private, use `<<-` only for an intentionally captured binding,
  document initialization/reset and order dependence, and consider an explicit
  environment or R6 object when state has multiple operations or invariants.
- Function operators must preserve the wrapped function's arguments and return
  contract unless changing that contract is the purpose. Force the wrapped
  function and operator configuration at construction, forward `...`
  deliberately, and document wrapper order because composing delay, logging,
  retries, caching, and side effects is not generally commutative.
- Memoise only functions whose result is determined by their inputs and whose
  relevant external state is stable for the cache lifetime. Do not memoise
  randomness, current time, mutable files, network responses, or other
  time-varying effects without an explicit invalidation policy.

## Boundaries and routing

- Use `r-purrr` for package-specific mapping, typed outputs, list-columns,
  `walk()` side effects, `reduce()`/predicate families, and per-element failure
  handling.
- Use `r-functions` for ordinary function contracts, argument matching,
  `...`, lazy evaluation, control flow, recursion, and basic composition.
- Use `r-environments` when environment identity, lexical lookup, captured
  bindings, namespaces, `<<-`, caches, or persistent state is the issue.
- Use `r-errors` for condition classes, handlers, backtraces, recovery, and
  the policy for converting failures to values. `safely()` and `possibly()`
  are purrr-specific applications of those policies.
- Use `r-testing` to verify purity boundaries, factory independence, forced
  configuration, operator return contracts, cache behavior, state reset, and
  side-effect isolation. Test observable behavior rather than the incidental
  shape of a closure's environment.
- Use `r-core` when the functional design depends on vector/list types,
  recycling, missingness, attributes, or output shape; use `r-style` for
  naming and readable composition.
