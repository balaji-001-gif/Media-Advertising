from frappe.model.document import Document


class BudgetvsActual(Document):
    def validate(self):
        self.total_budget = sum((r.budgeted or 0) for r in (self.channel_rows or []))
        self.total_actual = sum((r.actual or 0) for r in (self.channel_rows or []))
        self.variance = self.total_budget - self.total_actual
        self.variance_pct = (
            round((self.variance / self.total_budget) * 100, 2) if self.total_budget else 0
        )
