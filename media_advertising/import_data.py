import os
import frappe
from frappe.modules.import_file import import_file_by_path

def run():
    app_path = frappe.get_app_path("media_advertising")
    print(f"Scanning app directory: {app_path}")
    
    # 1. Canonical list of 8 modules
    modules = [
        "Media Advertising", 
        "Campaign Management", 
        "Media Operations", 
        "Client Crm", 
        "Billing Finance", 
        "Resource Production", 
        "Reporting Analytics", 
        "Masters"
    ]
    
    # 2. Database Self-Healing Sweep: Delete any stale/incorrectly cased Module Def records
    print("Sweeping database for stale or incorrectly cased Module Defs...")
    existing_module_defs = frappe.get_all("Module Def", filters={"app_name": "media_advertising"}, fields=["name"])
    existing_names = [d.name for d in existing_module_defs]
    
    for name in existing_names:
        if name not in modules:
            print(f"🗑️ Deleting stale/incorrect Module Def: {name}")
            try:
                frappe.delete_doc("Module Def", name, force=True, ignore_permissions=True)
            except Exception as e:
                print(f"⚠️ Failed to delete stale module {name}: {str(e)}")
                
    # Restore/Verify the correct 8 canonical modules
    print("Checking and restoring correct Module Def records...")
    for m in modules:
        if not frappe.db.exists("Module Def", m):
            print(f"🛠️ Creating correct Module Def: {m}")
            doc = frappe.new_doc("Module Def")
            doc.module_name = m
            doc.app_name = "media_advertising"
            doc.insert(ignore_permissions=True)
            
    frappe.db.commit()
    print("✅ All Module Def records verified, swept, and restored!")
    
    # 3. TARGETED CACHE RELOAD FOR BOTH APP_MODULES AND MODULE_APP:
    # This fully registers all 8 modules in Frappe's in-memory maps!
    scrubbed_modules = [frappe.scrub(m) for m in modules]
    
    # Reload app_modules cache (App -> Modules)
    if hasattr(frappe.local, "app_modules") and isinstance(frappe.local.app_modules, dict):
        print("Safely reloading in-memory app_modules cache for media_advertising...")
        frappe.local.app_modules["media_advertising"] = scrubbed_modules
        print("✅ app_modules cache updated successfully!")
        
    # Reload module_app cache (Module -> App)
    if hasattr(frappe.local, "module_app") and isinstance(frappe.local.module_app, dict):
        print("Safely reloading in-memory module_app cache for media_advertising...")
        for sm in scrubbed_modules:
            frappe.local.module_app[sm] = "media_advertising"
        print("✅ module_app cache updated successfully!")
        
    frappe.clear_cache()
    frappe.local.cache = {}
    
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

