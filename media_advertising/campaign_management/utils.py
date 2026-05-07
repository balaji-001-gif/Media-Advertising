import frappe
from frappe import _
from frappe.utils import nowdate, add_days


def check_campaign_deadlines():
    """Scheduled: Daily — notify account managers of campaigns ending in 3 days."""
    alert_date = add_days(nowdate(), 3)
    campaigns = frappe.db.get_all(
        "Campaign",
        filters={"status": "Active", "end_date": alert_date},
        fields=["name", "campaign_name", "client", "account_manager", "end_date"],
    )
    for c in campaigns:
        if not c.account_manager:
            continue
        frappe.sendmail(
            recipients=[c.account_manager],
            subject=_("Campaign {0} ending in 3 days").format(c.campaign_name),
            message=_(
                "Campaign <b>{0}</b> for client <b>{1}</b> ends on {2}."
            ).format(c.campaign_name, c.client, c.end_date),
        )
