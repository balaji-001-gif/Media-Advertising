import frappe
from frappe.model.document import Document


class ResourceAllocation(Document):
    def validate(self):
        if self.from_date and self.to_date and self.to_date < self.from_date:
            frappe.throw("To Date cannot be before From Date")
