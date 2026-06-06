# Final Review - Design

Date prepared: 2026-06-06  
Reviewer: Filippo (`s348651`)  
Scope: [`docs/design.md`](../../docs/design.md)

## Review Goal

Record the final design-report findings collected during the last review pass.

## Findings

- [ ] Problem: The Design report is not yet smooth enough to read.
  Why it is a problem: Some sections are understandable, but the reading flow is still heavy and can make the design rationale harder to follow.
  Suggested fix: Rewrite the Design report with clearer transitions, shorter paragraphs where useful, and more direct explanations of the dependency and pattern findings.
  Owner: Sefa / Stefano

- [ ] Problem: The section `Handoff Notes for Patterns and Design Summary` feels redundant in the final report.
  Why it is a problem: Handoff notes are useful during coordination, but they read like internal working notes in a final deliverable.
  Suggested fix: Remove the handoff framing and keep only the information that belongs in the final Summary section.
  Owner: Sefa

- [ ] Problem: Pattern sections use repeated prose bullets instead of a compact comparison structure.
  Why it is a problem: The repeated structure is harder to scan across patterns, especially for recurring fields such as analysis, problem solved, alternative, pros, and cons.
  Suggested fix: For each pattern, use a table with consistent columns such as Analysis, Problem solved, Alternative, Pros, Cons, and Hotspot link.
  Owner: Stefano

- [ ] Problem: The `Integration Notes` section should not remain in the final Design report.
  Why it is a problem: It describes final coordination tasks rather than final design conclusions, which weakens the report's polish.
  Suggested fix: Remove `Integration Notes` and move any still-relevant traceability statement into the Summary.
  Owner: Stefano
