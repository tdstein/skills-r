# tidyr list-columns and rectangling

- Use `nest()` when each row should own a data frame of related observations.
- Use `unnest()` when a data-frame column should be expanded back into rows and columns.
- Use `unnest_longer()` for a list-column where each element is a vector and each element should become rows.
- Use `unnest_wider()` when each element is a named vector or record whose components should become columns.
- Use `hoist()` to extract selected components from deeply nested data without fully expanding it.
- Inspect element lengths, names, and classes before unnesting. Decide what to do with empty and `NULL` elements.
- Preserve identifiers across expansion and test whether expansion is one-to-many; row multiplication is expected but must be intentional.
- For parsing JSON-like records, distinguish a missing component from a present component with `NULL` or `NA`.
