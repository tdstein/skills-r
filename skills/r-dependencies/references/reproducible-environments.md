# Reproducible R environments

## renv

For a project-specific environment:

```r
renv::init()
renv::snapshot()
renv::restore()
renv::status()
```

Commit `renv.lock` when the project uses lockfile-based reproducibility. Review snapshots for unintended packages and repository changes. Use `renv::restore()` in a fresh environment to verify the lockfile rather than assuming a developer library is representative.

Do not use `renv` to hide undeclared package dependencies in an R package. Packages still need correct `DESCRIPTION` and `NAMESPACE` metadata.

## Resolution and sources

Use `pak` or the established project tool to resolve dependencies. For non-CRAN sources, record the source and immutable reference when practical:

- GitHub: repository plus commit/tag.
- R-universe: repository and package.
- Bioconductor: Bioconductor release matching the R version.
- Local package: a documented path or release artifact, not an untracked developer directory.

## CI

CI should restore or install dependencies before tests and check. Pin the R version when reproducibility matters, and make the package repository configuration explicit. Avoid making CI silently update the lockfile.

## Further reading

- [renv](https://rstudio.github.io/renv/)
- [pak](https://pak.r-lib.org/)

