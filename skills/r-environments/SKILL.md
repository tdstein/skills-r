---
name: r-environments
description: "Use when R code depends on environment identity, bindings, lexical lookup, namespaces, caller context, closures, or state that persists across calls; route expression construction and general function design elsewhere."
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

# R environments

Use environments when the identity of a name-to-value store, its parent chain, or its mutation behavior is part of the program’s contract. Environments are central to lexical scoping, package namespaces, closures, call context, and deliberately persistent state.

## Model the structure first

- An environment is a set of uniquely named bindings. Bindings have no meaningful order, and environments are not copied when modified.
- Every environment has a parent except `emptyenv()`. Name lookup checks the current environment, then follows parents until the name is found or the empty environment is reached.
- Compare environments with `identical()`, never `==`. Inspect identity and structure with `env_print()`, `env_names()`, `env_parent()`, and `env_parents()`; use `new.env()` or `rlang::env()` to construct one.
- Treat an environment as a reference object: assigning it to another variable creates another reference to the same bindings. It can even contain a binding to itself, so avoid assuming that recursive structures can be printed or serialized like lists.
- Do not use list indexing assumptions. `$` and character `[[` access named bindings; `[` and numeric `[[` do not describe environment lookup. A missing binding accessed with `$` or `[[` yields `NULL`, which is different from a binding whose value is explicitly `NULL`.

## Manipulate bindings deliberately

- Use `env_has()` to distinguish an absent name from a present `NULL` value.
- Use `env_get()` when absence should be an error, or provide `default` when a fallback is part of the contract.
- Use `env_poke()` for one in-place binding and `env_bind()` for several. Use `env_unbind()` to remove a binding; assigning `NULL` does not remove the name.
- Prefer explicit string names at dynamic boundaries. Base equivalents include `get()`, `assign()`, `exists()`, and `rm()`, but check their `inherits` behavior: by default they may search the parent chain.
- Reserve `env_bind_lazy()`/`delayedAssign()` for values that should be computed on first access, and `env_bind_active()`/`makeActiveBinding()` for values recomputed on every access. Document the surprising evaluation behavior and test it explicitly.

## Keep lexical and dynamic lookup separate

- `<-` creates or updates a binding in the current execution environment.
- `<<-` searches parent environments for an existing binding and updates the first one found. If it finds none, it creates a binding in the global environment; treat that fallback as a defect unless it is intentional and documented.
- For a controlled ancestor update, walk parents with `env_has()` and `env_poke()` and stop at `emptyenv()`. This makes failure explicit and avoids an accidental global write.
- A function’s enclosing environment is captured when the function is created. It determines where free variables are found and is available with `rlang::fn_env()` or base `environment()`.
- The environment that contains a binding to a function is a different concept from the function’s enclosing environment. A function can be stored in one environment while capturing another.
- A call creates a fresh execution environment whose parent is the function’s enclosing environment. Locals normally disappear after return; they persist only when something retains a reference, such as a returned environment or closure.
- The caller environment is where a function was called, not where it was defined. Use `rlang::caller_env()` or `parent.frame()` for APIs that intentionally inspect the caller. Do not substitute caller lookup for lexical lookup without a clear interactive or metaprogramming reason.

## Recurse over parent chains safely

For “find the environment where…” operations, use three explicit cases:

1. Stop at `emptyenv()` and raise a useful error.
2. Return the current environment when the binding satisfies the condition.
3. Recurse or iterate with `env_parent()` otherwise.

Make the search policy explicit: current environment only versus inherited lookup, first match versus all matches, and any predicate such as “binding is a function.” Avoid silently stopping at the global environment when package or namespace ancestry matters.

## Understand package lookup

Distinguish package loading from attachment:

- `pkg::fun` can load a package without placing its package environment on the interactive search path.
- `library(pkg)` or `require(pkg)` attaches a package environment and changes the parent chain below the global environment.
- `search()` reports the search-path names; `rlang::search_envs()` returns the corresponding environments. `Autoloads` uses delayed bindings, and `base_env()` is the base package environment.

For a package, separate two lookup roles:

- The package environment is the user-facing interface containing exported bindings and is affected by the attachment order.
- The namespace environment is the implementation-facing interface captured by package functions. It contains internal bindings as well as exports and has an imports environment controlled by `NAMESPACE`, followed by the base namespace.

Use namespace imports and explicit qualification to make package code independent of the user’s attached packages. Do not infer that a function’s package environment is its lexical environment; the function’s enclosing environment is what controls its free-variable lookup.

## Use closures and state intentionally

- A closure is a function plus its captured enclosing environment. Function factories work by creating a private execution environment, then returning a function that retains it.
- Stateful closures should keep mutable state in a deliberately scoped environment, expose narrow operations, and avoid leaking the environment as a public mutable object.
- For package state, a private environment such as `new.env(parent = emptyenv())` prevents accidental fallback lookup. Provide getter/setter or operation functions rather than exporting the store.
- A setter that returns the old value makes temporary state changes easier to restore with `on.exit()`.
- Use an environment as a reference-backed cache or name-keyed map when identity and constant-time name lookup matter. For richer object behavior, prefer an abstraction such as R6 rather than exposing raw environment mutation throughout the codebase.
- State is process-local and order-sensitive. Define initialization, reset, cleanup, and concurrency expectations; never let a missing binding silently create global state.

## Verification

For environment-sensitive code, test the contract rather than only the returned value:

- Check `identical()` relationships, parent chains, binding presence, and whether `NULL` means “stored” or “absent.”
- Exercise shadowing, missing names, `emptyenv()` termination, and attempted ancestor updates.
- For closures, verify that each factory call gets independent state while repeated calls to one closure share only the intended state.
- For package-facing code, test behavior with different attachment orders and confirm that internal lookup uses declared imports.
- For active or delayed bindings, assert access timing and repeated-access behavior.
- Use `r-testing` for fixtures and isolation; reset private environments or restore temporary mutations with `on.exit()` so tests do not depend on execution order.

## Boundaries and routing

- Use this skill for the environment mechanics behind closures, function factories, package namespaces, caller inspection, caches, and stateful APIs.
- Route general function signatures, factories, operators, and function composition to an `r-functions` skill when available; retain only the closure/environment interaction here.
- Route `DESCRIPTION`, `NAMESPACE`, imports/exports, package loading, and `renv` decisions to `r-dependencies`; use this skill for the lookup model that explains those decisions.
- Route `quote()`, `eval()`, quosures, data masks, and DSL construction to an `r-metaprogramming` skill when available; use this skill only for the environment in which an expression is resolved.
- Route test organization and expectation style to `r-testing`; use this skill to identify the environment invariants and state-reset requirements that tests must cover.
