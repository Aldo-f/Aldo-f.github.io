import pytest
from playwright.sync_api import Page, expect

def test_404_dungeon_page_loads(page: Page):
    # Test the 404 page in Dutch (the site is served at /nl/404-pagina/)
    page.goto("http://localhost:8000/nl/404-pagina/")
    # Verify the page loads
    expect(page.locator("#dungeon-scene")).to_be_visible()
    # Verify absolute asset URLs (e.g. /assets/css/chat.css) are present
    html = page.content()
    assert "/assets/" in html, "Asset URLs should be absolute"
    # Verify the title and narrative
    expect(page.locator("#dungeon-title-text")).to_contain_text("The 404 Dungeon")