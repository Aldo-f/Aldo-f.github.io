import pytest
from playwright.sync_api import Page, expect


def test_404_dungeon_page_loads(page: Page):
    # Test the 404 page in Dutch (the site is served at /nl/404.html)
    page.goto("http://localhost:8000/nl/404.html")
    # Verify the page loads
    expect(page.locator("#dungeon-scene")).to_be_visible()
    # Verify absolute asset URLs (e.g. /assets/css/chat.css) are present
    html = page.content()
    assert "/assets/" in html, "Asset URLs should be absolute"
    # Verify the title and narrative
    expect(page.locator("#dungeon-title-text")).to_contain_text("The 404 Dungeon")


def test_404_dungeon_en(page: Page):
    page.goto("http://localhost:8000/404.html")
    expect(page.locator("#dungeon-scene")).to_be_visible()
    html = page.content()
    assert "/assets/" in html, "Asset URLs should be absolute"
    expect(page.locator("#dungeon-title-text")).to_contain_text("The 404 Dungeon")


@pytest.mark.parametrize(
    "width,height",
    [
        (320, 640),  # mobile
        (768, 1024),  # tablet
        (1280, 800),  # desktop
    ],
)
def test_404_dungeon_responsive(page: Page, width: int, height: int):
    """Test dungeon game renders at different viewport widths."""
    page.set_viewport_size({"width": width, "height": height})
    page.goto("http://localhost:8000/404.html")
    expect(page.locator("#dungeon-scene")).to_be_visible()
    expect(page.locator("#dungeon-title-text")).to_be_visible()
    # Should have at least one choice button
    expect(page.locator(".choice-btn").first).to_be_visible()
