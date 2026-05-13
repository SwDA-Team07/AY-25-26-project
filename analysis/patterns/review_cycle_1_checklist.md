# Review Cycle 1 Checklist - Patterns

Date prepared: 2026-05-06  
Owner: Filippo (`s348651`)  
Feedback recipient: Stefano
Review window target: by 2026-05-10

## Feedback for Stefano

### 1. Proxy Pattern

The current Proxy Pattern example may be weak and should be justified more clearly.

Current candidate:

- `AbstractLogger`: Proxy
- `Logger`: Subject

Questions for Stefano:

1. What is the RealSubject represented by `AbstractLogger`?
2. How should we interpret the role of `AbstractLogger`: as an access-control/delegation layer, or as a shared base implementation for logger behavior, as abstract classes often do?
3. Is Proxy still the strongest interpretation, or would Adapter/Singleton be easier to defend with the selected modules?

`Q1: The RealSubject in the Proxy interpretation would be the log4j-core logger implementation (e.g., Logger.java). The Proxy (AbstractLogger) acts as a front-end to prevent the Core from processing logs that aren't enabled.`
`Q2: It acts as an access-control layer. Its primary job is "short-circuiting"—deciding if a logging event should proceed to the expensive Core logic or stop immediately.`
`Q3: While Proxy is defensible, the Adapter Pattern is stronger and easier to justify`

Suggested action:

- Keep Proxy only if the Subject, Proxy, RealSubject (and Client) can be clearly identified.
- If this mapping cannot be justified, replace Proxy with a stronger pattern.
- Recommended replacement: Adapter Pattern in `log4j-slf4j2-impl`, using `Log4jLogger` / `Log4jLoggerFactory` as adapters between SLF4J and Log4j2.
- Alternative replacement: Singleton Pattern in `StatusLogger`.

### 2. Better explanation

The current Patterns section already has a good base structure: involved classes, location, purpose, why used, and alternatives.

The improvement should focus on making the pattern mapping easier to defend.

Suggested action:

- Add a short summary table immediately after the `## Patterns` heading, before the detailed explanations of individual patterns. Without this table, the section is harder to understand at first reading.
- For each pattern, add one short sentence explaining the concrete interaction between the involved classes.
- Make clear why the example is a real instance of that pattern, not only a generic similarity.
- For each pattern, explicitly answer which problem the pattern solves in Log4j2.
- For each pattern, include one reasonable alternative design and briefly state its pros and cons.
- When helpful, add a small Mermaid diagram to show the class relationship or call flow.
- Keep diagrams small, so they support the text without making the section too long.

Suggested per-pattern structure:

- **Problem solved:** explain the concrete design problem addressed by the pattern.
- **Alternative:** name one plausible alternative design.
- **Pros:** explain what the alternative would improve.
- **Cons:** explain what the alternative would make worse compared with the current pattern.

Suggested summary table format:

| Pattern | Main classes/components | Module |
|---|---|---|
| Adapter | `Log4jLogger`, `Log4jLoggerFactory` | `log4j-slf4j2-impl` |
| Builder | `ConsoleAppender.Builder`, `ConsoleAppender` | `log4j-core` |

Example diagram format:

```mermaid
classDiagram
    Client --> Target
    Target <|.. Adapter
    Adapter --> Adaptee
```

The diagrams should be concise and should only include the classes needed to explain the pattern.

### 3. Minor refinements

Suggested action:

- Use precise file paths for the main examples instead of only shortened paths with `...`.
- Avoid very strong claims such as saying that one pattern is the primary reason for extensibility.
- Keep the links with dependency hotspots only where the relationship is direct and easy to justify.

### 4. Summary consistency

If the Patterns section changes, the Pattern Impact part of the Summary must be updated accordingly.

Suggested action:

- Remove Proxy references from the Summary if Proxy is replaced.
- Align Strategy references with the actual Strategy example used in the Patterns section.
- Soften strong claims that depend on pattern interpretation.
- Keep Summary claims consistent with the final selected pattern set.

## Required Pattern Changes

- [x] Answer the Proxy Pattern questions and keep Proxy only if the mapping is clearly justified.
- [x] If Proxy is replaced, prefer Adapter in `log4j-slf4j2-impl` or Singleton in `StatusLogger`.
- [x] Add a short summary table immediately after the `## Patterns` heading.
- [x] Add a short and clear explanation of the concrete interaction between the classes of each pattern.
- [x] Add a clear "Problem solved" explanation for each pattern.
- [x] Add one alternative design for each pattern.
- [x] Add concise pros and cons for each alternative.
- [x] Add small Mermaid diagrams where they make the pattern structure easier to understand.
- [x] Use precise file paths for the main pattern examples.
- [x] Make strong claims more cautious, especially when linking patterns to dependency hotspots.
- [x] Check that every pattern example belongs to the selected five-module scope.
- [x] Update the Pattern Impact summary after changing the Patterns section.

## Follow-up After Stefano's Revision

The main requested changes were applied correctly: Proxy was replaced with Adapter, the Patterns section now has a summary table, Mermaid diagrams were added, and the Summary no longer references Proxy.

Remaining refinements before final freeze:

- [x] Fix the Adapter roles so they are consistent everywhere: `Log4jLogger` = Adapter, SLF4J logger interface = Target, `ExtendedLogger` / Log4j API = Adaptee. Do not use `org.apache.logging.log4j.Logger` in one place and `ExtendedLogger` in another without explaining the difference.
- [x] Fix the class name typo in the Strategy diagram: use `JsonLayout`, not `JSONLayout`.
- [x] Clarify the Strategy example: explain that appenders use a `Layout` to format each `LogEvent`. If `Appender` is too generic, use a concrete appender class as the context.
- [x] Expand each pattern entry with: problem solved, alternative design, pros, and cons.
