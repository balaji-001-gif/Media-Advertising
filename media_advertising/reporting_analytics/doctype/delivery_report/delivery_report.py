from frappe.model.document import Document


class DeliveryReport(Document):
    def validate(self):
        if self.booked_impressions and self.booked_impressions > 0:
            self.delivery_pct = round(
                ((self.delivered_impressions or 0) / self.booked_impressions) * 100, 2
            )
