# Review Cycle 2 Checklist - Architecture

Date prepared: 2026-05-28  
Reviewer: Stefano (363677) , Sefa (324924)
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

- [x] Problem: Relation direction is inconsistent between C2 and C3 scope overview diagrams for peripheral modules (`log4j-layout-template-json`, `log4j-jdbc-dbcp2`).
  Why it is a problem: In C2, `log4j-core` is shown as using peripheral modules; in C3 scope overview, some edges are shown in the opposite direction as "provides ... for". This makes cross-section reading less coherent even when the meaning is logically close.
  Suggested fix: Pick one direction convention (recommended: consumer -> provider with labels like "uses") and apply it consistently in both C2 and C3 overview diagrams.
  Owner: Davide / Yaman
  > Davide: completed for C2 (2026-05-29). C2 peripheral relations now read consumer -> provider (`log4j-core` -> peripheral, e.g. `formats events via JSON Layout SPI`, `obtains pooled JDBC connections via`). Aligning the C3 scope-overview edges to the same direction remains with Yaman.
  > Yaman: C3 level compeleted (2026/05/31-2026/06/01). THe diagram edges are fixed to match C2 level diagrams.

- [x] Problem: SOLID claims are partially evidence-backed but still miss direct traceability for some rows in the SOLID table.
  Why it is a problem: The review guide asks for evidence-backed claims; a few findings use generic statements without explicit anchors to concrete artifacts or classes, which weakens grading traceability.
  Suggested fix: For each SOLID row, add at least one explicit anchor (class/component path or analysis artifact reference) in the Evidence column.
  Owner: Yaman
   > Yaman: C3 level compeleted (2026/05/31-2026/06/01). Evidences are backed  with more stable, stronger evidences.

- [x] Problem: Minor wording/formatting inconsistencies remain in Architecture prose.
  Why it is a problem: Review Cycle 2 asks for final readability cleanup; small inconsistencies (e.g., mixed style for technical terms and occasional awkward phrasing) reduce clarity and polish.
  Suggested fix: Do one final language/style pass over `docs/architecture.md` with consistent backtick usage for module/class names and concise phrasing.
  Owner: Davide / Yaman
  > Davide: completed for C1/C2 prose (2026-05-29). The Context Description and the C1/C2 element labels use consistent backticked module names and concise phrasing. The C3/SOLID prose pass remains with Yaman.
  > Yaman: C3 level compeleted (2026/05/31-2026/06/01). Some wording errors are found in C3 section, Solid Findings and summary sections.

## Final Review Notes - 2026-06-05

- [x] Problem: The C1 context description still says operations/security teams are external actors, but the current C1 diagram no longer shows that actor.
  Why it is a problem: This creates a small mismatch between the diagram and the prose immediately below it.
  Suggested fix: Either re-add the operations/security actor to the C1 diagram, or change the prose to say they are stakeholders rather than actors shown in the diagram.
  > Davide: done (2026-06-06). Reworded the C1 Context Description so the described external elements match the C1 diagram (applications/SLF4J facade and the output destination systems); developers, operations, security, and DevOps teams are now described as stakeholders, consistent with the Overview report, rather than as actors shown in the diagram.
  

- [ ] Problem: The `log4j-core` C3 diagram is very dense and wide compared with the other diagrams.
  Why it is a problem: The diagram is technically complete, but it may be harder to read in the final Markdown/PDF because it contains many internal components plus several external context elements.
  Suggested fix: Consider reducing the external context shown in the `log4j-core` C3 diagram, or split the diagram into a runtime pipeline view and an output/integration context view if readability is poor in the final render.
  

- [ ] Problem: A few minor grammar issues remain in `docs/architecture.md`.
  Why it is a problem: The report is close to final, so small grammar errors stand out more during final evaluation.
  Suggested fix: Fix examples such as "interacting with logging system" -> "interacting with the logging system" and "Some architectural trade-offs remains present" -> "Some architectural trade-offs remain present".
  > Davide: C1/C2 prose reviewed (2026-06-06), no grammar issues found there. The two cited examples are outside the C1/C2 scope: "interacting with logging system" is in the C3 `log4j-api` container description and "trade-offs remains present" is in the Summary, both owned by Yaman. Left unchecked pending Yaman's grammar pass on those sections.


- [ ] Problem: Complete decoupling between the C3 architecture description and the documented design patterns (`docs/design.md`).
  Why it is a problem: The current text mentions abstract extension capabilities but fails to explicitly connect them to the behavioral patterns analyzed by the team (Adapter, Builder, Strategy, Chain of Responsibility). This reduces cross-document traceability and weakens the architectural narrative.
  Suggested fix: Integrate clear references to design patterns within the container descriptions, the quality attributes section, and the summary block to anchor structural elasticity to concrete behavioral principles.
  Owner: Yaman

- [ ] Problem: Inconsistent list structures and missing backticks for software components within the C3 container descriptions.
  Why it is a problem: While peripheral modules like `log4j-layout-template-json` use a clean, bolded numbering scheme, the core modules (`log4j-api` and `log4j-core`) lack a unified markup style, which hurts document uniformity.
  Suggested fix: Standardize all component lists under a uniform bolded header format and ensure all class or component names are consistently enclosed in backticks.
  Owner: Yaman
