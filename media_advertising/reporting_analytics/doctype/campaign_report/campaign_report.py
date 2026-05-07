from frappe.model.document import Document


class CampaignReport(Document):
    def validate(self):
        if self.budget_allocated and self.budget_allocated > 0:
            self.roi = round(
                ((self.budget_allocated - (self.budget_spent or 0)) / self.budget_allocated) * 100, 2
            )
