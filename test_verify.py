from playwright.sync_api import sync_playwright
import os

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        os.makedirs("/home/jules/verification/video", exist_ok=True)
        context = browser.new_context(record_video_dir="/home/jules/verification/video")
        page = context.new_page()

        print("Navigating to app...")
        page.goto("http://localhost:10000")
        page.wait_for_timeout(2000)

        print("Clicking Groceries tab on dashboard...")
        page.locator("span:has-text('Groceries')").first.click()
        page.wait_for_timeout(1000)

        print("Checking if we are on Groceries view...")
        assert page.locator("h2:has-text('Groceries')").is_visible()

        print("Adding a new item...")
        page.fill("input[placeholder='Add new item...']", "Apples")
        page.click("button:has-text('Add')")
        page.wait_for_timeout(2000)

        print("Verifying Apples is added...")
        assert page.locator("text=Apples").first.is_visible()

        print("Toggling Apples as purchased...")
        page.locator("li:has-text('Apples')").locator("div.flex.items-center").first.click()
        page.wait_for_timeout(1000)

        print("Deleting Apples...")
        page.locator("li:has-text('Apples')").locator("button").first.click()
        page.wait_for_timeout(2000)

        print("Taking screenshot...")
        page.screenshot(path="/home/jules/verification/verification.png")

        print("Navigating back to home...")
        page.click("button:has-text('Done')")
        page.wait_for_timeout(1000)

        context.close()
        browser.close()
        print("Done!")

if __name__ == "__main__":
    run()
