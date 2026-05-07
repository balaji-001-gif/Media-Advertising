import frappe
from frappe.model.document import Document


class MediaPlan(Document):
    def validate(self):
        self.total_planned_budget = sum(
            (row.total_cost or 0) for row in (self.media_plan_items or [])
        )
