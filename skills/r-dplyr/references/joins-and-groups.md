# dplyr joins and groups

## Joins

Use an equality or inequality specification that describes the relationship:

```r
orders |>
  left_join(customers, by = join_by(customer_id), relationship = "many-to-one")
```

Before the join:

- State which table is primary and whether unmatched rows must be retained.
- Check duplicates in each key with `count()` or an equivalent assertion.
- Decide how missing keys should match.
- Decide whether duplicate matches are valid, an error, or a data-quality issue.

After the join, check row count, unmatched keys, and key uniqueness. A left join preserves rows from the left table but can add rows when a key matches multiple right-hand records.

## Groups and summaries

- `group_by()` adds grouping metadata; it does not aggregate.
- `summarise()` creates one or more rows per group, normally one row per group.
- `reframe()` is appropriate when an expression returns a variable number of rows and returns an ungrouped result.
- Specify `.groups` when the default retention is not part of the intended contract.
- Use `count()` for a quick frequency table, but inspect whether its grouping and name choices fit the downstream contract.

For means, rates, and ratios, define how `NA` and zero denominators are handled. A correct-looking summary with the wrong missingness policy is still wrong.
