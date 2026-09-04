---
name: r-functions
description: "Use for designing, debugging, or reviewing ordinary R functions: contracts, calls, lexical scoping, argument matching, lazy evaluation, control flow, recursion, and function composition. Route data semantics to r-core, functional iteration to r-purrr, conditions to r-errors, and verification to r-testing."
license: MIT
compatibility: "R 4.1+ and the documented packages; compatible with Claude Code, Cursor, Gemini CLI, Codex, and similar Agent Skills clients."
user-invocable: true
allowed-tools: "Read Edit Write Glob Grep Bash(R:*) Bash(Rscript:*) Bash(git:*) Agent"
metadata:
  author: tdstein
  version: "0.1.0"
  openclaw:
    emoji: "🧩"
    homepage: "https://github.com/tdstein/skills-r"
    requires:
      bins:
        - R
        - Rscript
    install: []
---

# R functions

Design functions around an explicit contract: what arguments are accepted, what
result is returned, what is evaluated, and what state or conditions are exposed.
Use R's function semantics deliberately; many subtle bugs come from invisible
argument matching, lazy promises, or name lookup rather than from the algorithm.

## Define the contract

- State input type, length, names, missingness, allowed values, and whether
  `NULL` has a special meaning. State output type, size, class, names, and
  visibility when those properties matter.
- Decide whether the function is pure, mutates external state, performs I/O,
  or primarily exists for a side effect. Side-effect functions should usually
  return an invisible, useful value rather than an incidental diagnostic.
- Prefer a named function when it has a reusable contract, needs multiple
  branches, or deserves its own tests. Use an anonymous `\(x) ...` function for
  short, local behavior that is clearer at the call site.
- Remember that an R function consists of formals, body, and enclosing
  environment. Inspect `formals()`, `body()`, and `environment()` when
  debugging a closure; primitive functions are the important base-R exception.

## Understand calls and lexical scope

- R resolves names lexically: first in the current call frame, then through
  the environment where the function was defined, then through its parents.
  Bindings inside a function mask outer bindings.
- Every invocation gets a fresh call environment. Local assignments therefore
  do not persist across calls unless state is deliberately captured in an
  enclosing environment or stored elsewhere.
- Lookup is dynamic in time: external names are resolved when the function runs.
  Avoid accidental global dependencies, use explicit namespaces or injected
  dependencies where appropriate, and inspect `codetools::findGlobals()` when
  a function's dependencies are unclear.
- Do not reuse one name for both a function and a non-function in nearby scopes.
  In a call position R can skip a non-function binding while looking for a
  callable object, which is legal but needlessly confusing.
- When syntax hides the call structure, rewrite it mentally or temporarily in
  prefix form: `` `+`(x, y)``, `` `names<-`(x, value)``, or
  `` `[`(x, i)``. This is useful for reading, debugging, and passing existing
  operators as function values; do not override base operators globally.

## Match arguments intentionally

- R matches exact argument names first, then unique partial names, then
  remaining arguments by position. Use position only for the first one or two
  obvious arguments; name optional or less familiar arguments.
- Never rely on partial matching in new code. During review, consider
  `options(warnPartialMatchArgs = TRUE)` to expose fragile calls.
- Treat `...` as part of the public contract, not as a generic escape hatch.
  Use it to forward arguments to a known callee or to support a deliberate
  generic interface, document where forwarded arguments go, and reject or
  inspect unexpected arguments when the API needs strictness. `list(...)`
  evaluates and collects them; `..1`, `..2`, and similar positional accessors
  are niche and reduce readability.

## Use lazy evaluation deliberately

- Arguments arrive as promises containing an expression, its evaluation
  environment, and a cached value. An unused argument is never evaluated; an
  argument is normally evaluated at most once, when first needed.
- A user-supplied argument is evaluated in the caller's environment, while a
  default is evaluated in the function's evaluation context. Do not assume
  that visually identical supplied and default expressions behave identically.
- Keep defaults simple and easy to reason about. Although defaults may refer to
  other arguments or later local bindings, such dependencies make evaluation
  order part of the hidden contract.
- Prefer `NULL` as an explicit “not supplied / use derived default” sentinel
  when that is semantically available. Use `missing()` only when distinguishing
  omission from an explicitly supplied value is genuinely required.
- Use `&&` and `||` for scalar guard chains because they short-circuit; use
  `&` and `|` for vectorized logical operations. This distinction is often the
  difference between safe validation and accidental recycling or length errors.
- Use `force()` when a delayed code argument or captured value must be
  evaluated at a deliberate point. Otherwise let laziness avoid unnecessary
  work, especially in conditional branches.

## Choose control flow by shape

- Use `if` for one scalar condition. It is an expression and returns a value;
  without `else`, a false branch yields `NULL` invisibly. Do not pass a
  vector, `NA`, or a zero-length condition where a scalar decision is needed.
- Use `ifelse()` only for vectorized branching with compatible `yes` and `no`
  types and an output whose missingness and coercion are acceptable. For
  richer table expressions, route to the project's vectorized/data-masking
  conventions rather than hiding them in an ordinary function.
- Prefer character `switch()` for a small named dispatch. Include an explicit
  failure branch so an unknown option does not silently become `NULL`; avoid
  numeric dispatch when its indexing failure modes would be surprising.
- In a `for` loop, preallocate output and fill it by index. Use
  `seq_along(x)`, not `1:length(x)`, so empty inputs do not create the bogus
  index `1`. Be aware that direct iteration can strip attributes from S3
  vectors; use `x[[i]]` when element class matters.
- Use `next` to skip an iteration and `break` to leave the loop. Use `while`
  when the stopping condition is discovered during execution and `repeat`
  only when an explicit `break`-based loop is the clearest design; update or
  validate the termination state on every path.
- For ordinary element-wise mapping, prefer the `r-purrr` skill. This skill
  covers the function and control-flow semantics that make a custom loop or
  callback correct.

## Recursion

- Give every recursive function a clear base case, make every recursive call
  move toward it, and keep the return contract identical across base and
  recursive branches.
- Validate termination on empty, singleton, and malformed inputs before
  recursing. Avoid mutating shared state between recursive calls unless that
  state is an explicit part of the design.
- Use recursion when the problem's structure is naturally recursive (for
  example, a tree or nested language object). For large linear traversals,
  prefer an iterative loop or a purrr mapper to avoid unnecessary call-stack
  depth and to make resource use easier to control.

## Compose functions and return results

- Use nesting for short expressions, named intermediate values when a step is
  important or needs inspection, and `|>` for a readable linear sequence of
  single-object transformations. A pipe is a poor fit for branching,
  multiple independent inputs, or a computation whose intermediate names
  carry meaning.
- Treat operators as functions when that makes composition clearer, such as
  `lapply(x, \`+\`, 3)`. Custom infix functions should have two clear
  arguments and a predictable precedence/associativity story; avoid inventing
  one when a named function is easier to discover.
- Replacement functions named `xxx<-` must accept `x` and `value` (with any
  extra arguments between them), return the modified object, and be understood
  as producing a replacement rather than mutating in place.
- Let the final expression provide the normal return value. Use explicit
  `return()` for an early exit that materially clarifies control flow, not as
  decoration around every branch. Use `invisible()` for side-effect APIs whose
  useful result should not print automatically.

## Clean up on every exit

- Register cleanup immediately after acquiring a resource or changing state.
  Use `on.exit(..., add = TRUE)` so later cleanup registrations do not erase
  earlier ones, and choose cleanup order deliberately when operations depend
  on one another.
- Use this pattern for working directories, options, connections, devices,
  sinks, temporary files, and other process state. For common temporary-state
  helpers, prefer `withr` when it is already a project dependency.
- If a function evaluates a delayed code block in temporary state, restore
  state with `on.exit()` and then `force(code)` at the intended point.

## Routing boundaries

- Use `r-core` for vector, list, tibble/data-frame, recycling, missing-value,
  and output-shape semantics; this skill only describes how functions and
  control flow carry those contracts.
- Use `r-purrr` for `map()` families, typed mapping, list-columns, parallel
  mapping, and per-element failure strategies. Use this skill for callback
  contracts, argument forwarding, and the semantics of a custom function used
  by those tools.
- Use `r-errors` for `stop()` versus warnings/messages, rlang condition
  classes, handlers, recovery, and backtraces. A function contract should say
  when failure occurs, while `r-errors` defines the condition mechanism.
- Use `r-testing` to turn contracts into tests, including lazy branches,
  argument defaults, recursion termination, cleanup after errors, visibility,
  and control-flow edge cases.

## Verification checklist

Before considering a function complete, check:

- named and positional calls behave as intended, including omitted and
  explicitly `NULL` arguments;
- unused or conditionally used arguments do not trigger unexpected work;
- empty, scalar, missing, and boundary inputs preserve the stated contract;
- external dependencies are visible and stable under a fresh call;
- normal return, error exit, and cleanup paths all restore required state;
- the chosen composition and iteration form remains readable at the expected
  call site.
