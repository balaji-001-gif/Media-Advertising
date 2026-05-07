import frappe
from frappe import _


def execute(filters=None):
    return get_columns(), get_data(filters or {})


def get_columns():
    return [
        {"label": _("Campaign"), "fieldname": "campaign", "fieldtype": "Link", "options": "Campaign", "width": 180},
        {"label": _("Media Channel"), "fieldname": "media_channel", "fieldtype": "Link", "options": "Media Channel", "width": 140},
        {"label": _("Delivery Date"), "fieldname": "delivery_date", "fieldtype": "Date", "width": 110},
        {"label": _("Booked Impressions"), "fieldname": "booked_impressions", "fieldtype": "Int", "width": 140},
        {"label": _("Delivered Impressions"), "fieldname": "delivered_impressions", "fieldtype": "Int", "width": 150},
        {"label": _("Delivery %"), "fieldname": "delivery_pct", "fieldtype": "Percent", "width": 100},
        {"label": _("Booked GRPs"), "fieldname": "booked_grps", "fieldtype": "Float", "width": 110},
        {"label": _("Delivered GRPs"), "fieldname": "delivered_grps", "fieldtype": "Float", "width": 120},
        {"label": _("Reach"), "fieldname": "reach", "fieldtype": "Int", "width": 100},
        {"label": _("Frequency"), "fieldname": "frequency", "fieldtype": "Float", "width": 100},
    ]


def get_data(filters):
    conditions = "WHERE 1=1"
    values = {}
    if filters.get("campaign"):
        conditions += " AND dr.campaign = %(campaign)s"
        values["campaign"] = filters["campaign"]
    if filters.get("from_date"):
        conditions += " AND dr.delivery_date >= %(from_date)s"
        values["from_date"] = filters["from_date"]
    if filters.get("to_date"):
        conditions += " AND dr.delivery_date <= %(to_date)s"
        values["to_date"] = filters["to_date"]

    return frappe.db.sql(
        f"""
        SELECT
            dr.campaign, dr.media_channel, dr.delivery_date,
            dr.booked_impressions, dr.delivered_impressions, dr.delivery_pct,
            dr.booked_grps, dr.delivered_grps, dr.reach, dr.frequency
        FROM `tabDelivery Report` dr
        {conditions}
        ORDER BY dr.delivery_date DESC
        """,
        values,
        as_dict=True,
    )
