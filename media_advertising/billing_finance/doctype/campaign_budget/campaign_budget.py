import frappe
from frappe.model.document import Document


class CampaignBudget(Document):
    def validate(self):
        self.actual_spend = sum((r.actual or 0) for r in (self.budget_items or []))
        self.remaining_budget = (self.total_budget or 0) - self.actual_spend
        self.utilisation_pct = (
            round((self.actual_spend / self.total_budget) * 100, 2)
            if self.total_budget
            else 0
        )
        if self.utilisation_pct > 100:
            frappe.msgprint(
                "Budget is over-utilised ({0}%)".format(self.utilisation_pct),
                indicator="red",
            )
