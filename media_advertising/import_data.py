import os
import frappe
from frappe.modules.import_file import import_file_by_path

def run():
    app_path = frappe.get_app_path("media_advertising")
    print(f"Scanning app directory: {app_path}")
    
    # 1. Ensure all 8 Module Def records exist in the database
    modules = [
        "Media Advertising", 
        "Campaign Management", 
        "Media Operations", 
        "Client CRM", 
        "Billing Finance", 
        "Resource Production", 
        "Reporting Analytics", 
        "Masters"
    ]
    
    print("Checking and restoring missing Module Def records...")
    for m in modules:
        if not frappe.db.exists("Module Def", m):
            print(f"🛠️ Creating missing Module Def: {m}")
            doc = frappe.new_doc("Module Def")
            doc.module_name = m
            doc.app_name = "media_advertising"
            doc.insert(ignore_permissions=True)
            
    frappe.db.commit()
    print("✅ All Module Def records verified and restored!")
    
    # 2. TARGETED CACHE RELOAD WITH SCRUBBED NAMES:
    # We populate the in-memory cache with the scrubbed, snake_case directory names (e.g. reporting_analytics)
    # This allows python to import the folders perfectly!
    if hasattr(frappe.local, "app_modules") and isinstance(frappe.local.app_modules, dict):
        print("Safely reloading in-memory app modules cache for media_advertising...")
        try:
            # Convert display names like 'Reporting Analytics' to 'reporting_analytics'
            scrubbed_modules = [frappe.scrub(m) for m in modules]
            frappe.local.app_modules["media_advertising"] = scrubbed_modules
            print(f"✅ In-memory app modules for media_advertising successfully reloaded: {scrubbed_modules}")
        except Exception as e:
            print(f"⚠️ Failed to load modules for media_advertising: {str(e)}")
        
    frappe.clear_cache()
    frappe.local.cache = {}
    
    # 3. Force import workspaces, reports, and notifications
    json_files = []
    for root, dirs, files in os.walk(app_path):
        if any(k in root for k in ["workspace", "report", "notification"]):
            for file in files:
                if file.endswith(".json"):
                    full_path = os.path.join(root, file)
                    json_files.append(full_path)
                    
    print(f"Found {len(json_files)} metadata files to import.")
    
    for path in json_files:
        print(f"Force importing: {path}")
        try:
            import_file_by_path(path, force=True)
        except Exception as e:
            print(f"❌ Failed to import {path}: {str(e)}")
            
    frappe.db.commit()
    print("✨ All workspaces, reports, and notifications successfully populated in the database!")
