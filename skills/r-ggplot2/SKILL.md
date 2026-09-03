---
name: r-ggplot2
description: "Use for ggplot2 plots, aesthetics, geoms, stats, scales, facets, themes, and coordinates; prepare substantial data with dplyr or tidyr."
license: MIT
compatibility: "R 4.1+ and the documented packages; compatible with Claude Code, Cursor, Gemini CLI, Codex, and similar Agent Skills clients."
user-invocable: true
allowed-tools: "Read Grep Glob Bash(R:*) Bash(Rscript:*)"
metadata:
  author: "tdstein"
  version: "0.1.0"
  openclaw:
    emoji: "📈"
    homepage: "https://github.com/tdstein/cc-skills-r"
    requires:
      bins:
        - R
        - Rscript
    install: []
---

# ggplot2 visualization

Treat a plot as a mapping from data to visual encodings built from layers. Make the intended message, variables, statistical transformation, scales, and audience visible in the code.

## Workflow

1. Prepare and validate the data with `r-dplyr`/`r-tidyr` when needed.
2. Map variables inside `aes()`; set constants outside `aes()`.
3. Choose a geom whose statistical assumptions match the question. Use `stat =` or `after_stat()` deliberately when mapping computed variables.
4. Add scales, labels, facets, and coordinates to support interpretation rather than decoration.
5. Check discrete/continuous scale types, missing values, transformed axes, and overplotting.
6. Use `theme()` for local adjustments and a reusable theme function for project-wide consistency.
7. Test the plot with representative data, including empty groups and unusual labels.

## Non-obvious rules

- `aes(colour = "blue")` maps every observation to a discrete value named `"blue"`; `colour = "blue"` sets the constant blue. This distinction applies to all aesthetics.
- A `stat` may compute variables that are not present in the input. Use `after_stat()` when mapping those computed values and explain the denominator or binning.
- `coord_cartesian()` zooms the view without removing data; scale limits can remove data before statistical computation.
- Use `facet_wrap()` for one faceting variable and `facet_grid()` when row/column structure is meaningful. Do not facet merely to avoid deciding which comparison matters.
- Use an explicit scale for semantic mappings such as color categories, dates, percentages, and log axes.
- Do not use 3D, dual axes, or decorative encodings to compensate for an unclear data structure.

Read [references/layers-and-aesthetics.md](references/layers-and-aesthetics.md) for mapping, geoms, stats, and layer inheritance. Read [references/scales-and-facets.md](references/scales-and-facets.md) for scales, coordinates, facets, and communication choices.
