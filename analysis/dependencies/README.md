# Dependency Analysis Runbook (Member 2)

This folder contains reproducible evidence for the **Dependencies** part of `docs/design.md`.

## Locked Baseline

- Source repository: `C:\Users\cekur\Documents\GitHub\logging-log4j2`
- Source branch: `2.x`
- Source commit: `83702bb6194182572eccf6594acf935f83437e76`
- Co-change window: `2025-04-12` to `2026-04-12`
- Scope modules:
  - `log4j-core`
  - `log4j-api`
  - `log4j-layout-template-json`
  - `log4j-slf4j2-impl`
  - `log4j-jdbc-dbcp2`

## Counting Convention

- LOC convention used in this project: **Java SLOC on `src/main/java` only**.
- Scope total from `scope_loc.csv`: **92,131 SLOC**.

## Output Files

- `scope_loc.csv`
  - Columns: `module,sloc_main_java`
- `import_edges.csv`
  - Columns: `source_file,target_import,target_module`
  - One row per unique import statement found in each scoped source file.
- `import_stats.csv`
  - Columns: `file,outgoing_imports,incoming_refs,total`
  - `outgoing_imports`: number of unique imports in the file.
  - `incoming_refs`: number of direct class imports from other scoped files.
  - `total = outgoing_imports + incoming_refs`.
- `cochange_pairs.csv`
  - Columns: `file_a,file_b,cochange_count,window_start,window_end`
  - Pair count based on files changed together in commits of the selected window.
- `inconsistencies.md`
  - High co-change pairs split into:
    - no direct import (potential hidden/coordination dependencies),
    - direct import present (consistent structural dependencies).
- `summary.txt`
  - Snapshot metadata and aggregate counts.

## Reproduction Command

Run from project repo root (`AY-25-26-project`):

```powershell
& "C:\Users\cekur\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe" `
  tools\scripts\generate_dependency_analysis.py `
  --source-repo "C:\Users\cekur\Documents\GitHub\logging-log4j2" `
  --output-dir "C:\Users\cekur\IdeaProjects\AY-25-26-project\analysis\dependencies" `
  --baseline-commit 83702bb6194182572eccf6594acf935f83437e76 `
  --branch 2.x `
  --since-date 2025-04-12 `
  --window-end 2026-04-12
```

## Notes and Limits

- Co-change is measured on commits reachable from the pinned baseline; it captures maintenance-time coupling, not runtime coupling.
- Low co-change frequencies are expected in stable components and in narrow time windows.
- Wildcard imports can be mapped to modules but not always to an exact target file.
