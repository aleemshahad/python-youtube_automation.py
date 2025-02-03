import re
import time
from playwright.sync_api import Playwright, sync_playwright, expect

def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)  # Set to True for production
    context = browser.new_context()
    
    try:
        page = context.new_page()
        
        # Navigate to YouTube
        page.goto("https://www.youtube.com/")
        expect(page).to_have_title("YouTube")

        # Search for video
        search_box = page.get_by_role("combobox", name="Search")
        search_box.click()
        search_box.fill("Complete Guide to Airdrop Eligibility Form Filling TomMarket")
        page.keyboard.press("Enter")
        
        # Wait for search results
        expect(page.get_by_text("Search results")).to_be_visible()
        
        # Open video
        video = page.get_by_title(re.compile("Complete Guide to Airdrop", exact=False))
        video.first.click()
        
        # Wait for video player
        expect(page.locator(".html5-video-player")).to_be_visible()
        time.sleep(1)  # Consider using page.wait_for_timeout(120000) instead

        # Navigate to channel
        page.get_by_role("link", name="Aleem Shahzad", exact=True).click()
        expect(page).to_have_title("Aleem Shahzad - YouTube")
        
        # Click Videos tab
        page.locator("#tabsContent").get_by_text("Videos").click()
        expect(page.locator("ytd-grid-renderer")).to_be_visible()
        
        # Watch first video
        page.locator("ytd-grid-video-renderer").first.click()
        time.sleep(120)

    finally:
        context.close()
        browser.close()

if __name__ == "__main__":
    with sync_playwright() as playwright:
        run(playwright)