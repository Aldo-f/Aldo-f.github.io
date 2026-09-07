"""
mkdocs-pivot-table — Interactive sortable/filterable comparison table plugin for MkDocs.

Usage in Markdown:
    [pivot-table]
    col1 | col2 | col3
    ---- | ---- | ----
    a    | b    | c
    d    | e    | f
    [/pivot-table]
"""

__version__ = "0.1.0"

import os
import re
from bs4 import BeautifulSoup
from mkdocs.plugins import BasePlugin
from mkdocs.config.config_options import Type as PluginType


DEFAULT_ASSET_URL = "https://cdn.jsdelivr.net/npm/pivot-table-kit@0.1.0/dist/pivot-table.js"


def _escape_js(s):
    return s.replace("\\", "\\\\").replace("'", "\\'").replace("\n", "\\n")


def _generate_table_id(page_name, idx):
    return f"pivot-{page_name[:30].lower().replace(' ', '-')}-{idx}"


def _build_table_html(headers, rows, table_id):
    """Generate the static HTML skeleton for the interactive table."""
    h = [f'<div class="pivot-table-wrap" data-pivot="{table_id}">']
    h.append(f'<div class="pivot-toolbar" data-for="{table_id}">')
    h.append(f'<button class="pivot-btn" data-action="swap">⇄ Swap R/Col</button>')
    h.append(f'<button class="pivot-btn" data-action="reset">↺ Reset</button>')
    h.append(f'<span class="pivot-hint">click headers to sort · drag to reorder · state in URL</span>')
    h.append('</div>')
    h.append(f'<table id="{table_id}" class="pivot-table" border="1" cellpadding="5" style="border-collapse:collapse;font-size:0.85rem;width:100%">')
    h.append('<thead><tr>')
    for i, h_name in enumerate(headers):
        h.append(f'<th data-col="{i}">{h_name}</th>')
    h.append('</tr></thead><tbody>')
    for ri, row in enumerate(rows):
        h.append('<tr>')
        for ci, cell in enumerate(row):
            h.append(f'<td data-col="{ci}" data-row="{ri}">{cell}</td>')
        h.append('</tr>')
    h.append('</tbody></table></div>')
    return '\n'.join(h)


def _collect_pivot_blocks(output_content, page, config):
    """Scan rendered HTML for [pivot-table] ... [/pivot-table] markers and replace them."""
    soup = BeautifulSoup(output_content, 'html.parser')
    modified = False
    pivot_counter = 0

    for el in soup.find_all(string=re.compile(r'\[pivot-table\]')):
        modified = True
        pivot_counter += 1
        # Find the content between [pivot-table] and [/pivot-table]
        parent = el.parent
        start_idx = None
        end_marker = None
        for sibling in parent.children:
            if start_idx is not None and str(sibling).strip().startswith('[/pivot-table]'):
                end_marker = sibling
                break
            if start_idx is None and str(sibling).strip().startswith('[pivot-table]'):
                start_idx = sibling

    return modified, pivot_counter


def _extract_pivot_content(output_content):
    """Extract pivot table definitions from raw markdown before HTML conversion."""
    pattern = re.compile(
        r'\[pivot-table\]\s*\n(.*?)\n\s*\[/pivot-table\]',
        re.DOTALL
    )
    return pattern.findall(output_content)


def _parse_pivot_table(md_text):
    """Parse markdown pipe-table into headers and rows."""
    lines = [l.strip() for l in md_text.strip().split('\n') if l.strip()]
    if len(lines) < 2:
        return [], []
    headers = [c.strip() for c in lines[0].split('|') if c.strip()]
    # skip separator row
    rows = []
    for line in lines[2:]:
        cells = [c.strip() for c in line.split('|') if c.strip()]
        if cells:
            rows.append(cells)
    return headers, rows
