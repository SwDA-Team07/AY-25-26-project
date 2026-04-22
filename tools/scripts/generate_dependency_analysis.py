#!/usr/bin/env python3
"""Generate import dependencies and co-change analysis for SDA Design report.

This script is intentionally deterministic to support reproducibility claims.
It analyzes only Java production files (`src/main/java`) for selected modules.
"""

from __future__ import annotations

import argparse
import csv
import itertools
import re
import subprocess
from collections import Counter, defaultdict
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Iterable


PACKAGE_RE = re.compile(r"^\s*package\s+([A-Za-z_]\w*(?:\.[A-Za-z_]\w*)*)\s*;\s*$")
IMPORT_RE = re.compile(
    r"^\s*import\s+(?:static\s+)?([A-Za-z_]\w*(?:\.[A-Za-z_]\w*)*(?:\.\*)?)\s*;\s*$"
)


@dataclass(frozen=True)
class SourceFile:
    module: str
    rel_path: str
    abs_path: Path
    package_name: str
    class_name: str

    @property
    def fqcn(self) -> str:
        return f"{self.package_name}.{self.class_name}" if self.package_name else self.class_name


def run_git(repo: Path, args: list[str]) -> str:
    proc = subprocess.run(
        ["git", "-C", str(repo), *args],
        check=True,
        text=True,
        encoding="utf-8",
        capture_output=True,
    )
    return proc.stdout


def validate_snapshot(repo: Path, baseline_commit: str, expected_branch: str) -> tuple[str, str]:
    head = run_git(repo, ["rev-parse", "HEAD"]).strip()
    branch = run_git(repo, ["branch", "--show-current"]).strip()
    if head != baseline_commit:
        raise RuntimeError(
            f"Repository HEAD {head} does not match required baseline {baseline_commit}."
        )
    if branch != expected_branch:
        raise RuntimeError(
            f"Repository branch '{branch}' does not match required branch '{expected_branch}'."
        )
    return head, branch


def parse_java_file(path: Path) -> tuple[str, list[str]]:
    package_name = ""
    imports: list[str] = []
    with path.open("r", encoding="utf-8", errors="ignore") as handle:
        for line in handle:
            pkg_match = PACKAGE_RE.match(line)
            if pkg_match:
                package_name = pkg_match.group(1)
                continue
            imp_match = IMPORT_RE.match(line)
            if imp_match:
                imports.append(imp_match.group(1))
    return package_name, imports


def collect_source_files(repo: Path, modules: list[str]) -> tuple[dict[str, SourceFile], dict[str, set[str]], dict[str, set[str]], dict[str, list[str]]]:
    by_path: dict[str, SourceFile] = {}
    fqcn_to_path: dict[str, str] = {}
    package_to_modules: dict[str, set[str]] = defaultdict(set)
    imports_by_file: dict[str, list[str]] = {}

    for module in modules:
        src_root = repo / module / "src" / "main" / "java"
        if not src_root.exists():
            continue
        for java_file in src_root.rglob("*.java"):
            rel_path = java_file.relative_to(repo).as_posix()
            class_name = java_file.stem
            package_name, imports = parse_java_file(java_file)
            if class_name == "package-info":
                continue

            source = SourceFile(
                module=module,
                rel_path=rel_path,
                abs_path=java_file,
                package_name=package_name,
                class_name=class_name,
            )
            by_path[rel_path] = source
            imports_by_file[rel_path] = imports
            package_to_modules[package_name].add(module)
            fqcn_to_path[source.fqcn] = rel_path

    return by_path, package_to_modules, fqcn_to_path, imports_by_file


def resolve_import_target_module(
    target_import: str,
    package_to_modules: dict[str, set[str]],
    fqcn_to_path: dict[str, str],
    files_by_path: dict[str, SourceFile],
) -> tuple[str, str | None]:
    # Exact class import
    if not target_import.endswith(".*"):
        target_file = fqcn_to_path.get(target_import)
        if target_file is not None:
            return files_by_path[target_file].module, target_file
        package_name = target_import.rpartition(".")[0]
        modules = package_to_modules.get(package_name)
        if not modules:
            return "external", None
        if len(modules) == 1:
            return next(iter(modules)), None
        return "multiple", None

    # Wildcard package import
    package_name = target_import[:-2]
    modules = package_to_modules.get(package_name)
    if not modules:
        return "external", None
    if len(modules) == 1:
        return next(iter(modules)), None
    return "multiple", None


def build_import_outputs(
    files_by_path: dict[str, SourceFile],
    package_to_modules: dict[str, set[str]],
    fqcn_to_path: dict[str, str],
    imports_by_file: dict[str, list[str]],
) -> tuple[list[dict[str, str]], list[dict[str, str]], dict[str, set[str]]]:
    import_edges: list[dict[str, str]] = []
    outgoing_counter: Counter[str] = Counter()
    incoming_counter: Counter[str] = Counter()
    direct_edges: dict[str, set[str]] = defaultdict(set)

    for source_file, imports in imports_by_file.items():
        unique_imports = sorted(set(imports))
        outgoing_counter[source_file] = len(unique_imports)
        for target_import in unique_imports:
            target_module, target_file = resolve_import_target_module(
                target_import, package_to_modules, fqcn_to_path, files_by_path
            )
            import_edges.append(
                {
                    "source_file": source_file,
                    "target_import": target_import,
                    "target_module": target_module,
                }
            )
            if target_file is not None:
                incoming_counter[target_file] += 1
                direct_edges[source_file].add(target_file)

    import_stats: list[dict[str, str]] = []
    for rel_path in sorted(files_by_path):
        outgoing = outgoing_counter[rel_path]
        incoming = incoming_counter[rel_path]
        import_stats.append(
            {
                "file": rel_path,
                "outgoing_imports": str(outgoing),
                "incoming_refs": str(incoming),
                "total": str(outgoing + incoming),
            }
        )

    import_edges.sort(key=lambda row: (row["source_file"], row["target_import"]))
    return import_edges, import_stats, direct_edges


def collect_cochange_file_sets(
    repo: Path, baseline_commit: str, since_date: str, modules: list[str], scoped_files: set[str]
) -> tuple[list[set[str]], int]:
    pathspecs = [f"{module}/src/main/java" for module in modules]
    commit_out = run_git(
        repo,
        [
            "rev-list",
            baseline_commit,
            f"--since={since_date}",
            "--",
            *pathspecs,
        ],
    )
    commits = [line.strip() for line in commit_out.splitlines() if line.strip()]
    file_sets: list[set[str]] = []
    for commit in commits:
        changed = run_git(
            repo,
            ["show", "--name-only", "--pretty=format:", commit, "--", *pathspecs],
        )
        files = {
            line.strip().replace("\\", "/")
            for line in changed.splitlines()
            if line.strip().endswith(".java")
        }
        scoped_changed = files & scoped_files
        if len(scoped_changed) >= 2:
            file_sets.append(scoped_changed)
    return file_sets, len(commits)


def build_cochange_pairs(
    repo: Path, baseline_commit: str, since_date: str, modules: list[str], scoped_files: set[str]
) -> tuple[list[dict[str, str]], int, int]:
    pair_counter: Counter[tuple[str, str]] = Counter()
    file_sets, commit_count = collect_cochange_file_sets(
        repo, baseline_commit, since_date, modules, scoped_files
    )
    for changed_files in file_sets:
        for file_a, file_b in itertools.combinations(sorted(changed_files), 2):
            pair_counter[(file_a, file_b)] += 1

    rows: list[dict[str, str]] = []
    for (file_a, file_b), count in pair_counter.most_common():
        rows.append(
            {
                "file_a": file_a,
                "file_b": file_b,
                "cochange_count": str(count),
                "window_start": since_date,
                "window_end": "2026-04-12",
            }
        )
    return rows, commit_count, len(file_sets)


def explain_inconsistency(file_a: str, file_b: str) -> str:
    dir_a = file_a.rpartition("/")[0]
    dir_b = file_b.rpartition("/")[0]
    if dir_a == dir_b:
        return "Same package changed together; coordination dependency likely driven by shared behavior or refactors."
    if "/config/" in file_a and "/config/" in file_b:
        return "Both files belong to configuration flow; co-change may reflect configuration evolution rather than direct type coupling."
    if "/appender/" in file_a or "/appender/" in file_b:
        return "Appender-related files often co-evolve with policy/layout changes even without direct imports."
    return "Potential hidden coupling or cross-cutting change pattern not visible through direct import dependencies."


def write_csv(path: Path, fieldnames: list[str], rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def write_inconsistencies(
    output_path: Path,
    cochange_rows: list[dict[str, str]],
    direct_edges: dict[str, set[str]],
) -> None:
    def has_direct_dependency(file_a: str, file_b: str) -> bool:
        return file_b in direct_edges.get(file_a, set()) or file_a in direct_edges.get(file_b, set())

    high_no_direct = [
        row
        for row in cochange_rows
        if not has_direct_dependency(row["file_a"], row["file_b"])
    ][:20]
    high_direct = [
        row
        for row in cochange_rows
        if has_direct_dependency(row["file_a"], row["file_b"])
    ][:10]

    lines: list[str] = []
    lines.append("# Inconsistencies Between Code and Knowledge Dependencies")
    lines.append("")
    lines.append("This file compares import-based dependency signals with co-change signals.")
    lines.append("")
    lines.append("## High Co-change Pairs Without Direct Import")
    lines.append("")
    lines.append("| pair | code_dependency_signal | cochange_signal | interpretation |")
    lines.append("|---|---|---:|---|")
    for row in high_no_direct:
        pair = f"`{row['file_a']}` <-> `{row['file_b']}`"
        lines.append(
            f"| {pair} | no direct import | {row['cochange_count']} | {explain_inconsistency(row['file_a'], row['file_b'])} |"
        )
    if not high_no_direct:
        lines.append("| - | - | - | No high co-change / no-direct-import pairs found in the selected window. |")

    lines.append("")
    lines.append("## High Co-change Pairs With Direct Import")
    lines.append("")
    lines.append("| pair | code_dependency_signal | cochange_signal | interpretation |")
    lines.append("|---|---|---:|---|")
    for row in high_direct:
        pair = f"`{row['file_a']}` <-> `{row['file_b']}`"
        lines.append(
            f"| {pair} | direct import present | {row['cochange_count']} | Co-change aligns with explicit structural dependency. |"
        )
    if not high_direct:
        lines.append("| - | - | - | No high co-change direct-import pairs found in the selected window. |")

    lines.append("")
    output_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def count_java_sloc(path: Path) -> int:
    count = 0
    in_block = False
    with path.open("r", encoding="utf-8", errors="ignore") as handle:
        for raw_line in handle:
            line = raw_line.rstrip("\n")
            idx = 0
            out_chars: list[str] = []
            while idx < len(line):
                if in_block:
                    end = line.find("*/", idx)
                    if end == -1:
                        idx = len(line)
                        break
                    in_block = False
                    idx = end + 2
                else:
                    if line.startswith("//", idx):
                        break
                    if line.startswith("/*", idx):
                        in_block = True
                        idx += 2
                        continue
                    out_chars.append(line[idx])
                    idx += 1
            if "".join(out_chars).strip():
                count += 1
    return count


def build_scope_loc_rows(repo: Path, modules: list[str]) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    total = 0
    for module in modules:
        src_root = repo / module / "src" / "main" / "java"
        module_total = 0
        if src_root.exists():
            for java_file in src_root.rglob("*.java"):
                module_total += count_java_sloc(java_file)
        total += module_total
        rows.append({"module": module, "sloc_main_java": str(module_total)})
    rows.append({"module": "TOTAL", "sloc_main_java": str(total)})
    return rows


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-repo", required=True, help="Path to logging-log4j2 repository")
    parser.add_argument("--output-dir", required=True, help="Path to analysis/dependencies output directory")
    parser.add_argument(
        "--baseline-commit",
        default="83702bb6194182572eccf6594acf935f83437e76",
        help="Pinned source commit hash",
    )
    parser.add_argument(
        "--branch",
        default="2.x",
        help="Expected source branch name",
    )
    parser.add_argument(
        "--since-date",
        default="2025-04-12",
        help="Co-change window start date (YYYY-MM-DD)",
    )
    parser.add_argument(
        "--window-end",
        default="2026-04-12",
        help="Co-change window end date for metadata (YYYY-MM-DD)",
    )
    parser.add_argument(
        "--modules",
        nargs="+",
        default=[
            "log4j-core",
            "log4j-api",
            "log4j-layout-template-json",
            "log4j-slf4j2-impl",
            "log4j-jdbc-dbcp2",
        ],
        help="Modules to include in analysis",
    )
    args = parser.parse_args()

    repo = Path(args.source_repo).resolve()
    output_dir = Path(args.output_dir).resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    baseline_head, baseline_branch = validate_snapshot(repo, args.baseline_commit, args.branch)

    files_by_path, package_to_modules, fqcn_to_path, imports_by_file = collect_source_files(repo, args.modules)
    import_edges, import_stats, direct_edges = build_import_outputs(
        files_by_path, package_to_modules, fqcn_to_path, imports_by_file
    )
    cochange_rows, cochange_commit_count, cochange_pair_commit_count = build_cochange_pairs(
        repo=repo,
        baseline_commit=args.baseline_commit,
        since_date=args.since_date,
        modules=args.modules,
        scoped_files=set(files_by_path.keys()),
    )
    for row in cochange_rows:
        row["window_end"] = args.window_end

    scope_loc_rows = build_scope_loc_rows(repo, args.modules)

    write_csv(
        output_dir / "import_edges.csv",
        ["source_file", "target_import", "target_module"],
        import_edges,
    )
    write_csv(
        output_dir / "import_stats.csv",
        ["file", "outgoing_imports", "incoming_refs", "total"],
        import_stats,
    )
    write_csv(
        output_dir / "cochange_pairs.csv",
        ["file_a", "file_b", "cochange_count", "window_start", "window_end"],
        cochange_rows,
    )
    write_csv(
        output_dir / "scope_loc.csv",
        ["module", "sloc_main_java"],
        scope_loc_rows,
    )
    write_inconsistencies(output_dir / "inconsistencies.md", cochange_rows, direct_edges)

    summary_lines = [
        f"baseline_commit={baseline_head}",
        f"branch={baseline_branch}",
        f"modules={','.join(args.modules)}",
        f"java_main_files={len(files_by_path)}",
        f"import_edges={len(import_edges)}",
        f"cochange_pairs={len(cochange_rows)}",
        f"cochange_commits_scanned={cochange_commit_count}",
        f"cochange_commits_with_pairs={cochange_pair_commit_count}",
        f"window_start={args.since_date}",
        f"window_end={args.window_end}",
        f"generated_on={date.today().isoformat()}",
    ]
    (output_dir / "summary.txt").write_text("\n".join(summary_lines) + "\n", encoding="utf-8")

    print("Generated:")
    print(f"  {output_dir / 'import_edges.csv'}")
    print(f"  {output_dir / 'import_stats.csv'}")
    print(f"  {output_dir / 'cochange_pairs.csv'}")
    print(f"  {output_dir / 'scope_loc.csv'}")
    print(f"  {output_dir / 'inconsistencies.md'}")
    print(f"  {output_dir / 'summary.txt'}")


if __name__ == "__main__":
    main()
