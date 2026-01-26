import os
import json
import time
import requests
from dotenv import load_dotenv
from playwright.sync_api import sync_playwright

# 1. Load Environment Variables
# In GitHub Actions, these are injected from Secrets
load_dotenv()

EMAIL = os.getenv("NPOINT_EMAIL")
PASSWORD = os.getenv("NPOINT_PASSWORD")
REGISTRY_BIN_ID = os.getenv("REGISTRY_BIN_ID") 

def run():
    # Get list of changed files passed from GitHub Action env var
    files_env = os.getenv("CHANGED_FILES", "")
    
    # --- LOCAL DEBUGGING SETUP ---
    # If running locally, you often won't have the CHANGED_FILES env var set.
    # Uncomment the line below and point it to a real file to test the script locally.
    # files_env = "lessons/grade-5-plants.json" 

    if not files_env:
        print("No files to process. Exiting.")
        return

    # GitHub Actions passes files separated by spaces
    files_to_process = files_env.split()
    print(f"Processing files: {files_to_process}")

    new_registry_entries = []
    
    # Detect if running in GitHub Actions (CI) or Locally
    is_ci = os.getenv("GITHUB_ACTIONS") == "true"
    
    # If Local: Headless=False (Show Browser), SlowMo=1000ms (Human speed)
    # If CI: Headless=True (Hidden), SlowMo=0ms (Fastest)
    headless_mode = is_ci
    slow_mo_delay = 0 if is_ci else 1000

    print(f"Launching Browser (Headless: {headless_mode})...")

    with sync_playwright() as p:
        # Launch browser with settings determined above
        browser = p.chromium.launch(headless=headless_mode, slow_mo=slow_mo_delay)
        
        # FIX 1: Set a real User-Agent to avoid bot detection/white screens
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            permissions=["clipboard-read", "clipboard-write"]
        )
        
        # CRITICAL: Grant clipboard permissions for Headless mode to work with copy/paste
        context.grant_permissions(['clipboard-read', 'clipboard-write'], origin='https://www.npoint.io')
        
        page = context.new_page()

        print("--- Step 1: Logging into npoint.io ---")
        
        try:
            # Go to Home Page
            page.goto("https://www.npoint.io/", timeout=60000)
            
            # FIX 2: Wait for network to idle
            try:
                page.wait_for_load_state("networkidle", timeout=5000)
            except:
                pass 
            
            # Login Flow: Click Dropdown -> Fill Form -> Submit
            print("Opening Login Dropdown...")
            page.wait_for_selector('.login-dropdown-component', state="visible", timeout=20000)
            page.click('.login-dropdown-component')

            print("Entering credentials...")
            # Updated selectors based on the .login-component container
            page.wait_for_selector('.login-component', state="visible", timeout=10000)
            
            # Select the first input in the component (typically Email/User)
            page.fill('.login-component input:first-of-type', EMAIL)
            # Select the password input
            page.fill('.login-component input[type="password"]', PASSWORD)
            
            print("Clicking Login...")
            # Target the button strictly inside the login component
            page.click('.login-component button.button.primary');
            # Wait for redirection to the dashboard (/docs)
            page.wait_for_url("**/docs", timeout=30000)
            print("Logged in successfully.")
            
        except Exception as e:
            print(f"!!! LOGIN FAILED !!!")
            print(f"Current URL: {page.url}")
            print(f"Page Title: {page.title()}")
            # Take a screenshot to debug visual errors
            page.screenshot(path="debug_error_login.png")
            print("Saved screenshot to debug_error_login.png")
            raise e

        # --- Step 2: Loop through each new file and create a bin ---
        for file_path in files_to_process:
            if not os.path.exists(file_path):
                print(f"Skipping {file_path} (File not found on disk)")
                continue
            
            print(f"--- Processing: {file_path} ---")
            
            try:
                with open(file_path, 'r') as f:
                    file_data = json.load(f)
                    json_content_str = json.dumps(file_data, indent=2)

                bin_title = file_data.get("title", os.path.basename(file_path))
                bin_id_key = file_data.get("id", os.path.splitext(os.path.basename(file_path))[0])

                # --- NEW CREATE FLOW ---
                # Click "+ New" button to generate a new bin slug
                print("Creating new bin...")
                
                # We try to find the "+ New" button. It is usually in the navbar.
                # If we can't find it, we force navigate to dashboard.
                try:
                    page.click('button:has-text("+ New")', timeout=5000)
                except:
                    print("'+ New' button not found instantly, going to dashboard...")
                    page.goto("https://www.npoint.io/docs")
                    page.click('button:has-text("+ New")')

                # Wait for the URL to change to a specific bin slug (something longer than just /docs)
                # We wait for the browser to settle on the new bin URL
                time.sleep(2) # Brief wait for the redirect to start
                page.wait_for_url(lambda url: "/docs/" in url and len(url.split("/")) > 4, timeout=20000)
                
                current_bin_url = page.url
                print(f"Draft initialized at: {current_bin_url}")

                # --- EDIT CONTENT ---
                # Click into the editor area
                print("Focusing editor...")
                # 2. Wait for the Ace editor container to be visible
                # The HTML shows id="brace-editor", which is a very robust selector
                page.wait_for_selector('#brace-editor', state="visible")

                # 3. Click the main editor body to focus it
                page.click('#brace-editor')

                # Clear existing text (Select All + Backspace)
                page.keyboard.press("ControlOrMeta+a")
                page.keyboard.press("Backspace")
                
                page.keyboard.insert_text(json_content_str)
                
                # Click Save
                print("Saving...")
                page.click('button:has-text("Save")')
                
                # Wait for Save confirmation (usually button state change or toast)
                # We'll wait a moment to ensure server sync
                time.sleep(2)
                
                # Capture URL (should differ if it was a "new" slug vs "saved" slug, but usually consistent on npoint)
                generated_bin_id = page.url.split("/")[-1]
                public_api_url = f"https://api.npoint.io/{generated_bin_id}"
                
                print(f"CREATED: {bin_title} -> {public_api_url}")

                new_registry_entries.append({
                    "id": bin_id_key,
                    "title": bin_title,
                    "url": public_api_url
                })
            except Exception as e:
                print(f"ERROR processing {file_path}: {e}")
                page.screenshot(path=f"debug_error_{bin_id_key}.png")

        # --- Step 3: Update Registry (Only if we have new entries) ---
        if new_registry_entries:
            print("--- Step 3: Updating Registry ---")
            
            # Fetch existing registry
            registry_api_url = f"https://api.npoint.io/{REGISTRY_BIN_ID}"
            try:
                current_registry = requests.get(registry_api_url).json()
                if not isinstance(current_registry, list):
                    current_registry = []
            except:
                current_registry = []

            # Update logic
            new_ids = [entry['id'] for entry in new_registry_entries]
            updated_registry = [item for item in current_registry if item.get('id') not in new_ids]
            updated_registry.extend(new_registry_entries)

            # Navigate to Registry Edit Page
            registry_edit_url = f"https://www.npoint.io/docs/{REGISTRY_BIN_ID}"
            page.goto(registry_edit_url)
            
            # Edit Registry
            updated_registry_str = json.dumps(updated_registry, indent=2)
            page.click('#brace-editor')
            # Clear existing text (Select All + Backspace)
            page.keyboard.press("ControlOrMeta+a")
            page.keyboard.press("Backspace")    
            page.keyboard.insert_text(updated_registry_str)
            
            # Save
            page.click('button:has-text("Save")')
            time.sleep(2) 
            print("Registry Updated Successfully!")
        else:
            print("No new entries created, skipping registry update.")

        browser.close()

if __name__ == "__main__":
    run()