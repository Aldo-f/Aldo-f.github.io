#!/usr/bin/env python3
"""E2E: aldo-f.github.io chat -> rag.aldof.duckdns.org (spec 005-chat-rag)."""
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()

    page.goto("https://aldo-f.github.io/")
    page.wait_for_load_state("networkidle")

    # Open chat (button id from cubic: #chat-toggle-btn)
    page.click("#chat-toggle-btn")
    page.wait_for_selector("#chat-input", timeout=5000)

    # Ask a question
    page.fill("#chat-input", "What is Blanky?")
    page.keyboard.press("Enter")

    # Wait for response bubble or error message
    page.wait_for_selector(".chat-bubble, .chat-error", timeout=15000)
    answer = page.inner_text(".chat-bubble.ai:last-of-type")
    has_sources = len(page.locator(".chat-sources").all()) > 0

    with open("/tmp/e2e_chat_result.txt", "w") as f:
        f.write(f"answer_preview={answer[:120]}\n")
        f.write(f"sources_rendered={has_sources}\n")

    browser.close()

print("E2E done; see /tmp/e2e_chat_result.txt")
