# purrr side effects and parallel mapping

- Use `walk()` when the operation writes files, logs, sends requests, or mutates an external system and the return value is not the data product.
- Make side effects idempotent or record progress before running a large batch.
- Make output paths explicit and unique. Keep the mapping inputs and their corresponding output paths together, then use `walk2()` or `pwalk()` when multiple varying arguments are required.
- Limit retries and distinguish transient failures from invalid inputs.
- `in_parallel()` requires `carrier` (version 0.3.0 or newer) and a function that can be executed in the worker context. Namespace package calls and pass local dependencies explicitly.
- Measure whether parallelism helps; serialization, startup, rate limits, and external-service constraints can dominate.
- Do not use parallel mapping to hide an unbounded or non-reproducible workflow. Set seeds and document ordering when results depend on randomness.
