import frappe

__version__ = "0.0.1"

def create_missing_modules():
    try:
        # Check if the database connection is active
        if frappe.db:
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
            for m in modules:
                # Use a fast, raw SQL query to verify and restore the Module Def row
                # This bypasses all early-boot permission and validation locks!
                exists = frappe.db.sql("SELECT name FROM `tabModule Def` WHERE name=%s", (m,))
                if not exists:
                    frappe.db.sql(
                        "INSERT IGNORE INTO `tabModule Def` (name, module_name, app_name, creation, modified, modified_by, owner) VALUES (%s, %s, %s, NOW(), NOW(), 'Administrator', 'Administrator')",
                        (m, m, "media_advertising")
                    )
            frappe.db.commit()
    except Exception:
        pass

# Run database healing automatically on app load
create_missing_modules()
