---
name: r-interop
description: "Use when integrating R with C or C++, especially .Call interfaces, Rcpp code, native registration, memory protection, type conversion, portability, or native-code testing."
license: MIT
compatibility: "R 4.1+ and the documented packages; compatible with Claude Code, Cursor, Gemini CLI, Codex, and similar Agent Skills clients."
user-invocable: true
allowed-tools: "Read Edit Write Glob Grep Bash(R:*) Bash(Rscript:*) Bash(git:*) Agent"
metadata:
  author: tdstein
  version: "0.1.0"
  openclaw:
    emoji: "🔌"
    homepage: "https://github.com/tdstein/skills-r"
    requires:
      bins:
        - R
        - Rscript
    install: []
---

# R interoperability

Treat native code as a narrow, explicitly tested boundary around R code. Define the R-facing contract first: accepted types and lengths, missing-value behavior, recycling or indexing rules, attributes and classes, error behavior, ownership, and portability assumptions. Keep the native implementation small enough that its invariants can be reviewed independently.

## Choose the boundary

- Prefer ordinary R code when vectorisation, allocation reduction, or a better algorithm removes the bottleneck.
- Prefer Rcpp for new C++ implementations. It provides typed wrappers for common R vectors, matrices, lists, data frames, functions, attributes, and missing values, while hiding much of the raw SEXP and protection protocol.
- Use the raw C API when compatibility with an existing C implementation, a very small primitive, direct inspection of R internals, or a required C ABI justifies the additional safety burden. Do not choose C merely because it is older or appears lower level.
- Use `.Call()` as the normal R-to-C entry point for fixed arguments. Consider `.External()` only when a variable-length call or access to the unevaluated pairlist is a real part of the contract. Do not use the legacy `.C` interface for new designs.

## Design the R-facing API

- Put user-facing coercion, defaults, length checks, class checks, and actionable messages in an R wrapper when that makes the contract clearer. Keep the native routine focused on validated inputs and computation.
- If validation must happen in native code, inspect `TYPEOF()` or use the appropriate `is*()` helper before accessing a data pointer. Reject malformed inputs before indexing or assuming dimensions.
- Keep R and C++ indexing conventions visible: R is one-based at the API boundary; C and C++ arrays are zero-based internally. Convert deliberately and test the first, last, empty, and out-of-range cases.
- Make recycling explicit. Do not silently reproduce R's recycling rules unless they are part of the documented contract.
- Preserve or deliberately reconstruct names, dimensions, dimnames, class, and other attributes. Attributes are metadata, not a substitute for validating the underlying representation.
- Treat calls back into R as a dynamic boundary: the function may return different R types, raise conditions, or depend on evaluation and named arguments. Use a broad Rcpp return type only when that variability is intentional.

## .Call and raw C API invariants

For a `.Call()` routine:

1. Accept and return `SEXP` values.
2. Include the R headers needed by the API.
3. Convert only after checking the expected `SEXPTYPE`, length, dimensions, and relevant attributes.
4. Allocate output with the correct R type and size.
5. Protect every newly allocated R object until it is reachable from a protected object or is returned, and balance every `PROTECT()` with `UNPROTECT()`.
6. Return the result only after all intermediate protection obligations are satisfied.

Use `R_xlen_t` with `xlength()`/`XLENGTH()` for lengths that may exceed the 32-bit integer range. Avoid storing long-vector lengths in `int`, and use the matching pointer/accessor conventions for long-vector-safe code.

Remember that R objects are SEXPs: numeric, integer, logical, character, list, function, environment, call, pairlist, and promise objects have different representations. Lists are `VECSXP`; argument lists, calls, and attributes may be pairlists (`LISTSXP`) and require `CAR()`, `CDR()`, `TAG()`, and related accessors rather than vector indexing.

## Protection, mutation, and garbage collection

- Assume any operation that allocates an R object can trigger garbage collection, including vector allocation, scalar constructors, coercion, string creation, pairlist construction, and call construction.
- Protect all newly allocated intermediates, not just the final result. Keep the protection count easy to audit; use `PROTECT_WITH_INDEX()`/`REPROTECT()` only when replacement of a protected object is actually needed.
- Arguments already reachable from the call do not normally need protection, but derived objects and objects created while building another object do.
- Exercise protection-sensitive code with aggressive garbage-collection diagnostics such as `gctorture()` when available. A clean normal run does not prove protection correctness.
- Do not mutate an input merely because its data pointer is writable. R uses lazy copy-on-modify and shared objects, so direct mutation can change aliases in the caller. Duplicate first (`duplicate()` or an appropriate shallow copy), or construct a new result.
- In Rcpp, understand whether an operation aliases an R object, creates a copy, or returns a view-like wrapper before mutating it. Prefer clear output construction over clever in-place changes unless profiling and tests justify the optimization.

## Type conversion and missing values

- Match R's type system intentionally. R integer, numeric, logical, character, complex, raw, list, and scalar values are not interchangeable merely because a C or C++ scalar can hold them.
- In raw C, use the matching accessors (`REAL`, `INTEGER`, `LOGICAL`, `COMPLEX`, `RAW`, `STRING_ELT`, `VECTOR_ELT`) and setters. Character elements are SEXPs (`CHARSXP`), not mutable C strings; avoid hand-written string mutation when Rcpp or a safer library is appropriate.
- Protect objects returned by coercion or scalar-constructor helpers when they are newly allocated.
- Define the distinction among `NA`, `NaN`, and positive or negative infinity. For raw C use the matching constants and predicates (`NA_*`, `ISNA`, `ISNAN`, `R_FINITE`); in Rcpp use type-aware missing-value representations rather than assuming C++ scalar semantics match R.
- A C++ `bool` cannot represent R's three-state logical vector. Use an integer or a logical-vector wrapper when `NA` must survive conversion.
- Check empty inputs before reading element zero, and decide how zero length, missing values, non-finite values, and malformed dimensions should be returned or rejected.
- Convert STL containers only when their ordering, uniqueness, key semantics, and missing-value behavior match the R contract. Reserve capacity when output growth is expected, but measure before optimizing.

## Rcpp implementation workflow

- Use `cppFunction()` or `sourceCpp()` for small experiments and focused prototypes. Keep standalone source in `.cpp` files with the Rcpp header and export attributes; embedded R blocks can provide executable smoke tests.
- For package code, keep native sources under `src/`, declare `Rcpp` in `DESCRIPTION` with the appropriate `Imports` and `LinkingTo` entries, configure native-library loading, and rerun `Rcpp::compileAttributes()` whenever exported signatures or attributes change.
- Treat `Rcpp::export` as the C++-to-R wrapper generator. It is separate from package-level `@export`, which controls the public R namespace.
- Prefer standard-library algorithms and data structures when they clarify intent and have appropriate complexity. Do not port a vectorised R function to C++ automatically: compare the allocation pattern, numerical accuracy, maintainability, and expected call volume first.
- Benchmark against the best R implementation, not a deliberately slow loop. Verify outputs before interpreting speedups; a faster implementation that changes numerical stability, missing-value propagation, or recycling semantics is not a drop-in replacement.
- Keep compiler standards and external-library assumptions explicit. Avoid relying on one developer's compiler, platform-specific flags, or implicit transitive includes.

## Registration and portability

- Use native routine registration and the package's generated registration machinery where supported. Keep the R-visible symbol, native function signature, registration table, and wrapper in sync; avoid accidental dependence on dynamic symbol lookup.
- Treat generated files as generated: update them through the project’s established Rcpp or package tooling rather than hand-editing them.
- Keep C and C++ entry points compatible with the expected linkage. If C++ functions are called through a C ABI, use the appropriate `extern "C"` boundary and do not expose C++ name mangling to the loader.
- Avoid undefined behavior, unchecked casts, platform-sized assumptions, and integer overflow. Use R's allocation and error mechanisms instead of raw process termination.
- Test on the supported operating systems and compiler families when native code is shipped. Watch for differences in compiler standards, math libraries, integer widths, endianness, unavailable headers, and C++ ABI details.
- Do not require end users to have a compiler for ordinary package installation unless source installation is an explicit product requirement; distribute packages through the normal binary/source package workflow.

## Diagnostics and failure handling

- Raise errors through R-aware mechanisms (`error()`/`Rf_error()` in raw C, `Rcpp::stop()` in Rcpp) so R can unwind safely. Never use `abort()`, `exit()`, or C++ exceptions that escape an R entry point.
- Include the operation and the relevant argument in the diagnostic, without dumping secrets or huge inputs. Put friendly validation and domain context in the R wrapper when possible.
- Preserve native compiler diagnostics during development: compile from a stable source file, keep line numbers, and isolate the smallest failing function.
- Distinguish compile/link/load failures from runtime contract failures, protection bugs, and numerical mismatches. A segmentation fault or stack imbalance is an interface-safety defect, not an ordinary user input error.
- When debugging raw C, inspect `Rinternals.h`, the actual `SEXPTYPE`, lengths, attributes, and registration path. Compare with a small known-good `.Call()` function before changing complex code.

## Testing

Test the boundary at more than one level:

- R wrapper tests: accepted coercions, rejected types, lengths, dimensions, classes, names, warnings, errors, and stable missing/non-finite behavior.
- Native unit tests: indexing, empty inputs, boundary sizes, duplicate/shared inputs, arithmetic edge cases, and deterministic algorithms.
- Integration tests: package load, registered symbol lookup, generated wrappers, clean-session behavior, and installation on supported toolchains.
- Memory-safety tests: protection counts, repeated allocation, and garbage-collection stress for raw C; aliasing and mutation behavior for Rcpp.
- Numerical/performance tests: compare against a trusted R reference with suitable tolerances, then benchmark realistic workloads and include a correctness check.
- Optional-toolchain tests: skip clearly when Rcpp, a compiler, or another native dependency is unavailable; do not silently replace the implementation under test.

Keep tests deterministic. Seed random generators, use small fixtures for failure cases, and separate performance benchmarks from correctness tests so timing noise does not obscure regressions.

## Routing

- Use `r-dependencies` for `DESCRIPTION`, `NAMESPACE`, `LinkingTo`, native-library dependencies, compiler/toolchain declarations, and lockfile or reproducibility decisions.
- Use `r-project-layout` for package `src/` placement, generated files, package scaffolding, and the boundary between reusable package code and analysis/report code.
- Use `r-benchmarking` for profiling and benchmark design, and `r-performance`
  for algorithm choice, allocation analysis, optimization, and deciding
  whether native code is justified. If those skills are not installed in the
  project, keep performance advice local to this skill rather than inventing a
  second workflow.
- Use `r-errors` for condition classes, user-facing diagnostics, recovery, and error tests that cross the R/native boundary.
- Use `r-testing` for test organization, fixtures, isolation, optional dependency skips, integration tiers, and expectation style.
