# Tidy data and R types

## Names, values, and mutation

An assignment creates or changes a binding from a name to a value. Multiple
names can refer to the same value, so reason about aliasing before mutating.
For ordinary vectors and lists, a modification normally preserves the other
binding by copying the modified object; list copies are generally shallow, so
their components can remain shared. Environments instead have reference
semantics. R may optimise modifications to a value with one binding, but the
exact decision depends on evaluation and internal references.

Do not infer performance from object diagrams alone. Use `tracemem()` for a
specific copy, `lobstr::ref()` for shared components, and
`lobstr::obj_size()` for sizes that account for sharing. Avoid adding
micro-optimisations before measuring the actual operation.

## Shape first

Before transforming data, identify:

- What one row represents.
- Which columns are identifiers, measurements, and list-columns.
- Whether the input is local or a lazy remote table.
- Whether zero rows are valid and what schema should remain in that case.

Keep one observation per row and one variable per column when the downstream operation is relational or visual. Use `tidyr` when the problem is table shape; do not hide reshaping inside an unrelated helper.

## Size and type checks

Use the narrowest check that expresses the invariant:

```r
stopifnot(is.data.frame(x), nrow(x) >= 0L)
vctrs::vec_assert(id, character())
vctrs::vec_size_common(x, y)
```

For public helpers, prefer an informative `rlang::abort()` over an incidental base-R error. Check that returned vectors have the intended common type and size. Be especially careful with logical, integer, double, and date-time inputs: coercion can be valid R behavior while still violating the application contract.

Atomic vectors have one type for all elements; combining values commonly
coerces them toward character, double, integer, and then logical. A
length-one vector is not a separate scalar type. Lists can contain values of
different types, including other lists, while data frames are named lists
whose columns must agree in row count (including matrix or list columns by
their row extent).

## Missing values

- `is.na(x)` detects missing values; `x == NA` does not.
- `anyNA(x)` is useful for a fast presence check.
- `mean(x, na.rm = TRUE)` changes the denominator and can return `NaN` for all-missing input; decide whether that is acceptable.
- Do not use `coalesce()` or replacement as a generic fix without documenting the domain meaning of the substitute.

## Subsetting invariants

Use `[[` when a single element is required. Use `[` when preserving a vector,
list, or data-frame container matters. Use `$` only for a literal name, never
for a variable containing a column name; it can partially match in base data
frames. In functions accepting user-selected columns, validate selection and
preserve names rather than relying on accidental partial matching.

For matrices, arrays, and data frames, use `drop = FALSE` when the result must
keep its dimensionality. In subassignment, validate replacement size and
index uniqueness when those are part of the contract; use `x[] <- value` to
replace contents without replacing the outer object. Treat `NULL` as absence
or removal in list-like contexts, not as an element-level missing value.

Attributes are metadata, not a guarantee that every operation will preserve
them. Check `class()`, `attributes()`, `dim()`, and names after operations
that must retain a factor, date/time, matrix, or other structured type.

## Further reading

- [Tibble](https://tibble.tidyverse.org/)
- [vctrs size and type stability](https://vctrs.r-lib.org/articles/type-size.html)
- [Tidy data](https://r4ds.hadley.nz/tidy-data.html)
