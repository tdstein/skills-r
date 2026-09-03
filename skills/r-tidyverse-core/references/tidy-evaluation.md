# Tidy evaluation

Use this reference when a function accepts column expressions rather than ordinary strings.

## Choose the interface

- For a fixed column known by the author, use a regular function call such as `summarise(mean_x = mean(x, na.rm = TRUE))`.
- For a column name supplied as a string, use `.data[[column_name]]` or a verb's string-compatible interface.
- For a user-facing data-masked argument, document that it accepts a column expression and use embracing (`{{ column }}`) when forwarding it.
- For tidy selection, use selectors such as `starts_with()` or `where()` inside selection-aware verbs; do not evaluate selectors in ordinary R code.
- Use `.env$object` when a data column could shadow a function variable.

## Package code

When defining package functions, import or qualify the tidy-evaluation helpers, document data-masked arguments, and avoid unqualified global variables. Test both bare column expressions and string-driven interfaces when both are supported.

Prefer simple interfaces. Do not add tidy evaluation merely to make a one-off script look generic.
