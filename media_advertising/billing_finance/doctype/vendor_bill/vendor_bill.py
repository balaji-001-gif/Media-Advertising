from frappe.model.document import Document


class VendorBill(Document):
    def validate(self):
        self.total_amount = (self.amount or 0) + (self.tax_amount or 0)
