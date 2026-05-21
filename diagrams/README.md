# Diagrams

This directory contains the diagrams required for the Software Architecture report.

Diagrams are organized according to the C4 model levels:

* **context/**
  Contains the system context diagram (Level 1)

* **container/**
  Contains the container diagram (Level 2)

* **components/**
  Contains component diagrams (Level 3), one Mermaid file per scoped module:
  * [`log4j-api.mmd`](components/log4j-api.mmd)
  * [`log4j-core.mmd`](components/log4j-core.mmd)
  * [`log4j-layout-template-json.mmd`](components/log4j-layout-template-json.mmd)
  * [`log4j-slf4j2-impl.mmd`](components/log4j-slf4j2-impl.mmd)
  * [`log4j-jdbc-dbcp2.mmd`](components/log4j-jdbc-dbcp2.mmd)
  * [`overview.mmd`](components/overview.mmd)

Each diagram is referenced in the Architecture report and supported by corresponding explanations.
