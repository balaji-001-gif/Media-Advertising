import frappe
from frappe.model.document import Document


class ProductionJob(Document):
    def validate(self):
        if self.start_date and self.end_date and self.end_date < self.start_date:
            frappe.throw("End Date cannot be before Start Date")

    def on_submit(self):
        self.db_set("status", "In Progress")
