"""Top-level stub package for mkdocs_pivot_table.
Exports version, parser, HTML builder, ID generator, and dummy plugin.
"""

__version__ = "0.0.0-stub"

from plugins.mkdocs_pivot_table.plugin import (
    PivotTablePlugin,
    _parse_pivot_table,
    _build_table_html,
    _generate_table_id,
)

__all__ = [
    "__version__",
    "PivotTablePlugin",
    "_parse_pivot_table",
    "_build_table_html",
    "_generate_table_id",
]
