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
        context = browser.new_context()
        
        # CRITICAL: Grant clipboard permissions for Headless mode to work with copy/paste
        # FIX: Added origin to ensure permissions apply specifically to npoint
        context.grant_permissions(['clipboard-read', 'clipboard-write'], origin='https://www.npoint.io')
        
        page = context.new_page()

        print("--- Step 1: Logging into npoint.io ---")
        page.goto("https://www.npoint.io/login")
        
        # Login Logic
        page.fill('input[name="email"]', EMAIL)
        page.fill('input[name="password"]', PASSWORD)
        page.click('button[type="submit"]')
        
        # Wait specifically for the dashboard or nav to ensure login success
        # Increased timeout for slower CI runners
        page.wait_for_url("https://www.npoint.io/", timeout=30000)
        print("Logged in successfully.")

        # --- Step 2: Loop through each new file and create a bin ---
        for file_path in files_to_process:
            if not os.path.exists(file_path):
                print(f"Skipping {file_path} (File not found on disk)")
                continue
            
            print(f"--- Processing: {file_path} ---")
            
            try:
                with open(file_path, 'r') as f:
                    file_data = json.load(f)
                    # Convert to string for pasting
                    json_content_str = json.dumps(file_data, indent=2)

                # Metadata for registry
                # Uses the 'title' inside the JSON, or filename if missing
                bin_title = file_data.get("title", os.path.basename(file_path))
                # Uses the 'id' inside the JSON, or filename stem if missing
                bin_id_key = file_data.get("id", os.path.splitext(os.path.basename(file_path))[0])

                # Go to homepage to create new bin
                page.goto("https://www.npoint.io/")
                
                # Wait for the editor to appear
                page.wait_for_selector('.CodeMirror')
                page.click('.CodeMirror') 
                
                # Clear existing text
                page.keyboard.press("Control+A")
                page.keyboard.press("Backspace")
                
                # Robust Paste Logic with Fallback
                try:
                    # Attempt 1: Fast Clipboard Injection
                    page.evaluate(f"navigator.clipboard.writeText({json.dumps(json_content_str)})")
                    page.keyboard.press("Control+V")
                except Exception as clipboard_error:
                    # Attempt 2: Slow Typing (Fallback for restricted CI environments)
                    print(f"Clipboard access failed ({clipboard_error}), falling back to direct typing...")
                    page.keyboard.insert_text(json_content_str)
                
                # Click Save
                page.click('button:has-text("Save")')
                
                # Wait for URL to change to /docs/xyz
                page.wait_for_url("**/docs/*")
                
                # Capture URL
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
            
            # Fetch existing registry via Public API (Safer/Faster)
            registry_api_url = f"https://api.npoint.io/{REGISTRY_BIN_ID}"
            try:
                current_registry = requests.get(registry_api_url).json()
                if not isinstance(current_registry, list):
                    current_registry = []
            except:
                current_registry = []

            # Update logic: Remove old entries with same ID, append new ones
            new_ids = [entry['id'] for entry in new_registry_entries]
            
            # Keep entries that are NOT in our new list (preserve old data)
            updated_registry = [item for item in current_registry if item.get('id') not in new_ids]
            
            # Add new items
            updated_registry.extend(new_registry_entries)

            # Navigate to Registry Edit Page
            registry_edit_url = f"https://www.npoint.io/docs/{REGISTRY_BIN_ID}"
            page.goto(registry_edit_url)
            
            # Paste Logic with Fallback
            page.wait_for_selector('.CodeMirror')
            page.click('.CodeMirror')
            
            updated_registry_str = json.dumps(updated_registry, indent=2)
            
            page.keyboard.press("Control+A")
            page.keyboard.press("Backspace")

            try:
                page.evaluate(f"navigator.clipboard.writeText({json.dumps(updated_registry_str)})")
                page.keyboard.press("Control+V")
            except Exception:
                print("Clipboard failed for registry update, typing manually...")
                page.keyboard.insert_text(updated_registry_str)
            
            # Save
            page.click('button:has-text("Save")')
            
            # Brief wait to ensure save request hits server
            time.sleep(2) 
            print("Registry Updated Successfully!")
        else:
            print("No new entries created, skipping registry update.")

        browser.close()

if __name__ == "__main__":
    run()