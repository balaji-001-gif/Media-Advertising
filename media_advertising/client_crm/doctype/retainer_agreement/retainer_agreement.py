import frappe
from frappe.model.document import Document


class RetainerAgreement(Document):
    def validate(self):
        if self.start_date and self.end_date and self.end_date <= self.start_date:
            frappe.throw("End Date must be after Start Date")

    def on_submit(self):
        self.db_set("status", "Active")
