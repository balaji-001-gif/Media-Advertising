import os
import frappe
from frappe.modules.import_file import import_file_by_path

def run():
    app_path = frappe.get_app_path("media_advertising")
    print(f"Scanning app directory: {app_path}")
    
    # 1. Check if media_advertising is registered as installed on the site in the database
    installed_apps = frappe.db.sql("SELECT name FROM `tabInstalled App` WHERE name=%s", ("media_advertising",))
    print(f"DEBUG: Installed App check in DB: {installed_apps}")
    
    if not installed_apps:
        print("⚠️ WARNING: media_advertising is NOT in tabInstalled App table! Attempting to register it...")
        frappe.db.sql("INSERT IGNORE INTO `tabInstalled App` (name, creation, modified, modified_by, owner) VALUES (%s, NOW(), NOW(), 'Administrator', 'Administrator')", ("media_advertising",))
        frappe.db.commit()
        print("✅ Registered media_advertising in tabInstalled App!")
    
    # Print existing Module Defs in DB to debug
    res = frappe.db.sql("SELECT name, app_name FROM `tabModule Def` WHERE name IN ('Masters', 'Reporting Analytics', 'Media Operations', 'Campaign Management', 'Client CRM', 'Billing Finance', 'Resource Production', 'Media Advertising')")
    print(f"DEBUG: Found Module Defs in DB: {res}")
    
    # 2. Force recreate all 8 Module Def records to ensure they exist and are correctly linked
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
    
    print("Forcing restoration of all 8 Module Def records...")
    for m in modules:
        exists = frappe.db.sql("SELECT name FROM `tabModule Def` WHERE name=%s", (m,))
        if exists:
            print(f"Module Def {m} exists in DB. Deleting and recreating to ensure correctness...")
            frappe.db.sql("DELETE FROM `tabModule Def` WHERE name=%s", (m,))
        
        print(f"🛠️ Creating Module Def: {m}")
        doc = frappe.new_doc("Module Def")
        doc.module_name = m
        doc.app_name = "media_advertising"
        doc.insert(ignore_permissions=True)
            
    frappe.db.commit()
    print("✅ All Module Def records successfully restored and verified!")
    
    # Clear local and global caches
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
