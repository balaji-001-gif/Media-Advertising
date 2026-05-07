import frappe
from frappe import _
from frappe.model.document import Document


class AgencyClient(Document):
    def validate(self):
        if self.email and not frappe.utils.validate_email_address(self.email):
            frappe.throw(_("Invalid Email Address: {0}").format(self.email))
