# Architecture Handoff Packet (from Dependencies Evidence)

This note summarizes dependency signals that Architecture owners (Davide and Yaman) can reuse in `docs/architecture.md`, especially for coupling/cohesion and quality attribute reasoning.

## Baseline and Scope

- Baseline commit: `83702bb6194182572eccf6594acf935f83437e76`
- Branch: `2.x`
- Scoped modules:
  - `log4j-core`
  - `log4j-api`
  - `log4j-layout-template-json`
  - `log4j-slf4j2-impl`
  - `log4j-jdbc-dbcp2`
- Scope size: 929 production Java files, 92,131 SLOC (`src/main/java`)

Evidence:

- `summary.txt`
- `scope_loc.csv`

## Signals Useful for C2/C3 Architecture

### Structural dependency center

- `log4j-core` is the main structural hub.
- Strong cross-module flow: `log4j-core -> log4j-api` (816 import edges).

Evidence:

- `import_edges.csv`
- `import_stats.csv`

### Hotspots (shared extension/integration points)

- `Plugin.java` (`total=219`, `imports_received=213`)
- `LogEvent.java` (`total=217`, `imports_received=208`)
- `StatusLogger.java` (`total=185`)

Use in architecture text:

- Support claims about extensibility and stable abstraction boundaries.
- Motivate why API/Core separation is critical for maintainability.

Evidence:

- `import_stats.csv`

### Maintenance coupling clusters (co-change)

- Rolling/appender cluster:
  - `DefaultRolloverStrategy.java <-> DirectWriteRolloverStrategy.java` (`2`, no direct import)
  - `RollingFileManager.java <-> RollingRandomAccessFileManager.java` (`2`, no direct import)
- Network/config cluster:
  - `SslSocketManager.java <-> SslConfiguration.java` (`2`, direct import)
- Connection manager cluster:
  - `HttpURLConnectionManager.java <-> UrlConnectionFactory.java` (`2`, no direct import)

Use in architecture text:

- Support C3 discussion on maintenance-time coupling and hidden coordination dependencies.
- Support quality-attribute trade-off discussion (extensibility vs maintenance complexity).

Evidence:

- `cochange_pairs.csv`
- `inconsistencies.md`

## Suggested Reuse in `docs/architecture.md`

- C2 container relationships: cite `log4j-core` hub behavior and API/Core flow.
- C3 component discussion: cite hotspots and co-change clusters as coupling evidence.
- Architectural characteristics section: use these signals for maintainability/extensibility arguments.
