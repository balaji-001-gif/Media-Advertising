from frappe.model.document import Document


class TrafficOrder(Document):
    def on_submit(self):
        self.db_set("status", "Sent")
