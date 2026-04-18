# Git Workflow Guide

Guidelines for commits and contributions to the project.

---

## Commit Message Conventions

Use a prefix to indicate the type of change:

### Prefixes

| Prefix | Usage | Example |
|--------|-------|---------|
| `log:` | Journal updates | `log: Add week 1 activities - Filippo` |
| `docs:` | Report updates (overview, design, architecture) | `docs: Add dependency analysis to design report` |
| `analysis:` | Analysis files (dependencies, metrics, patterns) | `analysis: Add co-change analysis results` |
| `diagrams:` | C4 diagrams and visualizations | `diagrams: Add container diagram for Log4j2` |
| `refs:` | References, links, papers | `refs: Add design patterns documentation link` |
| `tools:` | Scripts and analysis tools | `tools: Add dependency extraction script` |
| `chore:` | General maintenance, setup | `chore: Initialize project structure` |

---

## Examples

```bash
# Logging activities
git commit -m "log: Document analysis of Logger hierarchy - Davide"

# Writing report sections
git commit -m "docs: Complete software design dependencies section"

# Adding analysis results
git commit -m "analysis: Add metrics for top 10 most coupled modules"

# Adding diagrams
git commit -m "diagrams: Create C3 component diagram for core module"

# Adding references
git commit -m "refs: Add SOLID principles paper link"
```

---

## Commit Frequency

- **Individual contributions:** Commit frequently as you complete small tasks
- **Journal updates:** Can be individual commits or bundled
- **Reports:** Commit when significant sections are completed
- **Push to remote:** At least every 2 weeks (as per project requirements)
