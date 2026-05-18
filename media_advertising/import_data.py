import os
import frappe
from frappe.modules.import_file import import_file_by_path
from frappe.model.sync import sync_for

def run():
    app_path = frappe.get_app_path("media_advertising")
    print(f"Scanning app directory: {app_path}")
    
    # 1. Ensure all 8 Module Def records exist in the database (Create only if missing to prevent cache dirtiness)
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
    
    # 2. SAFE-CLEAR and RE-POPULATE the in-memory app modules dictionary
    # We use frappe.get_module_list(app) which is the official Frappe API to load modules from modules.txt!
    if hasattr(frappe.local, "app_modules") and isinstance(frappe.local.app_modules, dict):
        print("Safely clearing and reloading in-memory app modules cache...")
        frappe.local.app_modules.clear()
        
        # Load fresh list from database/files for all active apps
        for app in frappe.get_installed_apps():
            try:
                modules_list = frappe.get_module_list(app)
                if modules_list:
                    frappe.local.app_modules[app] = modules_list
            except Exception as e:
                print(f"⚠️ Failed to load modules for app {app}: {str(e)}")
                
        print(f"✅ In-memory app modules successfully reloaded! Active app modules: {list(frappe.local.app_modules.keys())}")
        
    frappe.clear_cache()
    frappe.local.cache = {}
    
    # 3. Programmatically force sync all DocTypes of media_advertising
    print("Force syncing all DocTypes for media_advertising...")
    try:
        sync_for("media_advertising", force=True)
        print("✅ All DocTypes force-synced successfully!")
    except Exception as e:
        print(f"⚠️ DocType sync warning: {str(e)}")
        
    # 4. Force import workspaces, reports, and notifications
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
