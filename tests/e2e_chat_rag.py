#!/usr/bin/env python3
"""E2E: aldo-f.github.io chat -> rag.aldof.duckdns.org (spec 005-chat-rag)."""
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.goto("https://aldo-f.github.io/")
    # Click chat button (lazy-loaded widget)
    page.wait_for_selector(".chat-button, [aria-label='Chat']", timeout=5000)
    page.click(".chat-button")
    # Type a question
    page.fill(".chat-input input, [contenteditable='true']", "What is Blanky?")
    page.click("button:has-text('Send'), .chat-send")
    # Wait for RAG response or error
    page.wait_for_selector(".chat-bubble, .chat-error", timeout=15000)
    answer = page.inner_text(".chat-bubble:last-of-type")
    has_sources = len(page.locator(".chat-sources").all()) > 0
    with open("/tmp/e2e_chat_result.txt", "w") as f:
        f.write(f"answer_preview={answer[:120]}\n")
        f.write(f"sources_rendered={has_sources}\n")
    browser.close()
print("E2E done; see /tmp/e2e_chat_result.txt")
