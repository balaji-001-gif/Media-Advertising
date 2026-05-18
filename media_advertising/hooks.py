app_name = "media_advertising"
app_title = "Media Advertising"
app_publisher = "Your Company"
app_description = "Media & Advertising ERP for ERPNext v15+"
app_email = "dev@yourcompany.com"
app_license = "MIT"
app_version = "0.0.1"

# Required apps
required_apps = ["frappe", "erpnext"]

# DocTypes which need auto-naming
# autoname = "field:name"

# Includes in <head>
app_include_css = "/assets/media_advertising/css/media_advertising.bundle.css"
app_include_js = "/assets/media_advertising/js/media_advertising.bundle.js"

# Web assets
web_include_css = []
web_include_js = []

# Document Events
doc_events = {
    "Campaign": {
        "on_submit": "media_advertising.campaign_management.doctype.campaign.campaign.on_submit",
        "on_cancel": "media_advertising.campaign_management.doctype.campaign.campaign.on_cancel",
    },
    "Media Invoice": {
        "on_submit": "media_advertising.billing_finance.doctype.media_invoice.media_invoice.on_submit",
    },
    "Ad Booking": {
        "after_insert": "media_advertising.media_operations.doctype.ad_booking.ad_booking.after_insert",
    },
}

# Scheduled Tasks
scheduler_events = {
    "daily": [
        "media_advertising.campaign_management.utils.check_campaign_deadlines",
        "media_advertising.billing_finance.utils.check_billing_milestones",
    ],
    "weekly": [
        "media_advertising.reporting_analytics.utils.generate_weekly_reports",
    ],
}

# Permissions
# permission_query_conditions = {
#     "Campaign": "media_advertising.campaign_management.doctype.campaign.campaign.get_permission_query_conditions",
# }

# Fixtures — export these with bench export-fixtures
fixtures = [
    {"dt": "Custom Field", "filters": [["module", "=", "Media Advertising"]]},
    {"dt": "Property Setter", "filters": [["module", "=", "Media Advertising"]]},
    {"dt": "Workspace", "filters": [["module", "=", "Media Advertising"]]},
    "Industry Vertical",
    "Media Category",
    "Ad Format",
    "KPI Definition",
]

# Override standard methods
# override_whitelisted_methods = {}

# Jinja methods
# jinja = {"methods": [], "filters": []}

# Notification config
# notification_config = "media_advertising.notifications.get_notification_config"
