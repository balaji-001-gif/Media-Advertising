import frappe
from frappe.utils import add_days, today

def get_default_company():
    company = frappe.db.get_single_value("Global Defaults", "default_company")
    if not company:
        companies = frappe.get_all("Company", limit=1)
        company = companies[0].name if companies else None
    if not company:
        print("🛠️ Creating fallback default company...")
        try:
            company_doc = frappe.new_doc("Company")
            company_doc.company_name = "Global Technologies"
            company_doc.default_currency = "INR"
            company_doc.insert(ignore_permissions=True)
            company = company_doc.name
        except Exception:
            company = "Global Technologies"
    return company

def get_default_currency():
    return frappe.db.get_single_value("Global Defaults", "default_currency") or "INR"

def create_demo_data():
    print("🚀 Initializing premium demo data generation...")
    
    # Check if demo data already exists to prevent duplicate execution
    if frappe.db.count("Agency Client") >= 10:
        print("✅ Demo data already populated in the system! Skipping generation.")
        return
        
    company = get_default_company()
    currency = get_default_currency()
    user = "Administrator"
    current_date = today()
    
    # 1. Populate Industry Vertical
    verticals = [
        "Automotive", "FMCG", "Real Estate", "E-Commerce", "Technology",
        "Health & Wellness", "Entertainment", "Travel & Tourism", "Banking & Finance", "Education"
    ]
    print("Populating Industry Verticals...")
    for v in verticals:
        if not frappe.db.exists("Industry Vertical", v):
            doc = frappe.new_doc("Industry Vertical")
            doc.vertical_name = v
            doc.description = f"Industry Vertical for {v}"
            doc.insert(ignore_permissions=True)
            
    # 2. Populate Media Category
    categories = [
        "Digital", "Television", "Radio", "Out of Home", "Print", "Social Media", "Cinema", "Influencer Marketing"
    ]
    print("Populating Media Categories...")
    for c in categories:
        if not frappe.db.exists("Media Category", c):
            doc = frappe.new_doc("Media Category")
            doc.category_name = c
            doc.description = f"Media category for {c} channels"
            doc.insert(ignore_permissions=True)
            
    # 3. Populate KPI Definition
    kpis = [
        ("Click Through Rate", "CTR", "Percentage of users who click a link out of total viewers"),
        ("Cost Per Mille", "CPM", "Cost per thousand impressions"),
        ("Reach", "Reach", "Total unique audience exposed to the ad"),
        ("Conversions", "Conversions", "Total successful desired actions completed"),
        ("Impressions", "Impressions", "Total number of times the ad is displayed"),
        ("Return on Ad Spend", "ROAS", "Revenue generated divided by ad spend value"),
        ("Cost Per Click", "CPC", "Average cost incurred per click action"),
        ("Engagement Rate", "Engagement", "Total interactions divided by total reach percentage")
    ]
    print("Populating KPI Definitions...")
    for name, code, desc in kpis:
        if not frappe.db.exists("KPI Definition", name):
            doc = frappe.new_doc("KPI Definition")
            doc.kpi_name = name
            doc.kpi_code = code
            doc.description = desc
            doc.insert(ignore_permissions=True)

    # 4. Populate Media Channel
    channels = [
        ("Google Display Network", "Digital"),
        ("YouTube Video Ads", "Digital"),
        ("Star Sports TV", "Television"),
        ("Times of India Newspaper", "Print"),
        ("Red FM Radio", "Radio"),
        ("Billboard Metro Station", "Out of Home"),
        ("Facebook Sponsored Ads", "Social Media"),
        ("Instagram Influencer Post", "Influencer Marketing"),
        ("PVR Cinema Ads", "Cinema"),
        ("LinkedIn Sponsored Content", "Social Media")
    ]
    print("Populating Media Channels...")
    for name, cat in channels:
        if not frappe.db.exists("Media Channel", name):
            doc = frappe.new_doc("Media Channel")
            doc.channel_name = name
            doc.media_category = cat
            doc.insert(ignore_permissions=True)

    # 5. Populate Ad Format
    formats = [
        ("Display Banner", "Digital"),
        ("Video Ad (30 sec)", "Television"),
        ("Audio Spot (15 sec)", "Radio"),
        ("Full Page Print Ad", "Print"),
        ("Billboard Physical Banner", "Out of Home"),
        ("Carousel Post", "Social Media"),
        ("Cinema Slide", "Cinema"),
        ("Sponsored Story", "Influencer Marketing")
    ]
    print("Populating Ad Formats...")
    for name, cat in formats:
        if not frappe.db.exists("Ad Format", name):
            doc = frappe.new_doc("Ad Format")
            doc.format_name = name
            doc.media_category = cat
            doc.insert(ignore_permissions=True)

    # 6. Populate Ad Slot (12 entries to link with bookings)
    print("Populating Ad Slots...")
    created_slots = []
    slot_names = [
        "Google Premium Header banner",
        "YouTube Non-skippable Slot A",
        "Star Sports Primetime Slot 1",
        "TOI Front Page Bottom Quarter",
        "Red FM Evening Drive Slot",
        "Billboard HSR Layout Metro",
        "FB Carousel Ad Slot Prime",
        "Insta Influencer Story Slot",
        "PVR Cinema Interval Slide",
        "LinkedIn Sponsored post slot",
        "Google Display sidebar banner",
        "YouTube Midroll Spot 2"
    ]
    for i, name in enumerate(slot_names):
        chan = channels[i % len(channels)][0]
        fmt = formats[i % len(formats)][0]
        if not frappe.db.exists("Ad Slot", {"slot_name": name}):
            doc = frappe.new_doc("Ad Slot")
            doc.naming_series = "SLOT-.YYYY.-"
            doc.slot_name = name
            doc.media_channel = chan
            doc.ad_format = fmt
            doc.rate = 5000 + (i * 1000)
            doc.availability_status = "Available"
            doc.insert(ignore_permissions=True)
            created_slots.append(doc.name)
        else:
            created_slots.append(frappe.db.get_value("Ad Slot", {"slot_name": name}, "name"))

    # 7. Populate Agency Client (12 premium entries)
    clients_data = [
        ("Tesla India", "Automotive", "tesla.india@tesla.com", "+919988776611", "Whitefield, Bangalore"),
        ("Unilever Group", "FMCG", "marketing@unilever.com", "+919988776612", "Andheri East, Mumbai"),
        ("DLF Homes", "Real Estate", "sales@dlfhomes.com", "+919988776613", "DLF Phase 3, Gurugram"),
        ("Amazon India", "E-Commerce", "ads-india@amazon.com", "+919988776614", "Brigade Gateway, Bangalore"),
        ("Samsung Electronics", "Technology", "samsung.media@samsung.com", "+919988776615", "Sector 43, Noida"),
        ("CureFit Wellness", "Health & Wellness", "fitness@curefit.com", "+919988776616", "HSR Layout, Bangalore"),
        ("Netflix India", "Entertainment", "netflix.media@netflix.com", "+919988776617", "Bandra West, Mumbai"),
        ("MakeMyTrip", "Travel & Tourism", "travel.ads@makemytrip.com", "+919988776618", "DLF Cyber City, Gurugram"),
        ("HDFC Bank", "Banking & Finance", "campaigns@hdfcbank.com", "+919988776619", "Senapati Bapat Marg, Mumbai"),
        ("BYJU's Education", "Education", "marketing@byjus.com", "+919988776620", "Bannerghatta Road, Bangalore"),
        ("Zomato Foodtech", "E-Commerce", "ad-ops@zomato.com", "+919988776621", "DLF Phase 2, Gurugram"),
        ("Tata Motors", "Automotive", "tata.motors@tata.com", "+919988776622", "Prabhadevi, Mumbai")
    ]
    print("Populating Agency Clients...")
    created_clients = []
    for name, vert, email, phone, addr in clients_data:
        if not frappe.db.exists("Agency Client", {"client_name": name}):
            doc = frappe.new_doc("Agency Client")
            doc.naming_series = "CLT-.YYYY.-"
            doc.client_name = name
            doc.industry_vertical = vert
            doc.email = email
            doc.phone = phone
            doc.billing_address = addr
            doc.account_manager = ""  # Keep empty to prevent email notification warnings
            doc.is_active = 1
            doc.insert(ignore_permissions=True)
            created_clients.append(doc.name)
        else:
            created_clients.append(frappe.db.get_value("Agency Client", {"client_name": name}, "name"))

    # 8. Populate Client Brief (12 entries)
    print("Populating Client Briefs...")
    created_briefs = []
    brief_titles = [
        "Model 3 Launch India Campaign",
        "Dove Summer Glow Awareness",
        "DLF Midtown Luxury Launch",
        "Great Indian Festival Ad-Ops",
        "Galaxy Fold Z Digital Push",
        "CultFit Ultimate Pass Promotion",
        "Sacred Games Season 3 Promo",
        "Monsoon Getaway Special Plan",
        "HDFC Millennia Credit Card Push",
        "BYJU'S Learning App User Acquisition",
        "Zomato Gold Carnival Blitz",
        "Tata Nexon EV Redesign Launch"
    ]
    budgets = [2500000, 1500000, 4500000, 8500000, 6000000, 1200000, 3000000, 1800000, 5000000, 3500000, 2800000, 4000000]
    
    for i, title in enumerate(brief_titles):
        client_name = created_clients[i]
        if not frappe.db.exists("Client Brief", {"brief_title": title}):
            doc = frappe.new_doc("Client Brief")
            doc.naming_series = "CB-.YYYY.-"
            doc.brief_title = title
            doc.client = client_name
            doc.received_date = current_date
            doc.budget = budgets[i]
            doc.timeline = "3 Months"
            doc.status = "Converted"
            doc.assigned_to = user
            doc.requirements = f"<p>Detailed advertising requirements for {title}. Target audience must align with demographic parameters.</p>"
            doc.objectives = f"<p>Achieve premium reach, click through rates, and maximize conversions with optimized budget allocation.</p>"
            doc.insert(ignore_permissions=True)
            created_briefs.append(doc.name)
        else:
            created_briefs.append(frappe.db.get_value("Client Brief", {"brief_title": title}, "name"))

    # 9. Populate Campaign Brief (12 entries - required by Campaign linkage)
    print("Populating Campaign Briefs...")
    created_camp_briefs = []
    for i, title in enumerate(brief_titles):
        client_name = created_clients[i]
        if not frappe.db.exists("Campaign Brief", {"brief_title": title}):
            doc = frappe.new_doc("Campaign Brief")
            doc.naming_series = "BRIEF-.YYYY.-"
            doc.brief_title = title
            doc.client = client_name
            doc.brief_date = current_date
            doc.due_date = add_days(current_date, 15)
            doc.status = "Approved"
            doc.objectives = f"<p>Campaign objectives for {title}.</p>"
            doc.budget_indication = budgets[i]
            doc.insert(ignore_permissions=True)
            created_camp_briefs.append(doc.name)
        else:
            created_camp_briefs.append(frappe.db.get_value("Campaign Brief", {"brief_title": title}, "name"))

    # 10. Populate Campaign (12 entries)
    print("Populating Campaigns...")
    created_campaigns = []
    for i, title in enumerate(brief_titles):
        client_name = created_clients[i]
        camp_brief_name = created_camp_briefs[i]
        campaign_name = f"CAM - {title}"
        if not frappe.db.exists("Campaign", {"campaign_name": campaign_name}):
            doc = frappe.new_doc("Campaign")
            doc.naming_series = "CAMP-.YYYY.-"
            doc.campaign_name = campaign_name
            doc.client = client_name
            doc.campaign_brief = camp_brief_name
            doc.start_date = current_date
            doc.end_date = add_days(current_date, 90)
            doc.total_budget = budgets[i]
            doc.currency = currency
            doc.company = company
            doc.status = "Active"
            doc.account_manager = ""  # Keep empty to prevent email notification triggers
            doc.description = f"<p>Active execution log for {campaign_name}. Relational KPI thresholds and channels have been locked.</p>"
            doc.insert(ignore_permissions=True)
            
            # Reload fresh instance to avoid CannotChangeConstantError on set_only_once naming_series
            fresh_doc = frappe.get_doc("Campaign", doc.name)
            fresh_doc.submit()
            created_campaigns.append(fresh_doc.name)
        else:
            created_campaigns.append(frappe.db.get_value("Campaign", {"campaign_name": campaign_name}, "name"))

    # 11. Populate Client Approval (12 entries)
    print("Populating Client Approvals...")
    for i, campaign in enumerate(created_campaigns):
        client_name = created_clients[i]
        title = f"Approval for {brief_titles[i]}"
        if not frappe.db.exists("Client Approval", {"approval_title": title}):
            doc = frappe.new_doc("Client Approval")
            doc.naming_series = "APPV-.YYYY.-"
            doc.approval_title = title
            doc.client = client_name
            doc.campaign = campaign
            doc.approval_type = "Media Plan Approval"
            doc.approval_date = current_date
            doc.status = "Approved"
            doc.approved_by = "Client Marketing Head"
            doc.approved_on = current_date
            doc.remarks = f"<p>The locked campaign structure for {brief_titles[i]} is approved for execution.</p>"
            doc.insert(ignore_permissions=True)

    # 12. Populate Media Plan (12 entries)
    print("Populating Media Plans...")
    created_plans = []
    for i, campaign in enumerate(created_campaigns):
        plan_name = f"Plan for {brief_titles[i]}"
        client_name = created_clients[i]
        if not frappe.db.exists("Media Plan", {"campaign": campaign}):
            doc = frappe.new_doc("Media Plan")
            doc.naming_series = "MP-.YYYY.-"
            doc.plan_title = plan_name
            doc.campaign = campaign
            doc.client = client_name
            doc.plan_date = current_date
            doc.status = "Approved"
            
            # Append detailed item row matching correct child table field 'media_plan_items'
            doc.append("media_plan_items", {
                "media_channel": "Google Display Network" if i % 2 == 0 else "YouTube Video Ads",
                "ad_format": "Display Banner" if i % 2 == 0 else "Video Ad (30 sec)",
                "rate": budgets[i] * 0.6,
                "quantity": 1,
                "start_date": current_date,
                "end_date": add_days(current_date, 90)
            })
            doc.append("media_plan_items", {
                "media_channel": "Instagram Influencer Post" if i % 2 == 0 else "Facebook Sponsored Ads",
                "ad_format": "Sponsored Story" if i % 2 == 0 else "Carousel Post",
                "rate": budgets[i] * 0.4,
                "quantity": 1,
                "start_date": current_date,
                "end_date": add_days(current_date, 90)
            })
            
            doc.insert(ignore_permissions=True)
            
            # Reload fresh instance to avoid CannotChangeConstantError
            fresh_doc = frappe.get_doc("Media Plan", doc.name)
            fresh_doc.submit()
            created_plans.append(fresh_doc.name)
        else:
            created_plans.append(frappe.db.get_value("Media Plan", {"campaign": campaign}, "name"))

    # 13. Populate Creative Asset (12 entries)
    # Generated before Ad Booking to allow linking!
    print("Populating Creative Assets...")
    created_creatives = []
    for i, campaign in enumerate(created_campaigns):
        name = f"Asset {brief_titles[i]}"
        if not frappe.db.exists("Creative Asset", {"asset_name": name}):
            doc = frappe.new_doc("Creative Asset")
            doc.naming_series = "CA-.YYYY.-"
            doc.campaign = campaign
            doc.asset_name = name
            doc.asset_type = "Video" if i % 2 == 0 else "Image"
            doc.status = "Approved"
            doc.designer = user
            doc.insert(ignore_permissions=True)
            created_creatives.append(doc.name)
        else:
            created_creatives.append(frappe.db.get_value("Creative Asset", {"asset_name": name}, "name"))

    # 14. Populate Ad Booking (12 entries)
    # The submit hook of Ad Booking automatically and cleanly handles Traffic Order generation!
    print("Populating Ad Bookings...")
    created_bookings = []
    for i, plan in enumerate(created_plans):
        campaign = created_campaigns[i]
        client_name = created_clients[i]
        slot = created_slots[i]
        chan = channels[i % len(channels)][0]
        fmt = formats[i % len(formats)][0]
        creative = created_creatives[i]
        if not frappe.db.exists("Ad Booking", {"media_plan": plan}):
            doc = frappe.new_doc("Ad Booking")
            doc.naming_series = "BOOK-.YYYY.-"
            doc.booking_title = f"Booking - {brief_titles[i]}"
            doc.campaign = campaign
            doc.client = client_name
            doc.ad_slot = slot
            doc.media_plan = plan
            doc.media_channel = chan
            doc.ad_format = fmt
            doc.booking_date = current_date
            doc.air_date = current_date  # Critical to prevent mandatory field errors in auto-generated Traffic Orders
            doc.start_date = current_date
            doc.end_date = add_days(current_date, 30)
            doc.negotiated_rate = budgets[i] * 0.5
            doc.creative_asset = creative
            doc.status = "Confirmed"
            doc.insert(ignore_permissions=True)
            
            # Reload fresh instance to avoid CannotChangeConstantError
            fresh_doc = frappe.get_doc("Ad Booking", doc.name)
            fresh_doc.submit()
            created_bookings.append(fresh_doc.name)
        else:
            created_bookings.append(frappe.db.get_value("Ad Booking", {"media_plan": plan}, "name"))

    # 15. Populate Campaign Budget (12 entries)
    print("Populating Campaign Budgets...")
    for i, campaign in enumerate(created_campaigns):
        client_name = created_clients[i]
        if not frappe.db.exists("Campaign Budget", {"campaign": campaign}):
            doc = frappe.new_doc("Campaign Budget")
            doc.naming_series = "CBUD-.YYYY.-"
            doc.campaign = campaign
            doc.client = client_name
            doc.total_budget = budgets[i]
            doc.currency = currency
            doc.status = "Approved"
            
            # Append detailed item row matching correct child table field 'budget_items'
            doc.append("budget_items", {
                "media_channel": "Google Display Network" if i % 2 == 0 else "YouTube Video Ads",
                "allocated": budgets[i] * 0.7
            })
            doc.append("budget_items", {
                "media_channel": "Instagram Influencer Post" if i % 2 == 0 else "Facebook Sponsored Ads",
                "allocated": budgets[i] * 0.3
            })
            
            doc.insert(ignore_permissions=True)
            
            # Reload fresh instance to avoid CannotChangeConstantError
            fresh_doc = frappe.get_doc("Campaign Budget", doc.name)
            fresh_doc.submit()

    # 16. Populate Media Invoice (12 entries)
    print("Populating Media Invoices...")
    for i, campaign in enumerate(created_campaigns):
        client = created_clients[i]
        booking = created_bookings[i]
        if not frappe.db.exists("Media Invoice", {"campaign": campaign}):
            doc = frappe.new_doc("Media Invoice")
            doc.naming_series = "MINV-.YYYY.-"
            doc.invoice_title = f"Invoice - {brief_titles[i]}"
            doc.campaign = campaign
            doc.client = client
            doc.invoice_date = current_date
            doc.due_date = add_days(current_date, 30)
            doc.company = company
            doc.currency = currency
            doc.status = "Draft"  # Set to valid Select option
            
            # Append item row matching correct child table field 'invoice_items'
            doc.append("invoice_items", {
                "description": f"Media Delivery Fees for {brief_titles[i]}",
                "ad_booking": booking,
                "quantity": 1,
                "rate": budgets[i]
            })
            
            doc.insert(ignore_permissions=True)
            
            # Reload fresh instance to avoid CannotChangeConstantError
            fresh_doc = frappe.get_doc("Media Invoice", doc.name)
            fresh_doc.submit()

    # 17. Populate Production Job (12 entries)
    print("Populating Production Jobs...")
    for i, campaign in enumerate(created_campaigns):
        name = f"Job for {brief_titles[i]}"
        if not frappe.db.exists("Production Job", {"job_name": name}):
            doc = frappe.new_doc("Production Job")
            doc.naming_series = "PROD-.YYYY.-"
            doc.job_name = name
            doc.campaign = campaign
            doc.start_date = current_date
            doc.end_date = add_days(current_date, 15)
            doc.status = "In Progress"
            doc.assigned_team = "Creative Team Alpha"
            doc.insert(ignore_permissions=True)

    print("✨ Premium demo data generation finished successfully!")
