import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'mkdocs_pivot_table'))

import pytest
import re
from mkdocs_pivot_table.mkdocs_pivot_table import (
    _parse_pivot_table,
    _build_table_html,
    _generate_table_id,
    PIVOT_PATTERN,
    PivotTablePlugin,
)


class TestParsePivotTable:
    def test_simple_table(self):
        md = """| A | B | C |
|---|---|---|
| 1 | 2 | 3 |
| 4 | 5 | 6 |"""
        headers, rows = _parse_pivot_table(md)
        assert headers == ['A', 'B', 'C']
        assert rows == [['1', '2', '3'], ['4', '5', '6']]

    def test_table_with_extra_spaces(self):
        md = """| Feature | npm | pnpm |
|-------|-----|------|
| Speed | Slow | Fast |"""
        headers, rows = _parse_pivot_table(md)
        assert headers == ['Feature', 'npm', 'pnpm']
        assert rows == [['Speed', 'Slow', 'Fast']]

    def test_empty_table_returns_empty(self):
        headers, rows = _parse_pivot_table("")
        assert headers == []
        assert rows == []

    def test_single_row(self):
        md = """| A | B |
|---|---|
| x | y |"""
        headers, rows = _parse_pivot_table(md)
        assert headers == ['A', 'B']
        assert rows == [['x', 'y']]

    def test_multiline_content(self):
        md = """| Tool | Note |
|------|------|
| npm  | slow |
| pnpm | fast |"""
        headers, rows = _parse_pivot_table(md)
        assert headers == ['Tool', 'Note']
        assert rows == [['npm', 'slow'], ['pnpm', 'fast']]


class TestBuildTableHtml:
    def test_basic_output(self):
        headers = ['Tool', 'Speed']
        rows = [['npm', 'Slow'], ['pnpm', 'Fast']]
        html = _build_table_html(headers, rows, 'pivot-001')
        assert 'id="pivot-001"' in html
        assert 'class="pivot-table"' in html
        assert '<th' in html and 'Tool' in html
        assert '<td' in html and 'Slow' in html
        assert 'draggable="true"' in html

    def test_escapes_html(self):
        headers = ['A', '<script>']
        rows = [['x', '<b>y</b>']]
        html = _build_table_html(headers, rows, 'pivot-test')
        assert '<script>' in html
        assert '<b>y</b>' in html


class TestPivotPattern:
    def test_matches_wrapped_table(self):
        md = "[pivot-table]\n| A | B |\n|---|---|\n| 1 | 2 |\n[/pivot-table]"
        match = PIVOT_PATTERN.search(md)
        assert match is not None
        assert '| A | B |' in match.group(1)

    def test_does_not_match_without_markers(self):
        md = "| A | B |\n|---|---|\n| 1 | 2 |"
        match = PIVOT_PATTERN.search(md)
        assert match is None

    def test_does_not_match_partial_markers(self):
        md = "[pivot-table]\n| A | B |\n|---|---|\n| 1 | 2 |"
        match = PIVOT_PATTERN.search(md)
        assert match is None

    def test_matches_multiple(self):
        md = "[pivot-table]\n|A|B|\n|---|---|\n|1|2|\n[/pivot-table]\ntext\n[pivot-table]\n|X|Y|\n|---|---|\n|3|4|\n[/pivot-table]"
        matches = list(PIVOT_PATTERN.finditer(md))
        assert len(matches) == 2


class TestGenerateTableId:
    def test_generates_unique_ids(self):
        ids = {_generate_table_id(i) for i in range(10)}
        assert len(ids) == 10

    def test_format(self):
        assert _generate_table_id(0) == 'pivot-000'
        assert _generate_table_id(99) == 'pivot-099'


class TestPlugin:
    def test_on_config_initializes(self):
        plugin = PivotTablePlugin()
        config = {}
        result = plugin.on_config(config)
        assert result == config
        assert plugin._has_table is False

    def test_on_page_markdown_replaces_table(self):
        plugin = PivotTablePlugin()
        plugin.on_config({})
        md = "[pivot-table]\n| A | B |\n|---|---|\n| 1 | 2 |\n[/pivot-table]"
        class FakePage:
            file = type('obj', (), {'src_path': 'test.md'})()
        result, tables = plugin._process_markdown(md, FakePage())
        assert 'pivot-table' in result
        assert len(tables) == 1
        assert tables[0]['headers'] == ['A', 'B']

    def test_on_page_markdown_no_table_returns_original(self):
        plugin = PivotTablePlugin()
        plugin.on_config({})
        md = "Just some text"
        class FakePage:
            file = type('obj', (), {'src_path': 'test.md'})()
        result, tables = plugin._process_markdown(md, FakePage())
        assert result == md
        assert tables == []

    def test_on_page_markdown_multiple_tables(self):
        plugin = PivotTablePlugin()
        plugin.on_config({})
        md = "[pivot-table]\n| A | B |\n|---|---|\n| 1 | 2 |\n[/pivot-table]\n[pivot-table]\n| X | Y |\n|---|---|\n| 3 | 4 |\n[/pivot-table]"
        class FakePage:
            file = type('obj', (), {'src_path': 'test.md'})()
        result, tables = plugin._process_markdown(md, FakePage())
        assert len(tables) == 2


if __name__ == '__main__':
    pytest.main([__file__, '-v'])