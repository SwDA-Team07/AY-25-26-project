# Diagrams

The Architecture C4 diagrams are defined in [`architecture/workspace.dsl`](architecture/workspace.dsl).

After modifying the Structurizr DSL workspace, the SVG diagrams were exported from `diagrams/architecture/` with:

```sh
structurizr export -workspace workspace.dsl -format svg -output export
```

The generated SVG files are stored in [`architecture/export/`](architecture/export/) and included by `docs/architecture.md`.
