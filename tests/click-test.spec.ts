// tests/click-test.spec.ts
import { test, expect } from '@playwright/test';

test('Ctrl+K opens search', async ({ page }) => {
  await page.goto('https://aldo-f.github.io/');
  
  // Wait for page to load
  await page.waitForLoadState('networkidle');
  
  // Click Ctrl+K
  await page.keyboard.press('Control+k');
  
  // Wait for search to open - check for search panel with slide-down animation
  // Material theme adds 'md-search__inner' when search is active
  const searchInput = page.getByRole('textbox', { name: /search/i });
  await expect(searchInput).toBeVisible();
});
