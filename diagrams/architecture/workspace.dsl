workspace "Apache Log4j2 Architecture" "C4 model for the Apache Log4j2 modules included in the project analysis." {

    !impliedRelationships false

    model {
        app = softwareSystem "Applications / Libraries" "Java applications that emit log calls" {
            tags "External"
        }

        slf4jApi = softwareSystem "SLF4J 2 API" "Logging facade bridged to Log4j2" {
            tags "External"
        }

        fileSystem = softwareSystem "File System" "Log file destination" {
            tags "External"
        }

        console = softwareSystem "Console" "Standard output / error" {
            tags "External"
        }

        networkEndpoints = softwareSystem "Network Endpoints" "Syslog / HTTP / SMTP" {
            tags "External"
        }

        jdbcDatabases = softwareSystem "JDBC Databases" "Relational database destinations" {
            tags "External,Database"
        }

        logAggregation = softwareSystem "Log Aggregation / Monitoring" "Downstream observability stacks" {
            tags "External"
        }

        log4j2 = softwareSystem "Apache Log4j2" "Java logging framework in scope of this analysis" {
            log4jApi = container "log4j-api" "Public logging API used by applications and adapters" "Java" {
                statusLogger = component "StatusLogger" "Internal status diagnostics"
                loggerFactory = component "LoggerFactory / Provider" "Provider discovery mechanism"
                loggerApi = component "Logger API" "Public logging interface"
                logEventContract = component "LogEvent Contract" "Log event abstraction"
                logManager = component "LogManager" "Logger creation and lookup"
                extendedLogger = component "ExtendedLogger" "Extended logging operations"
                messageFactory = component "MessageFactory" "Structured message creation"
                message = component "Message" "Log message abstraction"
                simpleLogger = component "SimpleLogger" "Fallback logging implementation"
            }

            log4jCore = container "log4j-core" "Logging implementation, configuration, filters, appenders, runtime pipeline" "Java" {
                loggerContext = component "LoggerContext" "Runtime state and lifecycle manager"
                configuration = component "Configuration" "Configuration loading and management"
                loggerConfig = component "LoggerConfig" "Log event routing rules"
                appender = component "Appender" "Log event output destination"
                filter = component "Filter" "Log event filtering rules"
                pluginSystem = component "Plugin System" "SPI-based extension framework"
                layout = component "Layout" "Log event formatting engine"
                asyncLogger = component "Async Logger" "Asynchronous event processing"
            }

            jsonLayout = container "log4j-layout-template-json" "JSON layout templates for structured output" "Java" {
                jsonTemplateLayout = component "JsonTemplateLayout" "JSON layout implementation"
                templateResolver = component "TemplateResolver" "JSON template resolution engine"
                eventResolverRegistry = component "EventResolver Registry" "Event field resolver registry"
                builtInEventResolvers = component "Built-in EventResolvers" "Standard field extractors"
                jsonWriter = component "JsonWriter" "Low-allocation JSON serializer"
            }

            slf4jImpl = container "log4j-slf4j2-impl" "Adapter bridging SLF4J 2 calls to Log4j2 API" "Java" {
                mdcAdapter = component "Log4jMDCAdapter" "SLF4J MDC bridge"
                serviceProvider = component "Log4jServiceProvider" "SLF4J ServiceLoader provider"
                slf4jLoggerFactory = component "Log4jLoggerFactory" "SLF4J logger factory adapter"
                log4jLoggerAdapter = component "Log4jLogger" "SLF4J-to-Log4j adapter"
                markerFactory = component "Log4jMarkerFactory" "SLF4J marker bridge"
            }

            jdbcDbcp2 = container "log4j-jdbc-dbcp2" "JDBC appender integration writing log events to databases" "Java, Apache DBCP2" {
                poolingConnectionSource = component "PoolingDriverConnectionSource" "Provides pooled JDBC connections" "ConnectionSource SPI"
                commonsDbcpPool = component "Commons DBCP Pool" "Manages JDBC connection pooling" "Connection Pool"
            }
        }

        app -> log4j2 "logs via Logger API"
        slf4jApi -> log4j2 "bridged by log4j-slf4j2-impl"
        log4j2 -> fileSystem "writes log events"
        log4j2 -> console "writes log events"
        log4j2 -> networkEndpoints "writes log events"
        log4j2 -> jdbcDatabases "writes log events"
        log4j2 -> logAggregation "forwards logs"

        app -> log4jApi "calls Logger API"
        slf4jApi -> slf4jImpl "discovered via ServiceLoader"
        slf4jImpl -> log4jApi "delegates SLF4J calls to Logger API"
        log4jCore -> log4jApi "implements logging abstractions of"
        log4jCore -> jsonLayout "formats events via JSON Layout SPI"
        log4jCore -> jdbcDbcp2 "obtains pooled JDBC connections via"
        log4jCore -> fileSystem "writes log events"
        log4jCore -> console "writes log events"
        log4jCore -> networkEndpoints "writes log events"
        jdbcDbcp2 -> jdbcDatabases "writes log events over pooled JDBC connections"
        log4jCore -> logAggregation "forwards logs"

        loggerContext -> configuration "loads configuration from"
        configuration -> loggerConfig "creates logging configuration"
        loggerConfig -> appender "routes log events to"
        appender -> layout "formats log events using"
        loggerConfig -> filter "applies filtering rules via"
        pluginSystem -> appender "extends appenders via SPI"
        pluginSystem -> layout "extends layouts via SPI"
        pluginSystem -> filter "extends filters via SPI"
        asyncLogger -> appender "dispatches events asynchronously to"
        appender -> logAggregation "forwards logs to"
        log4jApi -> loggerContext "creates and manages logger contexts through"
        layout -> jsonLayout "invokes Layout SPI implemented by"
        appender -> jdbcDbcp2 "obtains JDBC connections through"
        appender -> fileSystem "writes log events"
        appender -> console "writes log events"
        appender -> networkEndpoints "writes log events"
        appender -> jdbcDatabases "writes log events through JDBC"

        app -> logManager "requests logger via"
        logManager -> loggerFactory "resolves provider using"
        loggerFactory -> loggerApi "creates logger instance"
        loggerApi -> extendedLogger "extends API with"
        loggerApi -> messageFactory "builds messages via"
        messageFactory -> message "creates Message instances"
        loggerApi -> logEventContract "emits log events"
        logManager -> simpleLogger "fallback when no core available"
        logManager -> statusLogger "publishes internal diagnostics to"
        slf4jImpl -> logManager "obtains loggers through"
        log4jCore -> loggerApi "implements logging abstractions exposed by"

        log4jCore -> jsonTemplateLayout "invokes Layout SPI on"
        jsonTemplateLayout -> templateResolver "resolves template using"
        templateResolver -> eventResolverRegistry "looks up field resolvers in"
        eventResolverRegistry -> builtInEventResolvers "returns resolver implementations from"
        builtInEventResolvers -> log4jApi "reads LogEvent fields from"
        jsonTemplateLayout -> jsonWriter "writes JSON output through"

        slf4jApi -> serviceProvider "discovers provider through ServiceLoader"
        serviceProvider -> slf4jLoggerFactory "provides logger factory"
        slf4jLoggerFactory -> log4jLoggerAdapter "creates adapter logger"
        log4jLoggerAdapter -> log4jApi "delegates SLF4J Logger calls to"
        slf4jApi -> markerFactory "routes marker operations through"
        slf4jApi -> mdcAdapter "routes MDC operations through"

        log4jCore -> poolingConnectionSource "requests JDBC connections from"
        poolingConnectionSource -> commonsDbcpPool "manages pooled connections via"
        commonsDbcpPool -> jdbcDatabases "opens JDBC connections to"
        coreWritesToJdbcDatabases = log4jCore -> jdbcDatabases "writes log events to"
    }

    views {
        systemContext log4j2 "c1-system-context" {
            title "C1 System Context Diagram - Apache Log4j2"
            include *
            autoLayout lr
        }

        container log4j2 "c2-container" {
            title "C2 Container Diagram - Apache Log4j2"
            include *
            exclude coreWritesToJdbcDatabases
            autoLayout lr
        }

        component log4jCore "c3-log4j-core" {
            title "C3 Component Diagram - log4j-core"
            include loggerContext configuration loggerConfig appender filter pluginSystem layout asyncLogger
            include log4jApi jsonLayout jdbcDbcp2 fileSystem console networkEndpoints jdbcDatabases logAggregation
            autoLayout lr
        }

        component log4jApi "c3-log4j-api" {
            title "C3 Component Diagram - log4j-api"
            include statusLogger loggerFactory loggerApi logEventContract logManager extendedLogger messageFactory message simpleLogger
            include app slf4jImpl log4jCore
            autoLayout lr
        }

        component jsonLayout "c3-log4j-layout-template-json" {
            title "C3 Component Diagram - log4j-layout-template-json"
            include jsonTemplateLayout templateResolver eventResolverRegistry builtInEventResolvers jsonWriter
            include log4jCore log4jApi
            autoLayout lr
        }

        component slf4jImpl "c3-log4j-slf4j2-impl" {
            title "C3 Component Diagram - log4j-slf4j2-impl"
            include mdcAdapter serviceProvider slf4jLoggerFactory log4jLoggerAdapter markerFactory
            include slf4jApi log4jCore log4jApi
            autoLayout lr
        }

        component jdbcDbcp2 "c3-log4j-jdbc-dbcp2" {
            title "C3 Component Diagram - log4j-jdbc-dbcp2"
            include poolingConnectionSource commonsDbcpPool
            include log4jCore jdbcDatabases
            autoLayout lr
        }

        container log4j2 "module-dependency-overview" {
            title "Module Dependency Overview - Apache Log4j2"
            include log4jApi log4jCore jsonLayout slf4jImpl jdbcDbcp2
            autoLayout lr
        }

        styles {
            element "Software System" {
                background "#1168BD"
                color "#FFFFFF"
                shape RoundedBox
            }

            element "Container" {
                background "#438DD5"
                color "#FFFFFF"
                shape RoundedBox
            }

            element "Component" {
                background "#85BBF0"
                color "#000000"
                shape RoundedBox
            }

            element "External" {
                background "#999999"
                color "#FFFFFF"
            }

            element "Database" {
                shape Cylinder
            }
        }
    }
}
