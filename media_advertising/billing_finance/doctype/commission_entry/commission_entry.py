from frappe.model.document import Document


class CommissionEntry(Document):
    def validate(self):
        self.commission_amount = (self.gross_media_value or 0) * (
            (self.commission_pct or 0) / 100
        )
