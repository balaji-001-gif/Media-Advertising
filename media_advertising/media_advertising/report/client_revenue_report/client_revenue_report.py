import frappe
from frappe import _


def execute(filters=None):
    return get_columns(), get_data(filters or {})


def get_columns():
    return [
        {"label": _("Client"), "fieldname": "client", "fieldtype": "Link", "options": "Agency Client", "width": 180},
        {"label": _("Industry"), "fieldname": "industry_vertical", "fieldtype": "Link", "options": "Industry Vertical", "width": 140},
        {"label": _("Invoice Count"), "fieldname": "invoice_count", "fieldtype": "Int", "width": 110},
        {"label": _("Gross Revenue"), "fieldname": "gross_revenue", "fieldtype": "Currency", "width": 130},
        {"label": _("Commission"), "fieldname": "commission", "fieldtype": "Currency", "width": 120},
        {"label": _("Net Revenue"), "fieldname": "net_revenue", "fieldtype": "Currency", "width": 130},
        {"label": _("Paid"), "fieldname": "paid_amount", "fieldtype": "Currency", "width": 120},
        {"label": _("Outstanding"), "fieldname": "outstanding", "fieldtype": "Currency", "width": 120},
    ]


def get_data(filters):
    conditions = "WHERE mi.docstatus = 1"
    values = {}
    if filters.get("client"):
        conditions += " AND mi.client = %(client)s"
        values["client"] = filters["client"]
    if filters.get("from_date"):
        conditions += " AND mi.invoice_date >= %(from_date)s"
        values["from_date"] = filters["from_date"]
    if filters.get("to_date"):
        conditions += " AND mi.invoice_date <= %(to_date)s"
        values["to_date"] = filters["to_date"]

    return frappe.db.sql(
        f"""
        SELECT
            mi.client,
            ac.industry_vertical,
            COUNT(mi.name) AS invoice_count,
            SUM(mi.gross_amount) AS gross_revenue,
            SUM(mi.gross_amount * 0.15) AS commission,
            SUM(mi.net_amount) AS net_revenue,
            SUM(CASE WHEN mi.status = 'Paid' THEN mi.total_amount ELSE 0 END) AS paid_amount,
            SUM(CASE WHEN mi.status != 'Paid' THEN mi.total_amount ELSE 0 END) AS outstanding
        FROM `tabMedia Invoice` mi
        LEFT JOIN `tabAgency Client` ac ON ac.name = mi.client
        {conditions}
        GROUP BY mi.client
        ORDER BY gross_revenue DESC
        """,
        values,
        as_dict=True,
    )
