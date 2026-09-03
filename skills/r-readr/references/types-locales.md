# readr types and locales

## Column specifications

- Use `cols()` with `col_character()`, `col_integer()`, `col_double()`, `col_number()`, `col_date()`, `col_datetime()`, and `col_logical()` as appropriate.
- Use `col_guess()` only when exploration or a deliberately heuristic pipeline is acceptable.
- `col_number()` handles grouping marks and currency-like decoration according to the locale; `col_double()` is stricter about the expected representation.
- Keep identifiers such as ZIP codes, account numbers, and codes as character even when they contain only digits.
- Use `col_skip()` for intentionally excluded columns and document why they are not part of the contract.

## Locales

Pass `locale(decimal_mark = ",", grouping_mark = ".")` or a suitable date/time configuration when the source requires it. Do not rely on the machine's system locale for a shared pipeline.

For dates, prefer an explicit `col_date(format = "%d/%m/%Y")` or a parse function with a documented format when the source is fixed. For heterogeneous human input, use `parse_date()` with an explicit locale and inspect failures.

## Parsing functions

Use `parse_number()` for human-formatted numbers, `parse_double()` for strict decimal values, and the matching `parse_*()` function for dates, times, and logicals. Choose the parser from the source contract, not from whichever function succeeds on one sample.
