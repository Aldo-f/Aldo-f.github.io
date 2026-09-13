"""Wrapper module to expose the plugin implementation for tests."""

from plugins.mkdocs_pivot_table.plugin import (
    PivotTablePlugin,
    _parse_pivot_table,
    _build_table_html,
    _generate_table_id,
)
