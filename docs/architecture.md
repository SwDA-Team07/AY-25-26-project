# Software Architecture — Apache Log4j2

**C4 Model Tool Used:** Mermaid diagrams embedded in Markdown.

---

## Context Level (C1)

### System Context Diagram
```mermaid
C4Context
    title C1 System Context Diagram - Apache Log4j2

    System_Ext(App, "Applications / Libraries", "Java applications that emit log calls")
    System_Ext(SLF4J, "SLF4J 2 API", "Logging facade bridged to Log4j2")

    System(Log4j2, "Apache Log4j2", "Java logging framework in scope of this analysis")

    System_Ext(DestFile, "File System", "Log file destination")
    System_Ext(DestConsole, "Console", "Standard output / error")
    System_Ext(DestNet, "Network Endpoints", "Syslog / HTTP / SMTP")
    SystemDb_Ext(DestDb, "JDBC Databases", "Relational database destinations")
    System_Ext(LogAgg, "Log Aggregation / Monitoring", "Downstream observability stacks")

    Rel(App, Log4j2, "logs via Logger API")
    Rel(SLF4J, Log4j2, "bridged by log4j-slf4j2-impl")

    Rel(Log4j2, DestFile, "writes log events")
    Rel(Log4j2, DestConsole, "writes log events")
    Rel(Log4j2, DestNet, "writes log events")
    Rel(Log4j2, DestDb, "writes log events")
    Rel(Log4j2, LogAgg, "forwards logs")
```

### Context Description
Apache Log4j2 is a Java logging framework used as a library inside applications.
The system boundary includes the `log4j-api` and implementation modules; external
actors include application developers, operations and security teams, and
systems that receive log output. Log4j2 accepts log calls from applications or the
SLF4J 2 facade and delivers formatted log events to files, consoles, network
endpoints, databases, or monitoring stacks. Configuration is not an external system
at context level; it is modelled at the container and component levels where the
configuration loader and plugins are relevant.

---

## Container Level (C2)

### Container Diagram
```mermaid
C4Container
    title C2 Container Diagram - Apache Log4j2

    System_Ext(App, "Applications / Libraries", "Java applications that emit log calls")
    System_Ext(SLF4J, "SLF4J 2 API", "Logging facade bridged to Log4j2")

    System_Boundary(log4j2, "Apache Log4j2") {
        Container(Log4jApi, "log4j-api", "Java", "Public logging API used by applications and adapters")
        Container(Log4jCore, "log4j-core", "Java", "Logging implementation, configuration, filters, appenders, runtime pipeline")
        Container(JsonLayout, "log4j-layout-template-json", "Java", "JSON layout templates for structured output")
        Container(SLF4JImpl, "log4j-slf4j2-impl", "Java", "Adapter bridging SLF4J 2 calls to Log4j2 API")
        Container(JdbcDbcp2, "log4j-jdbc-dbcp2", "Java, Apache DBCP2", "JDBC appender integration writing log events to databases")
    }

    System_Ext(DestFile, "File System", "Log file destination")
    System_Ext(DestConsole, "Console", "Standard output / error")
    System_Ext(DestNet, "Network Endpoints", "Syslog / HTTP / SMTP")
    SystemDb_Ext(DestDb, "JDBC Databases", "Relational database destinations")
    System_Ext(LogAgg, "Log Aggregation / Monitoring", "Downstream observability stacks")

    Rel(App, Log4jApi, "calls Logger API")
    Rel(SLF4J, SLF4JImpl, "discovered via ServiceLoader")
    Rel(SLF4JImpl, Log4jApi, "delegates SLF4J calls to Logger API")
    Rel(Log4jCore, Log4jApi, "implements logging abstractions of")
    Rel(Log4jCore, JsonLayout, "formats events via JSON Layout SPI")
    Rel(Log4jCore, JdbcDbcp2, "obtains pooled JDBC connections via")

    Rel(Log4jCore, DestFile, "writes log events")
    Rel(Log4jCore, DestConsole, "writes log events")
    Rel(Log4jCore, DestNet, "writes log events")
    Rel(JdbcDbcp2, DestDb, "writes log events over pooled JDBC connections")
    Rel(Log4jCore, LogAgg, "forwards logs")
```

### Container Description
The analyzed scope is a set of Java library modules that are packaged together
and embedded into JVM applications. Containers correspond to the main Maven
modules included in the analysis scope.

#### Containers:
1. **log4j-api**
   - Type: Java library
   - Technology: Java
   - Responsibility: Public logging API used by applications and adapters.

2. **log4j-core**
   - Type: Java library
   - Technology: Java
   - Responsibility: Logging implementation, configuration, filters, appenders, and runtime pipeline.

3. **log4j-layout-template-json**
   - Type: Java library
   - Technology: Java
   - Responsibility: JSON layout templates used by core for structured output.

4. **log4j-slf4j2-impl**
   - Type: Java library
   - Technology: Java
   - Responsibility: Adapter that bridges SLF4J 2 calls to Log4j2 API.

5. **log4j-jdbc-dbcp2**
   - Type: Java library
   - Technology: Java, Apache DBCP2
   - Responsibility: JDBC appender integration that writes log events to databases.

### Relationship with Clean Architecture Blueprint
The module split between `log4j-api` and `log4j-core` reflects a boundary between
stable interfaces and implementation details, which aligns with Clean
Architecture separation of abstractions from concrete mechanisms. The
implementation module depends on the API, not the other way around, which keeps
the public surface stable. However, Log4j2 is a library framework rather than a
traditional layered application, so the plugin system and appenders are built
inside the core module instead of as isolated outer layers. This trade-off favors
performance and configurability over a strict inward-only dependency rule.

---

## Component Level (C3)

### Component Diagrams

#### Diagram of `log4j-core`

```mermaid
C4Component 
title C3 Component Diagram - log4j-core

Container_Ext(api, "log4j-api",, "Public logging API")
System_Ext(net, "Network Endpoints", "Syslog / HTTP / SMTP")
Container_Ext(jdbc, "log4j-jdbc-dbcp2",, "JDBC integration")
System_Ext(logAgg, "Log Aggregation / Monitoring", "Downstream observability stacks")
SystemDb_Ext(db, "JDBC Databases", "Relational database destinations")
Container_Ext(json, "log4j-layout-template-json",, "JSON Layout module")
System_Ext(file, "File System", "Log file destination")
System_Ext(console, "Console", "Standard output / error")

Container_Boundary(core, "log4j-core") {

    Component(ctx, "LoggerContext",, "Runtime state and lifecycle manager")
    Component(conf, "Configuration",, "Configuration loading and management")
    Component(lconf, "LoggerConfig",, "Log event routing rules")
    Component(app, "Appender",, "Log event output destination")
    Component(filter, "Filter",, "Log event filtering rules")
    Component(plugin, "Plugin System",, "SPI-based extension framework")
    Component(layout, "Layout",, "Log event formatting engine")
    Component(async, "Async Logger",, "Asynchronous event processing")
}

Rel(ctx, conf, "loads configuration from")
Rel(conf, lconf, "creates logging configuration")
Rel(lconf, app, "routes log events to")
Rel(app, layout, "formats log events using")
Rel(lconf, filter, "applies filtering rules via")
Rel(plugin, app, "extends appenders via SPI")
Rel(plugin, layout, "extends layouts via SPI")
Rel(plugin, filter, "extends filters via SPI")
Rel(async, app, "dispatches events asynchronously to")
Rel(app, logAgg, "forwards logs to")
Rel(api, ctx, "creates and manages logger contexts through")
Rel(layout, json, "invokes Layout SPI implemented by")
Rel(app, jdbc, "obtains JDBC connections through")
Rel(app, file, "writes log events")
Rel(app, console, "writes log events")
Rel(app, net, "writes log events")
Rel(app, db, "writes log events through JDBC")
```
 
#### Diagram of `log4j-api`

```mermaid
C4Component
title C3 Component Diagram - log4j-api

System_Ext(app, "Applications / Libraries", "Java applications that emit log calls")
Container_Ext(slf4jImpl, "log4j-slf4j2-impl",, "SLF4J adapter")
Container(core, "log4j-core", "Java Library", "Runtime logging engine")

Container_Boundary(api, "log4j-api") {

    Component(status, "StatusLogger",, "Internal status diagnostics")
    Component(lf, "LoggerFactory / Provider",, "Provider discovery mechanism")
    Component(logger, "Logger API",, "Public logging interface")
    Component(event, "LogEvent Contract",, "Log event abstraction")
    Component(lm, "LogManager",, "Logger creation and lookup")
    Component(ext, "ExtendedLogger",, "Extended logging operations")
    Component(msgFactory, "MessageFactory",, "Structured message creation")
    Component(msg, "Message",, "Log message abstraction")
    Component(simple, "SimpleLogger",, "Fallback logging implementation")    
}

Rel(app, lm, "requests logger via")
Rel(lm, lf, "resolves provider using")
Rel(lf, logger, "creates logger instance")
Rel(logger, ext, "extends API with")
Rel(logger, msgFactory, "builds messages via")
Rel(msgFactory, msg, "creates Message instances")
Rel(logger, event, "emits log events")
Rel(lm, simple, "fallback when no core available")
Rel(lm, status, "publishes internal diagnostics to")
Rel(slf4jImpl, lm, "obtains loggers through")
Rel(core, logger, "implements logging abstractions exposed by")
```

#### Diagram of `log4j-layout-template-json`

```mermaid
C4Component
title C3 Component Diagram - log4j-layout-template-json

Container_Ext(core, "log4j-core",, "Provides Layout SPI")
Container_Ext(api, "log4j-api",, "Provides LogEvent model")

Container_Boundary(layout, "log4j-layout-template-json") {

    Component(json, "JsonTemplateLayout",, "JSON layout implementation")
    Component(resolver, "TemplateResolver",, "JSON template resolution engine")
    Component(registry, "EventResolver Registry",, "Event field resolver registry")
    Component(builtin, "Built-in EventResolvers",, "Standard Field Extractors")
    Component(writer, "JsonWriter",, "Low-allocation JSON serializer")
}

Rel(core, json, "invokes Layout SPI on")
Rel(json, resolver, "resolves template using")
Rel(resolver, registry, "looks up field resolvers in")
Rel(registry, builtin, "returns resolver implementations from")
Rel(builtin, api, "reads LogEvent fields from")
Rel(json, writer, "writes JSON output through")

```

#### Diagram of `log4j-slf4j2-impl`

```mermaid
C4Component
title C3 Component Diagram - log4j-slf4j2-impl

System_Ext(slf4jApi, "SLF4J 2 API", "External logging facade")
Container_Ext(core, "log4j-core",, "Runtime logging engine")
Container_Ext(log4jApi, "log4j-api",, "Log4j2 public API")


Container_Boundary(slf4jImpl, "log4j-slf4j2-impl") {

    Component(mdc, "Log4jMDCAdapter",, "SLF4J MDC bridge")
    Component(provider, "Log4jServiceProvider",, "SLF4J ServiceLoader provider")
    Component(factory, "Log4jLoggerFactory",, "SLF4J logger factory adapter")
    Component(adapter, "Log4jLogger",, "SLF4J-to-Log4j adapter")
    Component(marker, "Log4jMarkerFactory",, "SLF4J marker bridge")
}

Rel(slf4jApi, provider, "discovers provider through ServiceLoader")
Rel(provider, factory, "provides logger factory")
Rel(factory, adapter, "creates adapter logger")
Rel(adapter, log4jApi, "delegates SLF4J Logger calls to")
Rel(slf4jApi, marker, "routes marker operations through")
Rel(slf4jApi, mdc, "routes MDC operations through")
```

#### Diagram of `log4j-jdbc-dbcp2`

```mermaid
C4Component
title C3 Component Diagram - log4j-jdbc-dbcp2

Container_Ext(core, "log4j-core",, "Runtime logging engine")
System_Ext(db, "JDBC Databases", "Relational database destinations")

Container_Boundary(jdbc2, "log4j-jdbc-dbcp2") {

    Component(pcs, "PoolingDriverConnectionSource",, "ConnectionSource SPI", "Provides pooled JDBC connections")
    Component(dbcp, "Commons DBCP Pool",, "Connection Pool", "Manages JDBC connection pooling")
}

Rel(core, pcs, "requests JDBC connections from")
Rel(pcs, dbcp, "manages pooled connections via")
Rel(dbcp, db, "opens JDBC connections to")
Rel(core, db, "writes log events to")
```

#### Module Dependency Overview

```mermaid
C4Container
title C3 Component-Level Module Dependency Overview

System_Boundary(log4j2, "Apache Log4j2") {

    Container(jdbc, "log4j-jdbc-dbcp2",, "Java Library", "JDBC connection pooling integration")
    Container(core, "log4j-core",, "Java Library", "Runtime logging engine")
    Container(api, "log4j-api",, "Java Library", "Public logging API")
    Container(slf2, "log4j-slf4j2-impl",, "Java Library", "SLF4J 2 adapter")
    Container(ltj, "log4j-layout-template-json",, "Java Library", "JSON Layout implementation")
    
    
}

Rel(core, api, "implements logging abstractions from")
Rel(core, ltj, "uses Layout SPI implementation from")
Rel(core, jdbc, "uses JDBC ConnectionSource from")
Rel(slf2, api, "adapts SLF4J calls onto")
```

The 816 cross-module import edges between `log4j-core` and `log4j-api` and the central hotspots `Plugin.java`, `LogEvent.java`, and `StatusLogger.java` (see [architecture_handoff_packet.md](../analysis/dependencies/architecture_handoff_packet.md)) confirm that the API/Core split is the main extensibility boundary, while the three peripheral modules plug into that boundary via the Layout, Appender, and provider SPIs.


### Container: `log4j-api`

#### Container Description
The `log4j-api` container provides the public logging interface used by applications and libraries. It defines the core abstractions for creating loggers, creating log messages, and interacting with logging system independently of the runtime implementation.

Components:

1. Logger API
   - Responsibility: Provides public logging interface used by applications.
2. LogManager
   - Responsibility: Creates and retrieves logger instances.
3. Message Factory
   - Responsibility: Supports structured and parameterized logging messages.
4. Simple Logger
   - Responsibility: Provides minimal default logging implementation.

### Container: `log4j-core` 

#### Container Description
The `log4j-core` container contains the primary runtime implementation of Log4j2. It is responsible for configuration management, log event processing, filtering, formatting, plugin extensibility, and output delivery.

Components:

1. LoggerContext
   - Responsibility: Maintains runtime logging state and logger lifecycle management.
2. Configuration
   - Responsibility: Loads and manages logging configuration.
3. Appender
   - Responsibility: Sends log events to output destinations.
4. Layout
   - Responsibility: Formats log events before output.
5. Filter
   - Responsibility: Determines whether log events should be processed.
6. Plugin System
   - Responsibility: Supports extensibility for appenders, layouts, and filters.
7. Async Logger
   - Responsibility: Provides asynchronous log event processing.

### Container: `log4j-layout-template-json`

#### Container Description
The `log4j-layout-template-json` container provides a fast, garbage-free `Layout` implementation that serializes a `LogEvent` into JSON according to a user-supplied template. It plugs into the Layout SPI exposed by `log4j-core` and is the recommended layout for modern observability pipelines (ELK, OpenSearch, Loki) where structured rather than free-text output is required.

**Components:**

1. **JsonTemplateLayout**
   - Responsibility: Entry point implementing the core `Layout` interface; orchestrates template parsing and event serialization.
2. **TemplateResolver / EventResolver registry**
   - Responsibility: Parses the JSON template once at startup and binds each placeholder to a resolver that knows how to read a specific field from a `LogEvent`.
3. **Built-in EventResolvers**
   - Responsibility: Provide out-of-the-box resolution for common fields (timestamp, level, message, thread, MDC, exception, stack trace).
4. **JsonWriter**
   - Responsibility: Low-allocation JSON encoder used by resolvers to write output buffers efficiently.

### Container: `log4j-slf4j2-impl`

#### Container Description
The `log4j-slf4j2-impl` container is the **Adapter** between the SLF4J 2 API and the Log4j2 API. Applications that program against SLF4J can switch to Log4j2 as the runtime backend simply by placing this artifact on the classpath; the SLF4J `ServiceLoader` discovery then routes every SLF4J call into `log4j-api`.

**Components:**

1. **Log4jServiceProvider**
   - Responsibility: SLF4J 2 service provider entry point; discovered via `ServiceLoader` and exposes the factory and adapters to SLF4J.
2. **Log4jLoggerFactory**
   - Responsibility: Creates SLF4J `Logger` instances backed by Log4j2.
3. **Log4jLogger (Adapter)**
   - Responsibility: Adapts each SLF4J `Logger` call to the corresponding `ExtendedLogger` call in `log4j-api`.
4. **Log4jMarkerFactory / Log4jMDCAdapter**
   - Responsibility: Bridge SLF4J marker and MDC concepts onto the Log4j2 equivalents.

### Container: `log4j-jdbc-dbcp2`

#### Container Description
The `log4j-jdbc-dbcp2` container supplies a pooled JDBC `ConnectionSource` for the JDBC Appender defined in `log4j-core`. It uses Apache Commons DBCP 2 to keep connection acquisition cheap when log events are persisted to a relational database.

**Components:**

1. **PoolingDriverConnectionSource**
   - Responsibility: Implements the `ConnectionSource` SPI expected by the JDBC Appender and hands out pooled connections.
2. **Commons DBCP pool integration**
   - Responsibility: Configures and manages the underlying connection pool (sizing, validation, eviction).

### Out-of-Scope Context

Additional Log4j2 integration modules exist outside the selected scope, but they are not expanded at C3 level because the analyzed modules already cover the primary API/runtime boundary, extension SPI mechanisms, external adapters, and infrastructure integrations required for this analysis.

### SOLID Principles Analysis at Level 3

The Log4j2 architecture demonstrates an emphasis on modularity, extensibility, and separation of concerns through a clear distinction between API components, runtime core components, and external integration modules. Architectural decomposition of the system mostly aligns well with several SOLID principles, particularly regarding extensibility, modular separation, and interface-based integration. This is achieved through the use of plugin-based extensibility, abstraction layers, and separation between `log4j-api` and `log4j-core`.

At component level, the architecture generally maintains high cohesion by assigning focused responsibilities to components such as `Appender`, `Layout`, `Filter`, and `Log4jLogger`. Integration modules isolate interoperability concerns from the runtime engine, improving maintainability and reducing unnecessary subsystem dependencies.

#### SOLID Findings:

| Finding | Type | Explanation | Evidence | Location |
|---|---|---|---|---|
| Open/Closed Principle through Plugin System | Architectural Strength | The plugin architecture allows appenders, layouts, and filters to be extended without modifying existing runtime components. Modules such as `log4j-layout-template-json` integrate through extension points while remaining decoupled from the internal logging pipeline. | `org.apache.logging.log4j.core.config.plugins.Plugin`, C3 Plugin System component, and `JsonTemplateLayout` integration through the Layout SPI. | `log4j-core` → Plugin System |
| API/Core separation improves modular extensibility | Architectural Strength | `log4j-api` defines the public logging abstractions while `log4j-core` provides the runtime implementation. Peripheral modules integrate primarily through APIs and SPI contracts rather than direct runtime modification. | Dependency analysis artifact `architecture_handoff_packet.md`; approximately 816 import edges between `log4j-core` and `log4j-api`; C3 Logger API and `LoggerContext` components. | Relationship between `log4j-api` and `log4j-core` |
| Single Responsibility Principle trade-off in `LoggerContext` | Architectural Trade-off | `LoggerContext` coordinates runtime state, lifecycle management, configuration handling, and reconfiguration workflows. Centralized coordination simplifies runtime management but increases component complexity. | `org.apache.logging.log4j.core.LoggerContext`; C3 `LoggerContext` and Configuration components. | `log4j-core` → `LoggerContext` |
| Adapter-based integration supports Interface Segregation | Architectural Strength | The `log4j-slf4j2-impl` module isolates SLF4J interoperability concerns into dedicated adapter components, preventing external logging abstractions from leaking into runtime internals. | `Log4jLogger`, `Log4jLoggerFactory`, and `Log4jServiceProvider`; C3 adapter components in `log4j-slf4j2-impl`. | `log4j-slf4j2-impl` |

---

## Architectural Characteristics

### Quality Attributes Supported by the Architecture

#### Characteristic 1 - Extensibility
- **Definition:** The ability of the system to support new functionality without requiring major modifications to existing components.
- **How Supported:** Log4j2 supports extensibility through its plugin-based architecture, SPI extension points, and modular separation between `log4j-api` and `log4j-core`. Components such as layouts, appenders, and adapters can be added independently through the plugin registration and interface-based integration.
- **Evidence:** `Plugin.java` extension mechanism allows modules such as `log4j-layout-template-json` to integrate with the Layout SPI without modifying `log4j-core`.

#### Characteristic 2 - Interoperability
- **Definition:** The ability of the architecture to interact with external frameworks, APIs, and infrastructure systems.
- **How Supported:** Log4j2 isolates interoperability concerns to dedicated adapter and integration modules. External logging frameworks communicate with the system through bridge components rather than coupling to runtime internals.
- **Evidence:** `log4j-slf4j2-impl` module adapts SLF4J 2 API calls into `log4j-api` through components such as `Log4jLogger` and `Log4jServiceProvider`.

#### Characteristic 3 - Maintainability
- **Definition:** The ability of the system to support modification, extension, and long-term evolution/support with minimal impact on existing components.
- **How Supported:** Log4j2 separates API abstractions, runtime implementations, adapters, and extension modules into distinct `Maven artifacts`. Components communicate primarily through interfaces, SPIs, and plugin contracts, reducing direct subsystem dependency.
- **Evidence:** The separation between `log4j-api`, `log4j-core`, `log4j-layout-template-json`, `log4j-slf4j2-impl`, and `log4j-jdbc-dbcp2` isolates responsibilities into dedicated modules connected through APIs and SPIs. This modularization allows features such as JSON layouts, SLF4J adaptation, and JDBC connection pooling to evolve independently without modifying the primary runtime pipeline.

#### Characteristic 4 - Performance and Scalability
- **Definition:** The ability of the system to efficiently process increased workloads while minimizing runtime overhead.
- **How Supported:** Log4j2 uses asynchronous logging, pooled resource management, and low-allocation serialization mechanisms to reduce runtime overhead and improve throughput under high logging loads.
- **Evidence:** Async Logger supports asynchronous event-processing inside `log4j-core`, while `JsonWriter` in `log4j-layout-template-json` lowers allocation overhead during JSON serialization. The `PoolingDriverConnectionSource` in `log4j-jdbc-dbcp2` reduces database connection acquisition costs through connection pooling.

### Coupling and Cohesion Metrics (Optional)

Dependency analysis identified approximately 816 cross-module import relationships between `log4j-api` and `log4j-core`, confirming that the API/Core boundary represents the central architectural dependency within the selected scope.

At component level, the architecture generally demonstrates high cohesion. Components such as `Appender`, `Layout`, `Filter`, and `Log4jLogger` maintain focused responsibilities and interact primarily through clearly defined interfaces and SPIs. Peripheral modules such as `log4j-layout-template-json` and `log4j-slf4j2-impl` remain relatively loosely coupled because they integrate through extension points rather than direct runtime modification.

| Metric | Value | Assessment |
|--------|-------|------------|
| API/Core Import Coupling| 816 import edges | High but expected due to implementation relationship |
| Component Cohesion | High | Most components maintain focused responsibilities |
| Tightly Coupled Pairs | log4j-api ↔ log4j-core | Central architectural dependency |
| Plugin-Based Extension Points | Multiple SPI interfaces | Supports low coupling for extensions |

The dependency structure reflects a hub-and-spoke architecture centered around `log4j-core`, while peripheral modules integrate primarily through stable interfaces, adapters, and SPI extension points rather than direct runtime modification.

---

## Summary

The selected Log4j2 modules demonstrate a modular and extensible architecture centered around the separation between `log4j-api` and `log4j-core`. The architecture strongly supports extensibility through plugin-based components, SPI-driven integration mechanisms, and adapter modules such as `log4j-layout-template-json`, `log4j-slf4j2-impl`, and `log4j-jdbc-dbcp2`.

The component-level analysis demonstrates generally strong alignment with several SOLID principles, particularly Open/Closed Principle and Interface Segregation Principle. The architecture also demonstrates strong modular separation between API abstractions, runtime implementations, and extension modules through the use of SPIs, adapters, and plugin-based integration. The dependency analysis and component diagrams indicate that extensibility is achieved primarily through stable interfaces, plugin registration mechanisms, and adapter-based integration rather than direct modification of runtime components. Some architectural trade-offs remains present, especially in runtime coordination components such as `LoggerContext`, where centralized management increases component responsibility and complexity in exchange for simpler runtime orchestration.

Overall, the analyzed architecture demonstrates strong modular decomposition, high component cohesion, and controlled coupling around the API/Core boundary while maintaining extensibility, interoperability, maintainability, and runtime performance across the selected scope.

---
