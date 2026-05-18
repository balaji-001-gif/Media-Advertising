import frappe
from frappe import _


def execute(filters=None):
    return get_columns(), get_data(filters or {})


def get_columns():
    return [
        {"label": _("Campaign"), "fieldname": "campaign", "fieldtype": "Link", "options": "Campaign", "width": 180},
        {"label": _("Client"), "fieldname": "client", "fieldtype": "Link", "options": "Agency Client", "width": 140},
        {"label": _("Channel"), "fieldname": "media_channel", "fieldtype": "Link", "options": "Media Channel", "width": 140},
        {"label": _("Budgeted"), "fieldname": "budgeted", "fieldtype": "Currency", "width": 120},
        {"label": _("Actual"), "fieldname": "actual", "fieldtype": "Currency", "width": 120},
        {"label": _("Variance"), "fieldname": "variance", "fieldtype": "Currency", "width": 120},
        {"label": _("Variance %"), "fieldname": "variance_pct", "fieldtype": "Percent", "width": 100},
    ]


def get_data(filters):
    conditions = "WHERE 1=1"
    values = {}
    if filters.get("campaign"):
        conditions += " AND cb.campaign = %(campaign)s"
        values["campaign"] = filters["campaign"]
    if filters.get("client"):
        conditions += " AND cb.client = %(client)s"
        values["client"] = filters["client"]

    return frappe.db.sql(
        f"""
        SELECT
            cb.campaign,
            cb.client,
            cbi.media_channel,
            cbi.allocated AS budgeted,
            cbi.actual,
            (cbi.allocated - cbi.actual) AS variance,
            CASE WHEN cbi.allocated > 0
                 THEN ROUND(((cbi.allocated - cbi.actual) / cbi.allocated) * 100, 2)
                 ELSE 0 END AS variance_pct
        FROM `tabCampaign Budget` cb
        JOIN `tabCampaign Budget Item` cbi ON cbi.parent = cb.name
        {conditions}
        ORDER BY cb.campaign, cbi.media_channel
        """,
        values,
        as_dict=True,
    )
