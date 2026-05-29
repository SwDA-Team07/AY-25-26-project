# Review Cycle 2 Checklist - Architecture

Date prepared: 2026-05-28  
Reviewer: Stefano () , Sefa (324924)
Scope: [`docs/architecture.md`](../../docs/architecture.md)

## Review Goal

Check whether the Architecture report is clear, understandable, and consistent with the Overview and Design reports.

## Review Steps

- Read the full Architecture report.
- Check consistency with `docs/overview.md`.
- Check consistency with `docs/design.md`.
- Check that C1, C2, and C3 diagrams are understandable and coherent.
- Check the dedicated C4 cycle 2 review in [`c4_diagrams_review_cycle_2.md`](./c4_diagrams_review_cycle_2.md).
- Check that SOLID and architectural quality claims are evidence-backed.
- Check whether any statement or paragraph is difficult to understand.
- Check wording, typos, links, and formatting.

## Findings

Add one checkbox per issue found. If no issue is found, write: `Review completed: no issues found.`

- [ ] Problem: Relation direction is inconsistent between C2 and C3 scope overview diagrams for peripheral modules (`log4j-layout-template-json`, `log4j-jdbc-dbcp2`).
  Why it is a problem: In C2, `log4j-core` is shown as using peripheral modules; in C3 scope overview, some edges are shown in the opposite direction as "provides ... for". This makes cross-section reading less coherent even when the meaning is logically close.
  Suggested fix: Pick one direction convention (recommended: consumer -> provider with labels like "uses") and apply it consistently in both C2 and C3 overview diagrams.
  Owner: Davide / Yaman
  > Davide: completed for C2 (2026-05-29). C2 peripheral relations now read consumer -> provider (`log4j-core` -> peripheral, e.g. `formats events via JSON Layout SPI`, `obtains pooled JDBC connections via`). Aligning the C3 scope-overview edges to the same direction remains with Yaman.

- [ ] Problem: SOLID claims are partially evidence-backed but still miss direct traceability for some rows in the SOLID table.
  Why it is a problem: The review guide asks for evidence-backed claims; a few findings use generic statements without explicit anchors to concrete artifacts or classes, which weakens grading traceability.
  Suggested fix: For each SOLID row, add at least one explicit anchor (class/component path or analysis artifact reference) in the Evidence column.
  Owner: Yaman

- [ ] Problem: Minor wording/formatting inconsistencies remain in Architecture prose.
  Why it is a problem: Review Cycle 2 asks for final readability cleanup; small inconsistencies (e.g., mixed style for technical terms and occasional awkward phrasing) reduce clarity and polish.
  Suggested fix: Do one final language/style pass over `docs/architecture.md` with consistent backtick usage for module/class names and concise phrasing.
  Owner: Davide / Yaman
  > Davide: completed for C1/C2 prose (2026-05-29). The Context Description and the C1/C2 element labels use consistent backticked module names and concise phrasing. The C3/SOLID prose pass remains with Yaman.
