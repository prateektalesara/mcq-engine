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
    
    # If strictly testing locally, you can uncomment this:
    # files_env = "lessons/grade-5-plants.json"

    if not files_env:
        print("No files to process. Exiting.")
        return

    # GitHub Actions passes files separated by spaces
    files_to_process = files_env.split()
    print(f"Processing files: {files_to_process}")

    new_registry_entries = []

    with sync_playwright() as p:
        # headless=True is MANDATORY for GitHub Actions
        browser = p.chromium.launch(headless=True)
        
        # FIX 1: Set a real User-Agent to avoid bot detection/white screens
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
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
            page.wait_for_selector('input[name="email"]', state="visible", timeout=10000)
            page.fill('input[name="email"]', EMAIL)
            page.fill('input[name="password"]', PASSWORD)
            
            print("Clicking Login...")
            # Target the submit button inside the form
            page.click('button[type="submit"]')
            
            # Wait for redirection to the dashboard (/docs)
            page.wait_for_url("**/docs", timeout=30000)
            print("Logged in successfully.")
            
        except Exception as e:
            print(f"!!! LOGIN FAILED !!!")
            print(f"Current URL: {page.url}")
            print(f"Page Title: {page.title()}")
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
                # Try finding CodeMirror first (standard), fallback to generic textarea if changed
                try:
                    page.wait_for_selector('.CodeMirror', state="visible", timeout=10000)
                    page.click('.CodeMirror')
                except:
                    # Fallback if they use a plain textarea now
                    page.click('textarea')

                # Clear existing text (Select All + Backspace)
                page.keyboard.press("Control+A")
                page.keyboard.press("Backspace")
                
                # Robust Paste Logic
                try:
                    page.evaluate(f"navigator.clipboard.writeText({json.dumps(json_content_str)})")
                    page.keyboard.press("Control+V")
                except Exception as clipboard_error:
                    print(f"Clipboard access failed, falling back to typing...")
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
            page.wait_for_selector('.CodeMirror', state="visible", timeout=15000)
            page.click('.CodeMirror')
            
            updated_registry_str = json.dumps(updated_registry, indent=2)
            
            page.keyboard.press("Control+A")
            page.keyboard.press("Backspace")

            try:
                page.evaluate(f"navigator.clipboard.writeText({json.dumps(updated_registry_str)})")
                page.keyboard.press("Control+V")
            except Exception:
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