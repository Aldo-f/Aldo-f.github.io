"""Verify confusion stat actually changes during gameplay."""
import pytest
from playwright.sync_api import Page, expect


def test_confusion_changes(page: Page):
    """Choosing the torch should increase confusion from 0 to 1."""
    page.goto("http://localhost:8000/404.html")
    page.wait_for_load_state("networkidle")
    
    # Initial state
    conf_el = page.locator("#dungeon-conf")
    hp_el = page.locator("#dungeon-hp")
    expect(conf_el).to_have_text("0")
    expect(hp_el).to_have_text("3")
    
    # Click "Examine the torch"
    torch_btn = page.locator("button.choice-btn").first
    torch_btn.click()
    page.wait_for_timeout(200)
    
    # Confusion should now be 1, HP should be 2
    expect(conf_el).to_have_text("1")
    expect(hp_el).to_have_text("2")
    
    # Back to start - confusion stays at 1 because start has statDelta=0
    back_btn = page.locator("button.choice-btn").first
    back_btn.click()
    page.wait_for_timeout(200)
    
    # Confusion stays at 1 (start node has statDelta=0)
    expect(conf_el).to_have_text("1")
    expect(hp_el).to_have_text("2")


def test_escape_path(page: Page):
    """Following corridor -> slime_help should show escape button."""
    page.goto("http://localhost:8000/404.html")
    page.wait_for_load_state("networkidle")
    
    # Enter corridor
    corridor_btn = page.locator("button.choice-btn").last
    corridor_btn.click()
    page.wait_for_timeout(200)
    
    # Accept slime help
    accept_btn = page.locator("button.choice-btn").first
    accept_btn.click()
    page.wait_for_timeout(200)
    
    # Escape button should be visible (no choices at slime_help)
    escape_btn = page.locator("#escape-btn")
    expect(escape_btn).to_be_visible()
    
    # Confusion should be 0 (slime_help has statDelta -1)
    expect(page.locator("#dungeon-conf")).to_have_text("0")
    expect(page.locator("#dungeon-hp")).to_have_text("3")