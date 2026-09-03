#!/usr/bin/env Rscript

args <- commandArgs(trailingOnly = TRUE)
root <- if (length(args) > 0) args[[1]] else "."

markdown_files <- list.files(
  root,
  pattern = "[.]md$",
  recursive = TRUE,
  full.names = TRUE
)
markdown_files <- markdown_files[
  !grepl("[/\\\\][.]git([/\\\\]|$)", normalizePath(markdown_files, mustWork = FALSE))
]

failures <- character()
snippet_count <- 0L

for (path in markdown_files) {
  lines <- readLines(path, warn = FALSE)
  in_r_block <- FALSE
  block <- character()
  start_line <- 0L

  for (line_number in seq_along(lines)) {
    if (!in_r_block && grepl("^```[rR][[:space:]]*$", lines[[line_number]])) {
      in_r_block <- TRUE
      block <- character()
      start_line <- line_number
      next
    }

    if (in_r_block && grepl("^```[[:space:]]*$", lines[[line_number]])) {
      snippet_count <- snippet_count + 1L
      result <- tryCatch(
        {
          parse(text = block, keep.source = FALSE)
          NULL
        },
        error = function(error) conditionMessage(error)
      )
      if (!is.null(result)) {
        failures <- c(
          failures,
          sprintf("%s:%d: %s", path, start_line, result)
        )
      }
      in_r_block <- FALSE
      block <- character()
      next
    }

    if (in_r_block) {
      block <- c(block, lines[[line_number]])
    }
  }

  if (in_r_block) {
    failures <- c(
      failures,
      sprintf("%s:%d: unterminated R fenced code block", path, start_line)
    )
  }
}

if (length(failures) > 0L) {
  cat(paste(failures, collapse = "\n"), "\n", sep = "")
  quit(status = 1L)
}

cat(sprintf("Parsed %d R fenced code block(s).\n", snippet_count))
