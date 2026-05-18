from frappe.model.document import Document


class WIPEntry(Document):
    def validate(self):
        self.balance_wip = (self.wip_amount or 0) - (self.invoiced_amount or 0)
