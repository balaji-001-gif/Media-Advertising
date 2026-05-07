import frappe
from frappe.model.document import Document


class CampaignBrief(Document):
    def validate(self):
        if self.due_date and self.brief_date and self.due_date < self.brief_date:
            frappe.throw("Due Date cannot be before Brief Date")
