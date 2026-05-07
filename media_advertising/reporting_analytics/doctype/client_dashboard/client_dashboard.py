import frappe
from frappe.model.document import Document


class ClientDashboard(Document):
    def validate(self):
        self.refresh_metrics()

    def refresh_metrics(self):
        self.active_campaigns = frappe.db.count(
            "Campaign", {"client": self.client, "status": "Active"}
        )
        self.pending_approvals = frappe.db.count(
            "Client Approval", {"client": self.client, "status": "Pending"}
        )
        self.open_briefs = frappe.db.count(
            "Client Brief", {"client": self.client, "status": "New"}
        )
