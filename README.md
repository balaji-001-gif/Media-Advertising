# Media Advertising ERP — ERPNext v15+ Custom App

A full-featured Media & Advertising ERP built on the **Frappe Framework v15+** and **ERPNext v15+**, covering Campaign Management, Media Operations, Client CRM, Billing & Finance, Resource & Production, Reporting & Analytics, and Master data.

---

## Table of Contents
1. [Prerequisites](#prerequisites)
2. [Installation](#installation)
3. [App Structure](#app-structure)
4. [Doctypes Reference](#doctypes-reference)
5. [Reports](#reports)
6. [Workspace & Dashboard](#workspace--dashboard)
7. [Notifications](#notifications)
8. [Scheduled Tasks](#scheduled-tasks)
9. [Fixtures & Default Data](#fixtures--default-data)
10. [ERPNext Integration Points](#erpnext-integration-points)
11. [Common Errors & Fixes](#common-errors--fixes)
12. [Development Guide](#development-guide)
13. [Git Setup](#git-setup)

---

## Prerequisites

| Requirement | Version |
|-------------|---------|
| Python | 3.10+ |
| Node.js | 18+ |
| Frappe Framework | v15.x |
| ERPNext | v15.x |
| MariaDB | 10.6+ |
| Redis | 6+ |

---

## Installation

### 1. Get the app into your bench

```bash
cd /path/to/frappe-bench
bench get-app https://github.com/your-org/media_advertising
# OR for local dev:
bench get-app media_advertising /absolute/path/to/media_advertising
```

### 2. Install on a site

```bash
bench --site your-site.localhost install-app media_advertising
```

### 3. Run migrations

```bash
bench --site your-site.localhost migrate
```

### 4. Build assets

```bash
bench build --app media_advertising
```

### 5. Restart

```bash
bench restart
# or in development:
bench start
```

### 6. Load fixtures (default master data)

```bash
bench --site your-site.localhost import-fixtures --app media_advertising
```

---

## App Structure

```
media_advertising/                          # Bench app root
├── setup.py
├── pyproject.toml
├── requirements.txt
├── MANIFEST.in
├── README.md
└── media_advertising/                      # Python package
    ├── __init__.py                         # sets __version__
    ├── hooks.py                            # app metadata, events, scheduler
    ├── modules.txt                         # "Media Advertising" (one line)
    ├── public/
    │   ├── js/media_advertising.js
    │   └── css/media_advertising.css
    ├── config/
    │   ├── __init__.py
    │   ├── desktop.py
    │   └── docs.py
    ├── fixtures/                           # JSON fixtures for master data
    │   ├── industry_vertical.json
    │   ├── media_category.json
    │   ├── ad_format.json
    │   └── kpi_definition.json
    ├── workspace/
    │   └── media_advertising.json
    ├── notification/
    │   ├── campaign_deadline_alert.json
    │   ├── budget_overrun_alert.json
    │   ├── media_invoice_overdue.json
    │   └── creative_approval_request.json
    ├── dashboard/
    │   └── media_advertising_dashboard.json
    ├── dashboard_chart/
    │   ├── campaigns_by_status.json
    │   └── monthly_invoice_value.json
    ├── number_card/
    │   ├── active_campaigns.json
    │   ├── open_media_invoices.json
    │   └── pending_client_approvals.json
    ├── report/
    │   ├── campaign_performance_summary/
    │   ├── budget_vs_actual_report/
    │   ├── media_delivery_report/
    │   └── client_revenue_report/
    ├── campaign_management/
    │   ├── __init__.py
    │   ├── utils.py
    │   └── doctype/
    │       ├── campaign/
    │       ├── campaign_brief/
    │       ├── campaign_phase/
    │       ├── ad_placement/
    │       ├── media_plan/
    │       └── media_plan_item/          # child table
    ├── media_operations/
    │   ├── __init__.py
    │   └── doctype/
    │       ├── media_channel/
    │       ├── ad_slot/
    │       ├── ad_booking/
    │       ├── traffic_order/
    │       ├── creative_asset/
    │       └── ad_format/
    ├── client_crm/
    │   ├── __init__.py
    │   └── doctype/
    │       ├── agency_client/
    │       ├── client_brief/
    │       ├── retainer_agreement/
    │       ├── proposal/
    │       └── client_approval/
    ├── billing_finance/
    │   ├── __init__.py
    │   ├── utils.py
    │   └── doctype/
    │       ├── campaign_budget/
    │       ├── campaign_budget_item/     # child table
    │       ├── media_invoice/
    │       ├── media_invoice_item/       # child table
    │       ├── vendor_bill/
    │       ├── commission_entry/
    │       ├── billing_milestone/
    │       └── wip_entry/
    ├── resource_production/
    │   ├── __init__.py
    │   └── doctype/
    │       ├── production_job/
    │       ├── resource_allocation/
    │       ├── timesheet_entry/
    │       ├── freelancer_contract/
    │       └── shoot_schedule/
    ├── reporting_analytics/
    │   ├── __init__.py
    │   ├── utils.py
    │   └── doctype/
    │       ├── campaign_report/
    │       ├── delivery_report/
    │       ├── budget_vs_actual/
    │       ├── budget_vs_actual_row/     # child table
    │       └── client_dashboard/
    └── masters/
        ├── __init__.py
        └── doctype/
            ├── industry_vertical/
            ├── media_category/
            ├── pricing_template/
            ├── pricing_template_row/     # child table
            ├── target_audience_profile/
            └── kpi_definition/
```

---

## Doctypes Reference

### 🎯 Campaign Management

| Doctype | Series | Submittable | Key Fields |
|---------|--------|-------------|------------|
| **Campaign** | CAMP-.YYYY.- | ✅ | campaign_name, client, status, total_budget, start_date, end_date |
| **Campaign Brief** | BRIEF-.YYYY.- | ❌ | brief_title, campaign, objectives, target_audience |
| **Campaign Phase** | PHASE-.YYYY.- | ❌ | phase_name, campaign, phase_type, start_date, end_date, status |
| **Ad Placement** | ADP-.YYYY.- | ❌ | media_channel, ad_format, rate, quantity, total_cost (auto) |
| **Media Plan** | MP-.YYYY.- | ❌ | plan_title, campaign, media_plan_items (child) |
| **Media Plan Item** | — (child) | — | media_channel, rate, quantity, total_cost |

### 📺 Media Operations

| Doctype | Series | Submittable | Key Fields |
|---------|--------|-------------|------------|
| **Media Channel** | By name | ❌ | channel_name, media_category, channel_type |
| **Ad Slot** | SLOT-.YYYY.- | ❌ | media_channel, rate, slot_date, availability_status |
| **Ad Booking** | BOOK-.YYYY.- | ✅ | campaign, ad_slot, negotiated_rate, agency_commission_pct, net_rate |
| **Traffic Order** | TO-.YYYY.- | ✅ | ad_booking, media_channel, air_date, creative_asset |
| **Creative Asset** | CA-.YYYY.- | ❌ | asset_name, campaign, asset_type, status, file_attachment |
| **Ad Format** | By name | ❌ | format_name, media_category, duration_seconds, dimensions |

### 👥 Client CRM

| Doctype | Series | Submittable | Key Fields |
|---------|--------|-------------|------------|
| **Agency Client** | CLT-.YYYY.- | ❌ | client_name, industry_vertical, gstin, customer (link to ERPNext) |
| **Client Brief** | CB-.YYYY.- | ❌ | brief_title, client, requirements, status |
| **Retainer Agreement** | RET-.YYYY.- | ✅ | client, monthly_fee, start_date, end_date |
| **Proposal** | PROP-.YYYY.- | ❌ | proposal_title, client, total_value, status |
| **Client Approval** | APPV-.YYYY.- | ❌ | approval_type, campaign, status |

### 💰 Billing & Finance

| Doctype | Series | Submittable | Key Fields |
|---------|--------|-------------|------------|
| **Campaign Budget** | CBUD-.YYYY.- | ❌ | campaign, total_budget, actual_spend, utilisation_pct (auto) |
| **Campaign Budget Item** | — (child) | — | media_channel, allocated, actual, variance |
| **Media Invoice** | MINV-.YYYY.- | ✅ | client, campaign, invoice_items, total_amount |
| **Media Invoice Item** | — (child) | — | description, quantity, rate, amount, tax |
| **Vendor Bill** | VB-.YYYY.- | ✅ | vendor_name, supplier, campaign, amount |
| **Commission Entry** | COM-.YYYY.- | ❌ | campaign, gross_media_value, commission_pct, commission_amount |
| **Billing Milestone** | BMS-.YYYY.- | ❌ | campaign, due_date, amount, status |
| **WIP Entry** | WIP-.YYYY.- | ❌ | campaign, wip_amount, invoiced_amount, balance_wip |

### 🧑‍🎨 Resource & Production

| Doctype | Series | Submittable | Key Fields |
|---------|--------|-------------|------------|
| **Production Job** | PROD-.YYYY.- | ✅ | job_title, campaign, job_type, assigned_to, estimated_hours |
| **Resource Allocation** | RESA-.YYYY.- | ❌ | employee, campaign, from_date, to_date, allocated_hours |
| **Timesheet Entry** | TSE-.YYYY.- | ❌ | employee, campaign, entry_date, hours, billable, billable_amount |
| **Freelancer Contract** | FLC-.YYYY.- | ✅ | freelancer_name, campaign, rate_type, rate |
| **Shoot Schedule** | SHOOT-.YYYY.- | ❌ | shoot_title, campaign, shoot_date, location, status |

### 📊 Reporting & Analytics

| Doctype | Series | Submittable | Key Fields |
|---------|--------|-------------|------------|
| **Campaign Report** | RPT-.YYYY.- | ❌ | campaign, total_impressions, grp_achieved, budget_spent |
| **Delivery Report** | DR-.YYYY.- | ❌ | campaign, booked_impressions, delivered_impressions, delivery_pct |
| **Budget vs Actual** | BVA-.YYYY.- | ❌ | campaign, total_budget, total_actual, variance, channel_rows |
| **Budget vs Actual Row** | — (child) | — | media_channel, budgeted, actual, variance |
| **Client Dashboard** | CD-.YYYY.- | ❌ | client, active_campaigns, total_spend_ytd (auto-computed) |

### ⚙️ Masters

| Doctype | Naming | Key Fields |
|---------|--------|------------|
| **Industry Vertical** | By vertical_name | vertical_name, is_active |
| **Media Category** | By category_name | category_name, category_type |
| **Pricing Template** | PT-.YYYY.- | media_channel, ad_format, base_rate, pricing_rows |
| **Pricing Template Row** | — (child) | min_quantity, max_quantity, rate |
| **Target Audience Profile** | By profile_name | age_group, gender, income_bracket, interests |
| **KPI Definition** | By kpi_name | kpi_name, kpi_code, kpi_type, formula, unit |

---

## Reports

| Report Name | Type | Ref DocType | Key Metrics |
|-------------|------|-------------|-------------|
| **Campaign Performance Summary** | Script | Campaign | Budget, actual spend, utilisation %, GRPs, placements |
| **Budget vs Actual Report** | Script | Campaign Budget | By channel: budgeted vs actual, variance |
| **Media Delivery Report** | Script | Delivery Report | Impressions, GRPs, reach, frequency, delivery % |
| **Client Revenue Report** | Script | Media Invoice | Gross revenue, commission, net, outstanding by client |

### Running Reports

Navigate to **Media Advertising Workspace → Reports** or:
```
http://your-site/app/query-report/Campaign Performance Summary
```

---

## Workspace & Dashboard

The **Media Advertising** workspace is auto-installed and provides:
- Shortcuts to all key doctypes
- Sections grouped by module (Campaign Management, Media Operations, Billing, Reporting)
- Quick access to all 4 script reports

**Number Cards:**
- Active Campaigns (count, status = Active)
- Open Media Invoices (count, submitted, unpaid)
- Pending Client Approvals (count)

**Charts:**
- Campaigns by Status (Donut)
- Monthly Invoice Value (Bar, time series)

---

## Notifications

| Notification | Trigger | Recipients |
|--------------|---------|------------|
| **Campaign Deadline Alert** | 3 days before end_date, status = Active | Account Manager |
| **Budget Overrun Alert** | utilisation_pct > 90 (value change) | Accounts Manager role |
| **Media Invoice Overdue** | Days after due_date, status = Submitted | Accounts Manager role |
| **Creative Approval Request** | Status changes to "In Review" | System Manager role |

Import notifications:
```bash
bench --site your-site.localhost import-doc \
  apps/media_advertising/media_advertising/notification/campaign_deadline_alert.json
```

---

## Scheduled Tasks

Defined in `hooks.py`:

```python
scheduler_events = {
    "daily": [
        "media_advertising.campaign_management.utils.check_campaign_deadlines",
        "media_advertising.billing_finance.utils.check_billing_milestones",
    ],
    "weekly": [
        "media_advertising.reporting_analytics.utils.generate_weekly_reports",
    ],
}
```

Trigger manually for testing:
```bash
bench --site your-site.localhost execute \
  media_advertising.campaign_management.utils.check_campaign_deadlines
```

---

## Fixtures & Default Data

Fixtures are auto-loaded on `bench migrate` if registered in `hooks.py`:

```python
fixtures = [
    "Industry Vertical",
    "Media Category",
    "Ad Format",
    "KPI Definition",
]
```

Includes:
- **10** Industry Verticals (FMCG, Auto, Tech, BFSI, etc.)
- **11** Media Categories (TV, Radio, Print, Digital, OOH, Cinema)
- **13** Ad Formats (30s TVC, Leaderboard, Social, OOH, etc.)
- **7** KPI Definitions (GRP, CPM, CPC, CTR, Reach, Frequency, ROAS)

Export fixtures after customisation:
```bash
bench --site your-site.localhost export-fixtures --app media_advertising
```

---

## ERPNext Integration Points

| Media Advertising | ERPNext |
|-------------------|---------|
| Agency Client → `customer` | Customer |
| Vendor Bill → `purchase_invoice` | Purchase Invoice |
| Media Invoice → `sales_invoice` | Sales Invoice (auto-created via `billing_finance.utils.create_sales_invoice`) |
| Campaign → `project` | Project |
| Resource Allocation → `employee` | Employee |
| Timesheet Entry → `employee` | Employee |

### Creating a Sales Invoice from Media Invoice
1. Submit the Media Invoice
2. Click **Create → Sales Invoice** button
3. The Agency Client must have `customer` field set to a valid ERPNext Customer

---

## Common Errors & Fixes

### `ModuleNotFoundError` on bench migrate
**Cause:** Missing `__init__.py` files  
**Fix:** Every directory (module, doctype, each individual doctype folder) needs an `__init__.py`

```bash
find apps/media_advertising -type d | while read d; do
  touch "$d/__init__.py"
done
```

### `Module 'Media Advertising' not found`
**Cause:** `modules.txt` is missing or has wrong content  
**Fix:** `media_advertising/modules.txt` must contain exactly:
```
Media Advertising
```
The string must match `"module": "Media Advertising"` in every doctype JSON.

### DocType JSON `module` field mismatch
**Cause:** The `module` field in the JSON doesn't match `modules.txt`  
**Fix:** All doctype JSONs in this app use `"module": "Media Advertising"`

### Child table not recognised
**Cause:** Child DocType JSON missing `"istable": 1`  
**Fix:** All child doctypes (Media Plan Item, Campaign Budget Item, etc.) have `"istable": 1`

### `Cannot find module` for whitelisted methods
**Cause:** Method path in `hooks.py` doesn't match actual Python path  
**Fix:** Use exact dotted path matching the file structure, e.g.:
```python
"media_advertising.campaign_management.doctype.campaign.campaign.on_submit"
```

### `NameError: name 'frappe' is not defined` in scheduled task
**Cause:** Forgot `import frappe` at top of utils.py  
**Fix:** Add `import frappe` in every utility file

### Notification not firing
**Cause:** Notification JSON not imported into DB  
**Fix:** Import via bench:
```bash
bench --site site.localhost import-doc apps/media_advertising/media_advertising/notification/campaign_deadline_alert.json
```

### `Link` field pointing to non-existent DocType
**Cause:** Typo or wrong DocType name in `options` field  
**Fix:** Use the exact `name` field from the target DocType's JSON

### `Series` naming not working
**Cause:** `naming_rule` not set to `"By \"Naming Series\" field"`  
**Fix:** Ensure the doctype JSON has:
```json
"naming_rule": "By \"Naming Series\" field"
```
AND the `naming_series` field has `"fieldtype": "Series"` with the desired pattern.

### `field_order` references a field not in `fields`
**Cause:** field_order list is out of sync with fields list  
**Fix:** Run `bench --site site.localhost migrate` after correcting the JSON

### `Attach Image` field not saving thumbnail
**Cause:** Using `"fieldtype": "Attach"` instead of `"fieldtype": "Attach Image"`  
**Fix:** Creative Asset thumbnail uses `"fieldtype": "Attach Image"`

---

## Development Guide

### Adding a new Doctype

1. Create directory: `media_advertising/<module>/doctype/<snake_name>/`
2. Add `__init__.py`
3. Create `<snake_name>.json` — **must include** `"module": "Media Advertising"` and `"naming_rule"`
4. Create `<snake_name>.py` with class inheriting `Document`
5. Create `<snake_name>.js` (can be `{}` if no custom JS needed)
6. Run `bench --site site.localhost migrate`
7. Run `bench build --app media_advertising`

### Adding a new Report

1. Create directory: `media_advertising/report/<report_name>/`
2. Add `<report_name>.json` with `"report_type": "Script Report"` and `"is_standard": "Yes"`
3. Add `<report_name>.py` with `execute(filters)` returning `(columns, data)`
4. Add `<report_name>.js` with `frappe.query_reports["Report Name"] = { filters: [] }`
5. Run `bench --site site.localhost migrate`

### Adding a new Notification

1. Create `media_advertising/notification/<name>.json`
2. Run `bench --site site.localhost import-doc path/to/file.json`
   OR add to fixtures and run `migrate`

### Code Style

- Python: follow PEP 8, use `frappe.throw()` for user-facing errors, `frappe.msgprint()` for warnings
- JavaScript: use `frappe.ui.form.on("DocType", { ... })` pattern
- Always validate dates: `if end_date < start_date: frappe.throw(...)`
- Auto-calculated fields: set `"read_only": 1` in JSON, calculate in `validate()`

---

## Git Setup

### Initialise repo

```bash
cd /path/to/media_advertising
git init
git add .
git commit -m "feat: initial Media Advertising ERP app"
```

### Recommended branch strategy

```
main          — production-ready releases
develop       — integration branch
feature/*     — individual feature work
fix/*         — bug fixes
```

### .gitignore (included)

```
*.pyc
__pycache__/
*.swp
.DS_Store
node_modules/
dist/
*.egg-info/
```

### Pushing to GitHub/GitLab

```bash
git remote add origin https://github.com/your-org/media_advertising.git
git branch -M main
git push -u origin main
```

### CI: minimal bench test

```yaml
# .github/workflows/ci.yml
name: CI
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Validate JSON
        run: python -m json.tool $(find . -name "*.json" | head -50) > /dev/null
```

---

## License

MIT — see LICENSE file.
