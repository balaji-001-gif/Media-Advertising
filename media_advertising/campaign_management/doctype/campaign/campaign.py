# Copyright (c) 2024, Your Company and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import getdate, nowdate


class Campaign(Document):
    # -----------------------------------------------------------
    # Lifecycle hooks
    # -----------------------------------------------------------
    def validate(self):
        self.validate_dates()
        self.validate_budget()

    def on_submit(self):
        self.db_set("status", "Active")
        self.notify_account_manager()

    def on_cancel(self):
        self.db_set("status", "Cancelled")

    # -----------------------------------------------------------
    # Private helpers
    # -----------------------------------------------------------
    def validate_dates(self):
        if self.start_date and self.end_date:
            if getdate(self.end_date) < getdate(self.start_date):
                frappe.throw(_("End Date cannot be before Start Date"))
        if self.start_date and getdate(self.start_date) < getdate(nowdate()):
            # Only warn, not block — campaigns can be backdated
            frappe.msgprint(
                _("Start Date {0} is in the past").format(self.start_date),
                indicator="orange",
            )

    def validate_budget(self):
        if self.total_budget and self.total_budget <= 0:
            frappe.throw(_("Total Budget must be greater than zero"))

    def notify_account_manager(self):
        if not self.account_manager:
            return
        frappe.sendmail(
            recipients=[self.account_manager],
            subject=_("Campaign {0} is now Active").format(self.campaign_name),
            message=_(
                "Campaign <b>{0}</b> for client <b>{1}</b> has been submitted and is now active."
            ).format(self.campaign_name, self.client),
        )

    # -----------------------------------------------------------
    # Whitelisted API methods
    # -----------------------------------------------------------
    @frappe.whitelist()
    def get_campaign_summary(self):
        """Return budget utilisation and phase count for dashboard."""
        phases = frappe.db.count("Campaign Phase", {"campaign": self.name})
        placements = frappe.db.count("Ad Placement", {"campaign": self.name})
        spent = (
            frappe.db.get_value(
                "Campaign Budget",
                {"campaign": self.name},
                "sum(actual_spend)",
            )
            or 0
        )
        return {
            "phases": phases,
            "placements": placements,
            "spent": spent,
            "budget": self.total_budget,
            "utilisation_pct": round((spent / self.total_budget) * 100, 2)
            if self.total_budget
            else 0,
        }
