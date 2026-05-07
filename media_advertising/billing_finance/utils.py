import frappe
from frappe import _
from frappe.utils import nowdate, getdate


def check_billing_milestones():
    """Scheduled: Daily — flag due milestones."""
    today = getdate(nowdate())
    milestones = frappe.db.get_all(
        "Billing Milestone",
        filters={"status": "Pending", "invoiced": 0},
        fields=["name", "milestone_name", "campaign", "client", "due_date", "amount"],
    )
    for m in milestones:
        if getdate(m.due_date) <= today:
            frappe.db.set_value("Billing Milestone", m.name, "status", "Due")
            frappe.publish_realtime(
                "milestone_due",
                {"message": f"Billing Milestone {m.milestone_name} is due for {m.campaign}"},
                user=frappe.session.user,
            )


def create_sales_invoice(media_invoice):
    """Create an ERPNext Sales Invoice from a Media Invoice."""
    mi = frappe.get_doc("Media Invoice", media_invoice)
    if mi.sales_invoice:
        frappe.throw(_("Sales Invoice {0} already created").format(mi.sales_invoice))

    ac = frappe.get_doc("Agency Client", mi.client)
    if not ac.customer:
        frappe.throw(
            _("Agency Client {0} is not linked to an ERPNext Customer.").format(mi.client)
        )

    si = frappe.new_doc("Sales Invoice")
    si.customer = ac.customer
    si.posting_date = mi.invoice_date
    si.due_date = mi.due_date
    si.currency = mi.currency or "INR"

    for item in mi.invoice_items:
        si.append("items", {
            "item_name": item.description,
            "description": item.description,
            "qty": item.quantity or 1,
            "rate": item.rate or 0,
            "amount": item.amount or 0,
        })

    si.insert(ignore_permissions=True)
    mi.db_set("sales_invoice", si.name)
    return si.name
