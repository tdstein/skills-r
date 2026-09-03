---
name: r-connections
description: "Use for R connection-based I/O with files, URLs, pipes, sockets, text, binary data, and encodings; keep project layout and tabular parsing separate."
license: MIT
compatibility: "R 4.1+ and the documented packages; compatible with Claude Code, Cursor, Gemini CLI, Codex, and similar Agent Skills clients."
user-invocable: true
allowed-tools: "Read Edit Write Glob Grep Bash(R:*) Bash(Rscript:*) Bash(git:*) Agent"
metadata:
  author: tdstein
  version: "0.1.0"
  openclaw:
    emoji: "🔌"
    homepage: "https://github.com/tdstein/cc-skills-r"
    requires:
      bins:
        - R
        - Rscript
    install: []
---

# R connections

Use connections as the I/O boundary between R code and an external stream.
Choose the connection for the transport, then keep opening, reading or
writing, parsing, and cleanup explicit.

## Choose the transport

- Use files for local persistent data, compressed-file connections for compressed
  streams, URLs or `curl` for HTTP resources, pipes for subprocess streams, and
  sockets for network endpoints.
- Use `stdin`, `stdout`, and `stderr` deliberately when a command-line or
  interactive interface owns the default connections.
- Check whether an operation is blocking or non-blocking before putting it in a
  long-running or interactive workflow.

## Manage lifecycle

If your code opens a connection, arrange for it to close on every exit path,
typically with `on.exit(close(con), add = TRUE)`. Do not close a connection
owned by the caller. Keep the connection lifetime no longer than the operation
that needs it, and make failures identify whether opening, transport, or
encoding caused the problem.

## Keep text and binary distinct

Use `raw()` with `readBin()` and `writeBin()` for binary protocols or files.
Do not route arbitrary binary data through text functions: newlines, null bytes,
and character conversion can change the payload.

For text, make the encoding boundary explicit. Prefer UTF-8 for new artifacts,
distinguish the connection's `encoding` from a file's `fileEncoding`, and use
`iconv()` when conversion is required. Test non-ASCII text rather than assuming
ASCII behavior.

## Keep responsibilities separate

A connection transports bytes or characters; it does not define the project's
path layout or the schema of a delimited table. Use `r-project-layout` for
paths and artifact ownership, `r-readr` for tabular parsing, and
`r-dependencies` for packages used to implement the transport. Validate and
sanitize external inputs at the boundary, and keep network or subprocess
behavior out of examples and tests unless it is explicitly controlled.
