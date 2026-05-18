# Copyright (c) 2024, Your Company
# For license information, please see license.txt

import frappe
from frappe import _


def execute(filters=None):
    columns = get_columns()
    data = get_data(filters or {})
    return columns, data


def get_columns():
    return [
        {"label": _("Campaign"), "fieldname": "campaign", "fieldtype": "Link", "options": "Campaign", "width": 200},
        {"label": _("Client"), "fieldname": "client", "fieldtype": "Link", "options": "Agency Client", "width": 150},
        {"label": _("Status"), "fieldname": "status", "fieldtype": "Data", "width": 100},
        {"label": _("Start Date"), "fieldname": "start_date", "fieldtype": "Date", "width": 100},
        {"label": _("End Date"), "fieldname": "end_date", "fieldtype": "Date", "width": 100},
        {"label": _("Total Budget"), "fieldname": "total_budget", "fieldtype": "Currency", "width": 130},
        {"label": _("Actual Spend"), "fieldname": "actual_spend", "fieldtype": "Currency", "width": 130},
        {"label": _("Utilisation %"), "fieldname": "utilisation_pct", "fieldtype": "Percent", "width": 110},
        {"label": _("Placements"), "fieldname": "placements", "fieldtype": "Int", "width": 100},
        {"label": _("GRPs Achieved"), "fieldname": "grps", "fieldtype": "Float", "width": 120},
    ]


def get_data(filters):
    conditions = "WHERE 1=1"
    values = {}

    if filters.get("client"):
        conditions += " AND c.client = %(client)s"
        values["client"] = filters["client"]
    if filters.get("status"):
        conditions += " AND c.status = %(status)s"
        values["status"] = filters["status"]
    if filters.get("from_date"):
        conditions += " AND c.start_date >= %(from_date)s"
        values["from_date"] = filters["from_date"]
    if filters.get("to_date"):
        conditions += " AND c.end_date <= %(to_date)s"
        values["to_date"] = filters["to_date"]

    campaigns = frappe.db.sql(
        f"""
        SELECT
            c.name AS campaign,
            c.client,
            c.status,
            c.start_date,
            c.end_date,
            c.total_budget,
            COALESCE(cb.actual_spend, 0) AS actual_spend,
            COALESCE(cb.utilisation_pct, 0) AS utilisation_pct,
            (SELECT COUNT(*) FROM `tabAd Placement` WHERE campaign = c.name) AS placements,
            COALESCE(cr.grp_achieved, 0) AS grps
        FROM `tabCampaign` c
        LEFT JOIN `tabCampaign Budget` cb ON cb.campaign = c.name
        LEFT JOIN `tabCampaign Report` cr ON cr.campaign = c.name
        {conditions}
        ORDER BY c.start_date DESC
        """,
        values,
        as_dict=True,
    )
    return campaigns
