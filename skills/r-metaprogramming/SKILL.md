---
name: r-metaprogramming
description: "Use when R code must inspect, generate, capture, translate, or evaluate code: expressions, calls, parsing, quotation, quasiquotation, quosures, data masks, tidy evaluation, or DSL translation. Route ordinary function design, data semantics, environment mechanics, and condition handling to the neighboring skills."
license: MIT
compatibility: "R 4.1+ and the documented packages; compatible with Claude Code, Cursor, Gemini CLI, Codex, and similar Agent Skills clients."
user-invocable: true
allowed-tools: "Read Edit Write Glob Grep Bash(R:*) Bash(Rscript:*) Bash(git:*) Agent"
metadata:
  author: tdstein
  version: "0.1.0"
  openclaw:
    emoji: "🛠️"
    homepage: "https://github.com/tdstein/skills-r"
    requires:
      bins:
        - R
        - Rscript
    install: []
---

# R metaprogramming

Use this skill when code itself is an input, output, or execution plan. Keep
the distinction between code, the value produced by code, and the environment
that gives names their meaning explicit. Prefer structured expressions and
quosures over string manipulation and implicit caller lookups.

## Start with the representation

- Treat parsed R code as an abstract syntax tree (AST). The important nodes are
  scalar constants, symbols, calls, and pairlists; an expression vector is a
  container of expressions rather than one AST node. Constants self-quote,
  symbols name bindings, and calls have the function in position one followed
  by their arguments.
- Inspect before transforming. Use `rlang::is_syntactic_literal()`,
  `is.symbol()`, `is.call()`, `is.pairlist()`, `lobstr::ast()`, `str()`, and
  `rlang::expr_print()` to distinguish structure that ordinary printing hides.
  Remember that a call can have another call in function position, as with
  `pkg::fun(x)` or `obj$method(x)`.
- Rewrite infix syntax in prefix form when precedence, associativity, or
  replacement semantics are unclear: `` `+`(x, y)``, `` `<-`(x, y)``, or
  `` `[`(x, i)``. Parentheses are themselves calls, so preserve them when
  they are semantically necessary.
- Treat calls as list-like only with an AST-aware contract. The first element
  is not an ordinary argument; named arguments may be positional, exactly
  matched, partially matched, or unnamed. Use `rlang::call_standardise()`
  only when the target function's formals make standardisation meaningful, and
  do not assume it can resolve `...` or every special form.
- When walking an AST, define explicit base cases for constants and symbols,
  recursive cases for calls and pairlists, and a stable result contract for
  every branch. Recurse through the function position when the analysis
  concerns all code; skip or treat it specially when only arguments matter.
  Handle function objects deliberately by traversing formals, body, and any
  relevant enclosing information.
- Preserve missing arguments as missing symbols. A missing argument is not
  `NULL`, `NA`, or a string; use `rlang::missing_arg()`, `is_missing()`, and
  `maybe_missing()` when constructing or splicing calls.

## Parse and deparse deliberately

- Use `rlang::parse_expr()` for one expression and `parse_exprs()` for a
  sequence. Base `parse()` returns an expression vector; convert it to a list
  when ordinary list semantics are clearer.
- Use `rlang::expr_text()` for a compact, single string representation and
  `deparse()` only when its possibly multi-element character result is part of
  the design. Parsing and deparsing are not lossless: comments, most
  whitespace, and some original backtick choices are not in the AST.
- Do not generate executable R by concatenating strings. Besides precedence
  errors, string assembly mishandles non-syntactic names and creates an
  injection surface. Prefer an AST template with `!!`, `!!!`, `call2()`, or
  `new_function()`.
- If text is unavoidable, parse only at a trusted boundary, validate the
  resulting AST before evaluation, and make the accepted grammar explicit.
  Parsing text does not make arbitrary text safe.

## Quote user input at the correct time

Choose the capture operation by both source and cardinality:

| Source | One expression | Many expressions |
| --- | --- | --- |
| Code written by the developer | `expr()` | `exprs()` |
| Expression supplied by the caller | `enexpr()` | `enexprs()` |
| A caller-supplied symbol/name only | `ensym()` | `ensyms()` |

- Use `ensym()`/`ensyms()` when an interface needs a single name, not an
  arbitrary expression. They also provide the intentional string-to-symbol
  compatibility expected by many R APIs.
- Base `quote()` and `alist()` cover developer-written code; `substitute()`
  captures caller input but also performs context-sensitive substitution. If
  substitution is intentional, provide its environment explicitly so the
  operation is visible. Avoid using `substitute()` as an unexplained mixture
  of capture and lookup.
- Quoting is not evaluation. Captured code is inert until an evaluation
  function runs it, and an evaluated argument cannot be recovered as the
  caller's original syntax after it has been forced.

## Build expressions with quasiquotation

- Use an expression template for fixed structure and `!!` to inject one
  expression, symbol, constant, or computed fragment. Unquoting works on
  structure, so it preserves precedence and protects non-syntactic names.
- Use `!!!` to splice a list of expressions into `...` or another
  multi-argument position. Preserve names intentionally; duplicate names and
  empty arguments are part of the generated call's contract.
- Use `call2()` when the function position or call shape is dynamic, especially
  when replacing a function itself would make parentheses confusing. Use
  `rlang::new_function()` when generating a function from formals, body, and
  an explicit enclosing environment.
- Use `:=` inside tidy-dots/quasiquotation when a computed expression must
  become an argument name. Use `rlang::list2()` for tidy dots and
  `rlang::exec()` when the goal is to evaluate a dynamically assembled call.
  Use base `do.call()` only when its eager list-of-values semantics and
  environment behavior are appropriate.
- For special forms whose grammar rejects `!!` in infix position, construct
  the prefix call explicitly, such as ``expr(`$`(data, !!name))``.
- Treat inlined non-expression objects as a deliberate advanced feature.
  Their printed form may omit attributes or add parentheses that are not
  literally present in the AST. Inspect with `expr_print()` and `lobstr::ast()`
  and test evaluation rather than trusting printed text.
- Never use `!!` or `!!!` as ordinary runtime operators. Outside an rlang
  quoting context they are repeated logical negation and can silently produce
  the wrong value.

## Preserve evaluation context

- `eval()` evaluates its first argument normally before it can evaluate the
  intended code. Quote the input explicitly, then select the environment:
  `eval(expr, envir)`. Use `eval()` for an ordinary expression/environment
  pair, including controlled implementations of `local()` or `source()`.
- A caller environment and a lexical/enclosing environment are different.
  Use `rlang::caller_env()` only when the API intentionally models caller
  lookup, such as wrapping a base NSE function. Use a child environment when
  code must see both caller bindings and temporary bindings created by the
  wrapper.
- A quosure is an expression bundled with the environment where it was
  supplied. Capture user code with `enquo()`/`enquos()` when its later
  evaluation must retain the caller's lexical context. This is essential for
  `...`, where different arguments can carry different environments.
- Evaluate quosures with `rlang::eval_tidy()`. It understands quosures,
  nested quosures, data masks, and tidy-evaluation pronouns. Extract
  components with `get_expr()` and `get_env()` rather than depending on
  formula-like implementation attributes.
- If a data mask will be used, capture with `enquo()` rather than `enexpr()`.
  An expression without its originating environment can accidentally resolve
  a same-named local binding inside the wrapper.
- Capture, transform, and evaluate at intentional times. Unquoting can
  force a value while constructing a call; evaluation in a mask can defer
  lookup until the generated expression runs. Document timing when side
  effects, mutable state, or expensive computations make the distinction
  observable.

## Use data masks without ambiguity

- A data mask lets a data frame, named list, or similar binding set supply
  names while the quosure's environment supplies surrounding functions and
  values. This is the mechanism behind `with()`, `subset()`, `mutate()`,
  `filter()`, `aes()`, and many small DSLs.
- In reusable code, make lookup intent explicit:
  `.data$x` means the data mask and `.env$x` means the quosure environment.
  Use `.data[[name]]` for a computed column name. These pronouns are lookup
  interfaces, not ordinary data frames or environments; missing names should
  fail clearly.
- When forwarding a data-masked argument, capture it as a quosure and unquote
  it at the callee boundary. Ordinary wrapper evaluation can otherwise resolve
  a column name in the wrapper's execution frame instead of the user's mask.
- The author is responsible for removing ambiguity in expressions the
  function constructs. For arbitrary expressions supplied by the user, state
  which names come from data and which come from the environment, and expose
  pronouns or an equivalent explicit interface.
- Validate mask results at the boundary: logical row conditions, vector sizes,
  selected columns, names, and missing-value behavior are data contracts, not
  incidental consequences of `eval_tidy()`.

## Translate code into a DSL or another language

Use the simplest translation architecture that preserves the target language's
semantics:

- For a small closed vocabulary, evaluate captured code in a child environment
  whose bindings replace operators and functions with translators. Arrange
  parent environments deliberately so known operations win over defaults, and
  so unknown names receive a defined fallback instead of accidentally calling
  real R functions.
- For open-ended symbols or calls, walk the AST first. Collect or classify
  symbols and function names, build a temporary environment for them, then
  evaluate with the translator bindings. Separate recognition from rendering
  so the default behavior is inspectable and testable.
- Generate repetitive translator functions with `new_function()` and
  quasiquotation, but keep the generated function environment explicit. Do
  not overwrite global operators or pollute the package/search path to install
  a DSL.
- Model output with a class that distinguishes trusted target-language output
  from ordinary user text. Escape ordinary text at the boundary and make
  already-rendered output idempotent; otherwise nested translation produces
  double escaping.
- Keep the source grammar, accepted operators, name resolution, output
  escaping, and unsupported-node policy explicit. For SQL, HTML, LaTeX, or
  similar targets, translation is not permission to evaluate arbitrary R
  side effects.

## Safe metaprogramming

- Prefer allowlisted call heads, symbols, argument shapes, and literal types
  when input can be influenced by a user, file, request, or database. Reject
  unsupported AST nodes before evaluation or translation.
- Never `eval(parse(text = user_input))` as a validation strategy. If code
  text is required, parse it, inspect the complete tree recursively, reject
  side-effecting or unknown constructs, and evaluate only in a deliberately
  constructed environment with the smallest useful parent.
- Avoid `paste()`/`deparse()` round trips for code generation. Use symbols,
  calls, quasiquotation, and exact name handling so backticks, precedence, and
  attributes are not lost.
- Treat `exec()` and `do.call()` as dynamic execution boundaries. Resolve the
  function from a trusted binding or allowlist, validate arguments, and avoid
  forwarding unvalidated names or values into a function with side effects.
- Use namespace-qualified references or explicit environment bindings in
  generated code. Do not rely on whatever packages happen to be attached in
  the caller's session.
- Bound recursive AST walks and generated work when the input is untrusted or
  can be very large. Preserve useful source expressions for diagnostics, but
  do not include secrets or uncontrolled input in error messages.
- Test both code structure and behavior: AST shape, precedence, non-syntactic
  names, missing arguments, nested quosures, mask/environment collisions,
  evaluation timing, unknown functions, escaping idempotence, and rejection
  of unsupported constructs.

## Routing boundaries

- Use `r-core` for vector/list/data-frame/tibble types, recycling, missing
  values, attributes, subsetting, and output shape. This skill only specifies
  how those objects participate in code capture or evaluation.
- Use `r-tidyverse-core` for the shared tidyverse data-masked grammar,
  tidy-data conventions, grouping, and dynamic-column semantics. Use this
  skill for the AST, quosure, mask, and evaluation mechanics behind that API.
- Use `r-functions` for ordinary function contracts, argument matching,
  lazy/default argument behavior outside metaprogramming, control flow,
  recursion as an algorithm, and composition. Use this skill when the
  function must capture or generate code.
- Use `r-environments` for environment identity, parent chains, namespaces,
  closures, persistent state, and binding mutation. Use this skill to choose
  the evaluation context, then route the environment design itself there.
- Use `r-errors` for `rlang` conditions, custom error classes, handlers,
  recovery, cleanup, and backtraces. This skill identifies where malformed
  ASTs, missing names, or unsupported translations should fail.
- Use `r-testing` to turn AST, evaluation-context, mask, translation, and
  rejection invariants into tests.

## Verification checklist

Before shipping metaprogramming code, verify:

- captured developer code and caller-supplied code are distinguished;
- every generated call has the intended function position, arguments, names,
  precedence, and missing-argument structure;
- every later evaluation has an explicit and correct environment or quosure;
- data-mask lookups and external lookups are unambiguous;
- generated output is escaped exactly once and unknown constructs have a
  defined policy;
- parsing, evaluation, dynamic calls, and translation reject inputs outside
  the documented grammar;
- normal results, errors, and side effects are tested at the relevant timing.
