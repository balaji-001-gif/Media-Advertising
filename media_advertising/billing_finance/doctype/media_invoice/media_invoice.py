import frappe
from frappe import _
from frappe.model.document import Document


class MediaInvoice(Document):
    def validate(self):
        self.gross_amount = sum((r.amount or 0) for r in (self.invoice_items or []))
        self.tax_amount = sum((r.tax_amount or 0) for r in (self.invoice_items or []))
        self.total_amount = self.gross_amount + self.tax_amount

    def on_submit(self):
        self.db_set("status", "Submitted")


def on_submit(doc, method=None):
    pass
