# readr diagnostics and import contracts

After reading:

- Inspect `spec(df)` or the printed column specification and record it for stable inputs.
- Inspect `problems(df)`; a nonempty result needs a decision, not automatic dismissal.
- Compare parsed row count with the source row count when the source provides one.
- Check sentinel identifiers, missingness rates, date ranges, numeric ranges, and duplicate keys.
- Preserve the original file or source reference so a bad row can be reproduced.

When parsing a batch of files, make the schema explicit and compare each file's names and types before combining. Do not use `bind_rows()` as a schema validator.

If malformed values are acceptable, convert them through a documented quarantine path that includes file, row, column, raw value, and parser problem. If they are not acceptable, fail before analysis.

For compressed, remote, or unusual encodings, verify that the reader's connection and encoding behavior match the source rather than assuming a successful read implies correct text.
