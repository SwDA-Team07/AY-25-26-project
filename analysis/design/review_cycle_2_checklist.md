# Review Cycle 2 Checklist - Design

Date prepared: 2026-06-06
Reviewer: Yaman (355144), Davide (346733), Filippo (348651)   
Scope: [`docs/design.md`](../../docs/design.md)

## Review Goal

Check whether the Design report is clear, understandable, and consistent with the Overview and Architecture reports.

## Review Steps

- Read the full Design report.
- Check consistency with `docs/overview.md`.
- Check consistency with `docs/architecture.md`.
- Check that dependencies, patterns, and summary stay within the project requirements.
- Check whether any statement or paragraph is difficult to understand.
- Check wording, typos, links, and formatting.

## Findings

Add one checkbox per issue found. If no issue is found, write: `Review completed: no issues found.`

- [x] Problem: The Design report is not yet smooth enough to read.
  Why it is a problem: Some sections are understandable, but the reading flow is still heavy and can make the design rationale harder to follow.
  Suggested fix: Rewrite the Design report with clearer transitions, shorter paragraphs where useful, and more direct explanations of the dependency and pattern findings.
  Owner: Sefa / Stefano

- [x] Problem: The section `Handoff Notes for Patterns and Design Summary` feels redundant in the final report.
  Why it is a problem: Handoff notes are useful during coordination, but they read like internal working notes in a final deliverable.
  Suggested fix: Remove the handoff framing and keep only the information that belongs in the final Summary section.
  Owner: Sefa

- [x] Problem: Pattern sections use repeated prose bullets instead of a compact comparison structure.
  Why it is a problem: The repeated structure is harder to scan across patterns, especially for recurring fields such as analysis, problem solved, alternative, pros, and cons.
  Suggested fix: For each pattern, use a table with consistent columns such as Analysis, Problem solved, Alternative, Pros, Cons, and Hotspot link.
  Owner: Stefano

- [x] Problem: The `Integration Notes` section should not remain in the final Design report.
  Why it is a problem: It describes final coordination tasks rather than final design conclusions, which weakens the report's polish.
  Suggested fix: Remove `Integration Notes` and move any still-relevant traceability statement into the Summary.
  Owner: Stefano

### Davide (346733) - consistency review (Design vs Overview/Architecture) - 2026-06-06

- [x] Problem: The Patterns summary table and the detailed Strategy section list different participants for the Strategy pattern.
  Why it is a problem: The summary table row for Strategy lists `Layout, PatternLayout, JsonLayout, LogEvent`, but the detailed section names the Context as `AbstractAppender` (which is missing from the table) and treats `LogEvent` as the shared event data passed to the strategy, not as a participant class. The Architecture C3 view models the same `Appender` -> `Layout` formatting relation, so the table should match the detail and the Architecture report.
  Suggested fix: Align the summary table with the detailed section: add `AbstractAppender` as the Context, and either drop `LogEvent` from the class list or relabel it as the shared event/context object.
  Owner: Stefano

- [x] Problem: `JsonLayout` (Design) and `JsonTemplateLayout` (Architecture) can be read as the same class across reports.
  Why it is a problem: The Design Strategy example uses core's `org.apache.logging.log4j.core.layout.JsonLayout`, while the Architecture report enters the `log4j-layout-template-json` container through `JsonTemplateLayout`. The near-identical names may make a reader think the JSON layout discussed in Design is the same class as the one in the JSON-template module, which it is not.
  Suggested fix: Use the fully qualified `core.layout.JsonLayout` in the Strategy example, or add a one-line note clarifying that it is distinct from `JsonTemplateLayout` in `log4j-layout-template-json`.
  Owner: Stefano

- [x] Problem: The Adapter Target is labelled inconsistently between prose and diagram.
  Why it is a problem: The Adapter section writes the Target interface as `org.slf4j.Logger` in the table and prose, but the class diagram labels the same node `SLF4J_Logger`. The Cycle 1 patterns review already asked to keep Adapter roles consistent everywhere.
  Suggested fix: Use one label for the Target (e.g. `org.slf4j.Logger`) in both the prose/table and the class diagram.
  Owner: Stefano

- Consistency confirmation (no issue): The cross-report invariants are consistent across `docs/overview.md`, `docs/design.md`, and `docs/architecture.md` — the five-module scope, `92,131` SLOC / `929` production files, the snapshot commit `83702bb...`, and the `log4j-core -> log4j-api` (`816` imports) dependency direction all match.

## Resolution Notes

Resolved on 2026-06-06:

- Removed internal handoff/integration-note framing from the final Design report.
- Rewrote the dependency and summary prose for smoother final-report flow.
- Converted the repeated pattern prose into compact comparison tables.
- Aligned Strategy participants by adding `AbstractAppender` as context and treating `LogEvent` as the shared event object.
- Clarified that `org.apache.logging.log4j.core.layout.JsonLayout` is distinct from Architecture's `JsonTemplateLayout`.
- Aligned Adapter target wording by using `org.slf4j.Logger` consistently in prose/table and diagram label.
