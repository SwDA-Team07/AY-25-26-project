# C4 Diagrams Review Cycle 2 - Architecture

Date prepared: 2026-05-28  
Reviewer: Filippo (`s348651`)  
Scope: C1, C2, and C3 diagrams in [`docs/architecture.md`](../../docs/architecture.md)

## Review Goal

Check that all C4 diagrams are mutually consistent, use the correct C4 level notation, and provide enough relationship detail to be understandable without relying only on surrounding prose.

## Findings

- [x] Problem: C4 diagrams do not consistently preserve connected parent-level context across levels.
  Why it is a problem: Component diagrams should show the connected containers and external systems that interact with the components; container diagrams should show the connected external systems; this context should be carried recursively from C1 to C2 to C3. Without this, the reader cannot easily trace the same relationship across abstraction levels.
  Suggested fix: For each C3 diagram, include the relevant connected container(s) and external system(s) as context. For each C2 diagram, include the relevant external system(s). Keep the same relationship meaning when moving between levels.
  Owner: Davide for C1/C2, Yaman for C3
  > Davide: completed for C1/C2 (2026-05-29). C2 carries the C1 external actors (`App`, `SLF4J 2 API`) and the external destination systems (File System, Console, Network Endpoints, JDBC Databases, Log Aggregation / Monitoring); C3 portion remains with Yaman.
  > Yaman: completed C3 (2026/05/31). diagrams are interconnected with each other. Ex: API and CORE connections are now can be seen in C3 level diagrams.

- [x] Problem: The C1 context diagram still models configuration as an external system.
  Why it is a problem: Configuration is not an external actor/system at context level; showing it as an external system makes the C1 boundary misleading and inconsistent with the later container/component diagrams.
  Suggested fix: Remove the configuration external system from the context diagram. If configuration must be discussed, model it at the lower level where configuration files, loaders, or plugins are relevant.
  Owner: Davide
  > Davide: done (2026-05-29). Removed the `Configuration Files` external system and its relation from C1; the Context Description now states configuration is modelled at the container/component level.

- [x] Problem: Naming is not fully consistent across all C4 diagrams.
  Why it is a problem: The same module, container, component, or external system may appear with slightly different names across C1/C2/C3, which makes cross-diagram comparison harder and weakens traceability.
  Suggested fix: Create one naming convention and reuse it everywhere, including capitalization and module names such as `log4j-api`, `log4j-core`, `log4j-layout-template-json`, `log4j-slf4j2-impl`, and `log4j-jdbc-dbcp2`.
  Owner: Davide for C1/C2, Yaman for C3
  > Davide: completed for C1/C2 (2026-05-29). C1/C2 use the canonical module names consistently; C3 portion remains with Yaman.
  > Yaman: All C3 level diagrams renamed to be more clear with its corresponging model (2026/05/31).

- [x] Problem: Diagram levels are not repeated explicitly for every diagram.
  Why it is a problem: Readers should immediately know whether each diagram is C1, C2, or C3, especially when several diagrams appear close together.
  Suggested fix: Repeat the C4 level in every diagram title/caption, for example `C3 Component Diagram - log4j-core`, `C3 Component Diagram - log4j-api`, and so on.
  Owner: Davide for C1/C2, Yaman for C3
  > Davide: completed for C1/C2 (2026-05-29). Titles now read `C1 System Context Diagram - Apache Log4j2` and `C2 Container Diagram - Apache Log4j2`; C3 portion remains with Yaman.
  > Yaman: C3 section rename is completed (2026/05/31). Titles are now using their Component Level name.

- [x] Problem: Several relationship labels are too generic, for example only `uses` or `implements`.
  Why it is a problem: Generic labels do not explain the actual interaction and do not satisfy the request for a small description or method on every arrow.
  Suggested fix: Give every arrow a short concrete label describing the called API, method, protocol, or responsibility, such as `calls Logger API`, `creates LogEvent`, `loads configuration`, `writes JDBC event`, or `adapts SLF4J calls`.
  Owner: Davide for C1/C2, Yaman for C3
  > Davide: completed for C1/C2 (2026-05-29). C2 arrows now use concrete labels (e.g. `calls Logger API`, `delegates SLF4J calls to Logger API`, `implements logging abstractions of`, `formats events via JSON Layout SPI`, `obtains pooled JDBC connections via`); C3 portion remains with Yaman.
  > Yaman: changes completed for C3 (2026/05/31). In the diagrams the connection roads are now use more concrete labels (ex: `formats log events using`, `extends layouts via SPI`, `creates and manages logger contexts through` and so on).

- [x] Problem: Some arrows overlap with other components, containers, or labels.
  Why it is a problem: Overlapping arrows reduce readability and make the diagram look inconsistent even when the model is correct.
  Suggested fix: After content corrections, adjust diagram layout, direction, grouping, and relationship ordering so arrows do not cross through unrelated elements or cover labels.
  Owner: Davide for C1/C2, Yaman for C3
  > Davide: open. The C1/C2 content corrections are done; the Mermaid C4 renderer auto-lays out these diagrams and removing the configuration node already reduced C1 crossings. Left unchecked pending a visual render pass and the C3 portion (Yaman).
  > Yaman: The problem with the overlapping/on top wording is the diagram renderer we use, Mermaid. Some changes are made that will increases the readability of the C3 diagrams. but it still is scrambled.

## Final Review Findings (2026-06-01)

- [ ] Problem: Some diagrams still have overlapping arrows or labels.
  Why it is a problem: Overlap reduces diagram readability.
  Suggested fix: Render the diagrams and adjust the layout where needed.
  Owner: Davide / Yaman
  > Davide: C1/C2 reviewed (2026-06-03). After the cycle-2 content fixes the C1 and C2 diagrams render without overlapping arrows or labels. The residual overlap is in the denser C3 diagrams (Yaman), which is a known Mermaid auto-layout limitation; left unchecked until the C3 side is also clean.

- [ ] Problem: External destination names are not fully consistent across C1, C2, and C3.
  Why it is a problem: The database destination is named differently, and `Log Aggregation / Monitoring` is not present in C3.
  Suggested fix: Reuse the same external destination names across levels.
  Owner: Yaman

- [x] Problem: The external database is modelled as a generic external system.
  Why it is a problem: Mermaid C4 supports a specific external database element.
  Suggested fix: Use Mermaid `SystemDb_Ext` for the external database where appropriate (see `references/links.md`).
  Owner: Davide
  > Davide: done (2026-06-03). The `JDBC Databases` external system now uses `SystemDb_Ext` in both the C1 and C2 diagrams, rendering it with the dedicated database shape.

- [ ] Problem: Some C3 relationship directions are still ambiguous.
  Why it is a problem: The C3 overview uses a different direction convention from some detailed C3 diagrams.
  Suggested fix: Make the C3 relationship direction convention consistent across overview and detailed diagrams.
  Owner: Yaman

## Priority

1. Remove the configuration external system from C1.
2. Standardize names across all diagrams.
3. Add the missing connected context recursively from C1 to C2 to C3.
4. Repeat the C4 level in every diagram title/caption.
5. Replace generic arrow labels with concrete interaction descriptions.
6. Clean up arrow layout so lines and labels do not overlap diagram elements.
