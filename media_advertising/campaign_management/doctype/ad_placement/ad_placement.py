import frappe
from frappe.model.document import Document


class AdPlacement(Document):
    def validate(self):
        if self.start_date and self.end_date and self.end_date < self.start_date:
            frappe.throw("End Date cannot be before Start Date")
        self.total_cost = (self.rate or 0) * (self.quantity or 1)
