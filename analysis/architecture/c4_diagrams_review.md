# C4 Diagrams Review - Architecture

Date prepared: 2026-05-26  
Reviewer: Filippo (`s348651`)  
Scope: C4 diagrams only in [`docs/architecture.md`](../../docs/architecture.md)

## Main Suggestions

- [ ] Replace generic Mermaid `flowchart` diagrams with the Mermaid C4 syntax/tooling.
  - Use `C4Context` for C1.
  - Use `C4Container` for C2.
  - Use `C4Component` for C3.

- [ ] Use different C4 element types/shapes instead of plain boxes for everything.
  - Use `Person` for users/teams such as operations or developers.
  - Use `System` or `System_Ext` for external software systems.
  - Use `Container` or `Container_Ext` for internal/external containers.
  - Use `Component` for C3 elements.
  - Actors, external systems, internal modules, databases, configuration files, and output destinations should be visually distinguishable.
  - Add a small legend if the notation is not obvious.

- [ ] Add clear system boundaries.
  - C1 should make `Apache Log4j2` the system in scope.
  - C2 should put the analyzed Log4j2 modules inside the Log4j2 boundary.
  - External actors, APIs, databases, file systems, and monitoring systems should stay outside.

- [ ] Make relationship labels more explicit.
  - Avoid vague labels such as `delegates` or `uses layouts`.
  - Prefer labels such as `calls Java API`, `implements SPI`, `writes log events to`, or `loads configuration from`.

- [ ] Keep C3 diagrams focused on components inside one container.
  - External elements may be shown only as context.
  - The `Scope Overview` diagram should be moved/relabelled because it is a module dependency overview, not a real C3 component diagram.

- [ ] Fix minor consistency issues.
  - Rename `Diagram of Lo4j-core` to `Diagram of log4j-core`.
  - Keep names and labels consistent with the C4 level they belong to.

## Priority

1. Convert `flowchart` diagrams to Mermaid C4 diagrams.
2. Add boundaries and proper C4 element types.
3. Clarify/justify Maven modules as C2 containers.
4. Move or relabel the `Scope Overview` diagram.
