# mkdocs-pivot-table

A lightweight MkDocs plugin that renders interactive, sortable, and filterable comparison tables directly in your documentation.

## Features

- **Sortable columns** – Click any column header to sort ascending/descending
- **Drag-to-reorder** – Drag column headers to change order
- **State preservation** – View state is saved to the URL (shareable links)
- **Reset button** – Restore the original sorted order
- **Zero config** – Works out of the box with minimal setup

## Installation

Add to your `mkdocs.yml`:

```yaml
plugins:
  - mkdocs_pivot_table
```

Then enable the plugin in your site config:

```yaml
# mkdocs.yml
plugins:
  - mkdocs_pivot_table
```

## Usage

Place a table in your markdown using the `[pivot-table]` wrapper:

```markdown
[pivot-table]

| Feature  | npm  | pnpm | Bun     | pip  | uv     |
| -------- | ---- | ---- | ------- | ---- | ------ |
| Speed    | Slow | Fast | Fastest | Slow | Fast   |
| Dedup    | No   | Yes  | Yes     | No   | Yes    |
| Runtime  | No   | Yes  | Yes     | No   | Yes    |
| Maturity | High | High | Medium  | High | Medium |

[reset-pivot]
```

The table will render as an interactive `<table>` with sorting and dragging enabled.

## Requirements

- MkDocs ≥ 1.5.0
- Beautiful Soup 4
- PyJS (for mermaid.js integration)

## License

MIT
