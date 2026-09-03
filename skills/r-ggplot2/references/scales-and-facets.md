# ggplot2 scales, facets, and coordinates

- Select scales based on the variable type and message: continuous, discrete, date/time, binned, transformed, or identity.
- Use `scale_*_manual()` only when category-to-value mappings are stable and documented.
- Label units and transformations in axis labels; do not make readers infer percentages, rates, or log bases.
- Use `coord_cartesian()` for visual zooming when outliers must remain in statistical calculations.
- Use scale limits when excluding values is an intentional data decision and document the exclusion.
- Use facets when panels share a meaningful comparison and keep scales fixed unless free scales improve legibility without obscuring magnitude differences.
- Use `theme()` for visual hierarchy and accessibility. Check color palettes in grayscale or with a color-vision deficiency simulator when color carries meaning.
- Prefer direct labels or clear legends over encoding too many groups with color, shape, and linetype simultaneously.
