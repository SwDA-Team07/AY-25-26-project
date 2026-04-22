# Tools

This directory contains tools and scripts used to support the analysis activities.

These may include:

* Scripts for analyzing code dependencies
* Tools for analyzing version control history (co-change)

Current implemented script:

* `scripts/generate_dependency_analysis.py`
  - Generates `import_edges.csv`, `import_stats.csv`, `cochange_pairs.csv`,
    `scope_loc.csv`, `inconsistencies.md`, and `summary.txt` in
    `analysis/dependencies/` from a pinned Log4j2 snapshot.

All tools are used to support the results described in the reports.
