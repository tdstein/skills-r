# CLAUDE.md

## Project overview

`cc-skills-r` is a cross-client Agent Skills plugin for R development, with
Tidyverse guidance as its initial focus. Skills are Markdown instructions that
can be used by Claude Code, Cursor, Gemini CLI, Codex, and similar agents.

## Project structure

```text
skills/<skill-name>/
  SKILL.md           # Required instructions and frontmatter
  references/        # Optional details loaded on demand
  scripts/           # Optional deterministic helpers
  assets/            # Optional reusable resources
  evals/             # Optional evaluation fixtures
.claude-plugin/      # Claude Code manifest
.cursor-plugin/      # Cursor manifest
gemini-extension.json # Gemini CLI manifest
```

## Skill authoring

Every skill must live in `skills/<name>/SKILL.md`. Keep the directory name and
frontmatter `name` identical, lowercase, hyphenated, and no longer than 64
characters.

Use concise YAML frontmatter compatible with the Agent Skills specification:

```yaml
---
name: r-example
description: "What the skill covers and when to apply it."
license: MIT
compatibility: "R 4.1+ and current releases of the documented packages; compatible with Claude Code, Cursor, Gemini CLI, Codex, and similar agents."
metadata:
  author: tdstein
  version: "0.1.0"
user-invocable: true
allowed-tools: Read Edit Write Glob Grep Bash(R:*) Bash(Rscript:*) Bash(git:*) Agent
---
```

Descriptions are the primary trigger. Name the relevant R packages, APIs, and
user tasks, and state boundaries with sibling skills. Keep descriptions below
1,000 characters and keep `SKILL.md` focused; move detailed material to
one-level-deep files in `references/`.

Tidyverse skills should preserve clear ownership:

- `dplyr` owns table transformations, grouping, summaries, and joins.
- `tidyr` owns table shape, pivoting, nesting, and unnesting.
- `purrr` owns functional iteration and list-column workflows.
- `ggplot2` owns visualization.
- `readr` owns rectangular-file parsing.
- Shared tidy-data, tibble, pipe, and type guidance belongs in a core skill.

Do not force database, modeling, Shiny, package-development, or general R
engineering concerns into Tidyverse skills. Cross-reference the appropriate
specialized skill instead.

## Compatibility and versioning

Keep plugin manifest versions synchronized across
`.claude-plugin/plugin.json`, `.cursor-plugin/plugin.json`, and
`gemini-extension.json`. The current repository version is `0.1.0`.

Use MIT licensing and avoid client-specific features unless they have a clear
cross-client fallback. When a client-specific metadata file is needed, keep it
optional and separate from the canonical `SKILL.md`.

## Verification

Before submitting a skill change:

- Validate YAML frontmatter and referenced files.
- Check directory/name and manifest-version consistency.
- Run Markdown linting and relevant R examples.
- Add or update adversarial evaluation fixtures for behavior that is easy to
  get subtly wrong.
