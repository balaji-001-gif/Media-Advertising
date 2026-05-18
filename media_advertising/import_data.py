import os
import frappe
from frappe.modules.import_file import import_file_by_path

def run():
    app_path = frappe.get_app_path("media_advertising")
    print(f"Scanning app directory: {app_path}")
    
    json_files = []
    for root, dirs, files in os.walk(app_path):
        # Scan under workspace, report, and notification folders
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
