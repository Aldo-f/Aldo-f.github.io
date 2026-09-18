import json
import types
import sys
import os
from pathlib import Path

import pytest
# Ensure the project root is on sys.path for imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Import the hook module
from hooks import abbreviations as abbrev

# Helper to create a simple abbreviation markdown file
def _create_abbreviation_file(path: Path, abbreviation: str, title: str, category: str, definition: str) -> None:
    content = f"""---
abbreviation: {abbreviation}
---
## {title}
**Category:** {category}

**Definition:** {definition}
"""
    path.write_text(content, encoding="utf-8")

@pytest.fixture(autouse=True)
def setup_abbrev_dir(tmp_path, monkeypatch):
    # Create a temporary abbreviation directory
    abbrev_dir = tmp_path / "abbreviations"
    abbrev_dir.mkdir()
    # Point the module's ABBREVIATIONS_DIR to this temporary directory
    monkeypatch.setattr(abbrev, "ABBREVIATIONS_DIR", abbrev_dir)
    return abbrev_dir

def test_parse_abbreviation_valid(setup_abbrev_dir):
    # Create a valid abbreviation file (DRY.md)
    file_path = setup_abbrev_dir / "DRY.md"
    _create_abbreviation_file(
        file_path,
        abbreviation="DRY",
        title="Don\'t Repeat Yourself",
        category="principle",
        definition="Avoid duplication in code.",
    )
    result = abbrev._parse_abbreviation(file_path)
    assert result is not None
    assert result["abbreviation"] == "DRY"
    answers = result["answers"]
    assert isinstance(answers, list) and len(answers) == 1
    ans = answers[0]
    assert ans["title"] == "Don't Repeat Yourself"
    assert ans["categories"] == ["principle"]
    assert ans["definition"] == "Avoid duplication in code."

def test_parse_abbreviation_template(setup_abbrev_dir):
    # Create a template file that should be ignored (NEW_ABBREVIATION)
    tmpl_path = setup_abbrev_dir / "TEMPLATE.md"
    _create_abbreviation_file(
        tmpl_path,
        abbreviation="NEW_ABBREVIATION",
        title="Template",
        category="template",
        definition="Placeholder",
    )
    result = abbrev._parse_abbreviation(tmpl_path)
    assert result is None

def test_load_abbreviations(setup_abbrev_dir):
    # Create two files: one valid, one template
    valid_path = setup_abbrev_dir / "YAGNI.md"
    _create_abbreviation_file(
        valid_path,
        abbreviation="YAGNI",
        title="You Aren't Gonna Need It",
        category="principle",
        definition="Do not implement features until they are needed.",
    )
    tmpl_path = setup_abbrev_dir / "TEMPLATE.md"
    _create_abbreviation_file(
        tmpl_path,
        abbreviation="NEW_ABBREVIATION",
        title="Template",
        category="template",
        definition="Placeholder",
    )
    entries = abbrev._load_abbreviations()
    # Should contain only the valid entry
    assert len(entries) == 1
    assert entries[0]["abbreviation"] == "YAGNI"

class DummyPage:
    def __init__(self, title):
        self.meta = {"title": title}

def test_on_page_markdown_injects_script(monkeypatch):
    # Prepare a dummy abbreviation list
    dummy_data = [{"abbreviation": "DRY", "answers": []}]
    monkeypatch.setattr(abbrev, "_abbreviations", dummy_data, raising=False)
    page = DummyPage(abbrev.PAGE_TITLE)
    markdown = "# Content"
    out = abbrev.on_page_markdown(markdown, page, None, None)
    # The output should start with the script tag and contain the JSON data
    assert out.startswith("<script>window.ABBREVIATIONS = ")
    # The original markdown should be present after the injected assets
    assert markdown in out
    # Verify JSON content matches dummy_data
    json_part = out.split("<script>window.ABBREVIATIONS = ", 1)[1].split(";</script>", 1)[0]
    parsed = json.loads(json_part)
    assert parsed == dummy_data


def test_on_page_markdown_injects_material_design_assets(monkeypatch):
    """TDD: Material Design assets must be injected for proper rendering."""
    dummy_data = [{"abbreviation": "DRY", "answers": []}]
    monkeypatch.setattr(abbrev, "_abbreviations", dummy_data, raising=False)
    page = DummyPage(abbrev.PAGE_TITLE)
    markdown = "# Content"
    out = abbrev.on_page_markdown(markdown, page, None, None)
    # Must inject the CSS and JS assets as absolute paths
    assert '/assets/css/abbreviations.css' in out
    assert '/assets/javascripts/abbreviations.js' in out
    # Must inject the data for the client-side UI
    assert 'window.ABBREVIATIONS' in out

def test_on_post_build_writes_json(tmp_path, monkeypatch):
    # Set up a temporary site directory
    site_dir = tmp_path / "site"
    site_dir.mkdir()
    # Dummy config object with site_dir attribute
    config = types.SimpleNamespace(site_dir=str(site_dir))
    # Prepare abbreviations data
    dummy_data = [{"abbreviation": "DRY", "answers": []}]
    monkeypatch.setattr(abbrev, "_abbreviations", dummy_data, raising=False)
    # Run the post-build hook
    abbrev.on_post_build(config=config)
    # Verify that the JSON file was written
    output_path = site_dir / abbrev.OUTPUT_FILE
    assert output_path.is_file()
    content = json.loads(output_path.read_text(encoding="utf-8"))
    assert content == dummy_data
