from frappe.model.document import Document


class TimesheetEntry(Document):
    def validate(self):
        if self.billable:
            self.billable_amount = (self.hours or 0) * (self.hourly_rate or 0)
        else:
            self.billable_amount = 0
