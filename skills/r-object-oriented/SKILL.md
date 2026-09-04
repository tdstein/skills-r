---
name: r-object-oriented
description: "Use for designing, implementing, reviewing, or debugging R object-oriented code with S3, S4, or R6, including representation, constructors, validation, methods, dispatch, inheritance, encapsulation, and system selection."
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

# R object-oriented programming

Use the OO system to make a stable interface polymorphic over well-defined object
contracts. Start by deciding what the object represents, how it is stored, which
operations should be generic, and whether state must be shared or mutable.

## Classify the object before editing it

- Distinguish a base object from an OO object. Every R value has a base type;
  S3 and S4 dispatch additionally depend on class information. Inspect
  `typeof()`, `attributes()`, `class()`, `inherits()`, `is.object()`, and,
  when available, `sloop::otype()`/`sloop::s3_class()`.
- Do not treat `class()` as the complete representation. Dimensions, implicit
  classes, attributes, slots, environments, and the underlying base type can
  all affect behavior. In particular, an unclassed integer or double can have
  implicit S3 classes such as `"numeric"`, while internal generics generally
  dispatch only when an explicit class is present.
- Decide whether the object is vector-like, record-like, data-frame-like, or
  scalar-like. This choice determines what `length()`, subsetting, recycling,
  names, and restoration should mean. A list-backed scalar is not automatically
  a record or a data frame.
- Prefer functions and data transformations over OO when there is no meaningful
  polymorphic interface, invariant, lifecycle, or identity to model.

## Choose the OO system

Default to S3 for small or medium-sized value objects, extensions to existing
R generics, and APIs intended to feel native to R. It is conventional and
extensible, but relies on disciplined contracts rather than enforcement.

Choose S4 when the class structure itself is a major part of the contract:
interrelated classes, formal slot types, multiple inheritance or multiple
dispatch, and systems maintained by many contributors. Pay the design cost
up front, keep dispatch graphs simple, and resolve ambiguity explicitly.

Choose R6 when the object has identity, must be modified in place, owns a
resource, represents an external or long-lived entity, or benefits from
encapsulated methods and method chaining. Treat reference semantics as a
deliberate trade-off: they simplify stateful workflows but make aliasing and
mutation harder to reason about.

Do not choose R6 merely because its syntax resembles another OO language. Do
not choose S4 merely because stricter machinery is available. In all systems,
keep the public interface small and make the representation replaceable.

## S3: informal functional OO

An S3 object is an ordinary base object with a `"class"` attribute. A generic
defines the interface and dispatches to a class-specific function, usually
named `generic.class`. The method is an implementation detail; callers should
call the generic, not the method directly.

### Build an S3 class as a contract

For a public class, separate construction from user ergonomics and expensive
validation:

- `new_myclass()` is a low-level constructor. Check the base type and the
  types of structural attributes, and keep it cheap enough for internal use.
- `validate_myclass()` checks value-level and cross-field invariants. Return
  the object on success when validation is composed into a pipeline; otherwise
  raise a clear condition.
- `myclass()` is the user-facing helper. Coerce friendly inputs, choose useful
  defaults, produce end-user diagnostics, then call the constructor and
  validator.

Use `structure()` or `class<-()` only when the resulting representation and
invariants are already known. S3 will let callers assign an unrelated class to
any object, so constructors and validators are the safety boundary.

Choose class names that are package-qualified when collision is plausible and
avoid `"."` in class names, since it is also the method-name separator.

### Write generics and methods carefully

- A new generic is usually a thin `UseMethod()` wrapper. Avoid computation,
  side effects, or argument rewriting in the generic; dispatch semantics are
  subtle and the generic defines the shared argument interface.
- Methods should accept the generic's arguments. A method may add arguments
  only where the generic deliberately exposes `...`; remember that `...` can
  hide misspellings.
- Add a method only when you own the generic or the class, or have coordinated
  with its maintainer. Otherwise create a separate generic or an adapter.
- Use `sloop::ftype()`, `sloop::s3_dispatch()`,
  `sloop::s3_methods_generic()`, `sloop::s3_methods_class()`, and
  `sloop::s3_get_method()` to inspect unfamiliar code.

Dispatch tries the explicit class vector in order, then `"default"`. For
unclassed objects, inspect the implicit class rather than assuming
`class(x)` tells the whole story. Internal generics such as `[`, `sum()`, and
`cbind()` have special dispatch rules; group generics (`Math`, `Ops`,
`Summary`, `Complex`) and `Ops` double dispatch add further paths. Use
`s3_dispatch()` before guessing.

### Inheritance and restoration

Represent S3 inheritance with a character class vector, most-specific first.
For a normal subclass, keep the same base type and retain the superclass's
attributes, adding only subclass state. A method can delegate to the next
candidate with `NextMethod()`.

If a class is intended to be subclassable:

- Let the constructor accept `...` and an incoming `class`, and prepend the
  subclass before the parent class.
- Avoid reconstructing results with a fixed parent constructor inside methods;
  that erases subclasses.
- Restore the class and attributes after operations such as subsetting,
  arithmetic, and concatenation. Prefer `vctrs::vec_restore()` and the
  corresponding vctrs framework for robust subclass preservation and
  arithmetic; write base methods only when the class has genuinely custom
  behavior.

## S4: formal functional OO

Use `methods::setClass()` to declare named slots and their classes. Supply a
prototype with representative typed defaults, use `contains` for inheritance,
and construct through `new()` or a user-facing helper named after the class.
Class definitions register mutable global metadata, so avoid redefining a class
after instances have been created.

- Put slot-type checks in the class definition and value/cross-slot checks in
  `setValidity()`. Use `validObject()` after mutations through accessors.
- Treat slots as implementation details. Expose getter and setter accessors,
  usually S4 generics, so representation can evolve without breaking callers.
- Define a generic with `setGeneric()` and a body that calls
  `standardGeneric()`. Use `signature` to limit which arguments participate in
  dispatch; do not dispatch on incidental control arguments.
- Define methods with `setMethod()` and match the generic's argument names.
  Implement `show()` for user-facing printing when appropriate.
- Use `is()`, `methods()`, `selectMethod()`, and the methods documentation to
  inspect class relationships and selected implementations.

S4 supports multiple inheritance and multiple dispatch, but their combination
can make the method graph ambiguous and difficult to maintain. Prefer single
inheritance and single dispatch unless the domain requires more. Define
terminal methods, provide deliberate `ANY` fallbacks, and resolve equal-distance
matches with a more specific method rather than relying on warning-time tie
breaking. `MISSING` is useful only for APIs whose behavior depends on an
argument being omitted.

When integrating S3 and S4, register S3 classes with `setOldClass()` before
using them in S4 definitions. Treat S3/S4 interoperation as a boundary with
special dispatch rules; inspect `?Methods_for_S3` and test both directions.

## R6: encapsulated reference OO

Define a class with `R6::R6Class()`, normally using `UpperCamelCase` for the
class and `snake_case` for public fields and methods. Use:

- `public` for the supported external interface;
- `private` for implementation state and helpers, accessed with `private$`;
- `active` for field-like accessors backed by functions, especially
  read-only or validated views;
- `initialize()` for per-instance construction and cheap invariant checks;
- `print()` for concise display, returning `invisible(self)` when it is
  primarily a side-effect;
- `super$` when an overriding method delegates to its parent.

Side-effect methods should normally return `invisible(self)` to support method
chaining. Methods that primarily compute should return their result instead.
Keep the distinction clear so a call does not unexpectedly both mutate and
return a value unless that is an intentional stateful API.

R6 instances are references. Assignment creates another name for the same
object; use `$clone()` for an independent copy and `$clone(deep = TRUE)` when
nested R6 objects must also be copied. Document ownership and aliasing at
boundaries where an object is stored or passed to another component.

Create mutable child fields in `initialize()`, not as class-definition defaults:
an R6 object placed in the class field list is otherwise shared by every
instance. Use `finalize()` only for cleanup of private resources acquired by
that instance (connections, temporary files, and similar). Finalizers can run
at garbage collection or process exit, so they must not mutate shared
application state or be relied on for ordinary control flow.

When debugging interactive R6 work, reconstruct instances after changing the
class definition; existing instances retain the methods and fields with which
they were created. Inspect `class()` and `names()` for the public surface, and
leave implementation details such as `.__enclos_env__` alone.

## Method-dispatch and representation workflow

When behavior is surprising, work from the object outward:

1. Inspect `typeof()`, class information, attributes or slots, and whether the
   object is mutable or shared.
2. Identify the generic or method call actually being made. For S3 use
   `s3_dispatch()`; for S4 inspect `methods()`/`selectMethod()`; for R6 inspect
   the instance's class and method names.
3. Enumerate the inheritance path and fallback path, including implicit
   classes, `NextMethod()`/`super$`, `ANY`, group generics, and multiple
   dispatch where relevant.
4. Check the method's input/output contract: base type, size, attributes,
   slots, class restoration, visibility, and mutation.
5. Reproduce the smallest failing case and test both ordinary and boundary
   inputs before changing the design.

Keep constructors, validators, accessors, and methods aligned: every operation
that can change representation must either preserve the invariant or return a
deliberately different class.

## Boundaries with other R skills

- Use `r-core` for vector/list/data-frame semantics, type coercion, sizes,
  recycling, missingness, and general attribute behavior; this skill applies
  those foundations to OO contracts.
- Use `r-functions` for closures, argument evaluation, factories, operators,
  and general function API design. This skill covers the OO-specific role of a
  generic, method, constructor, or encapsulated method.
- Use `r-errors` for condition classes, error/warning/message design, and
  recovery. Here, focus on where validation belongs and which invariant failed.
- Use `r-testing` for test organization, fixtures, mocking, snapshots, and
  coverage. Here, identify dispatch, subclass, aliasing, validity, and
  restoration cases that need tests.
- Use `r-documentation` for package documentation and user-facing API prose.
  Here, identify the public class contract, accessors, inheritance promises,
  mutability, and lifecycle behavior that documentation must state.

## Verification checklist

Before handing off OO code, verify:

- the chosen system matches the object's identity, lifecycle, and extension
  needs;
- constructors/helpers produce the documented base type and attributes/slots;
- validators reject malformed values and setters cannot bypass validity;
- generic and method signatures agree;
- dispatch and inheritance work for the intended classes and fallbacks;
- subsetting and transformations preserve or intentionally change class state;
- R6 aliasing, cloning, child-object initialization, and cleanup are tested;
- public access goes through stable interfaces rather than raw slots/private
  fields;
- tests cover empty, scalar, subclassed, invalid, and mixed-class cases where
  those cases are part of the contract.
