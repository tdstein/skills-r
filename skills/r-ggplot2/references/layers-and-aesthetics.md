# ggplot2 layers and aesthetics

## Mapping versus setting

```r
ggplot(df, aes(x, y, colour = group)) +
  geom_point() +
  geom_smooth(method = "lm", se = FALSE)
```

Use `aes()` for data-driven mappings. Put constants in the geom:

```r
geom_point(colour = "steelblue", alpha = 0.7)
```

A layer can inherit the global mapping or override it with `inherit.aes = FALSE`. Use that for annotations or reference data that does not share the main data columns.

Treat `+` as order-sensitive plot construction: later layers are drawn over
earlier layers, so regrouping or reordering layers can change the result.

## Stats

- A geom is a visual mark; a stat transforms data for that mark. They are paired defaults, not interchangeable concepts.
- Use `after_stat()` for variables created by the stat, such as density or bin counts.
- Set `binwidth`, `bins`, or a meaningful grouping when a histogram or smoother's result depends on it.
- Avoid comparing distributions with incompatible binning or smoothing choices.

Use `ggplot_build()` or a small reproducible data set to inspect computed data when a plot is surprising.
