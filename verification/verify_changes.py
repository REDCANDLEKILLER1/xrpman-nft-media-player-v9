import os
from playwright.sync_api import sync_playwright

def verify_changes():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        # Open local file
        # Assuming the script is run from repo root
        file_path = os.path.abspath("index.html")
        page.goto(f"file://{file_path}")

        # 1. Verify Tip Link Attribute
        tip_link = page.locator("#tipLink")
        target_attr = tip_link.get_attribute("target")
        if target_attr is None:
            print("SUCCESS: #tipLink does not have target='_blank'.")
        else:
            print(f"FAILURE: #tipLink has target='{target_attr}'.")

        # 2. Verify Tip Button Removal from Control Bar
        # Control bar button should NOT exist
        # We can check if #btnTip is NOT inside .control-bar
        # or just check that #btnTip exists and is visible in the header

        control_bar_btn = page.locator(".control-bar #btnTip")
        if control_bar_btn.count() == 0:
            print("SUCCESS: #btnTip is NOT in .control-bar.")
        else:
            print("FAILURE: #btnTip IS STILL in .control-bar.")

        # 3. Verify Tip Button Presence in Header
        # We can look for it in the header area or just verify visibility
        header_btn = page.locator(".live-border #btnTip")
        if header_btn.count() > 0 and header_btn.is_visible():
            print("SUCCESS: #btnTip IS in .live-border (header) and is visible.")
        else:
            print("FAILURE: #btnTip is NOT found or NOT visible in .live-border.")

        # Take screenshots
        page.screenshot(path="verification/full_page.png", full_page=True)

        # Screenshot of Header
        header = page.locator(".live-border")
        if header.count() > 0:
            header.screenshot(path="verification/header_verification.png")

        # Screenshot of Control Bar
        control_bar = page.locator(".control-bar")
        if control_bar.count() > 0:
            control_bar.screenshot(path="verification/control_bar_verification.png")

        browser.close()

if __name__ == "__main__":
    verify_changes()
