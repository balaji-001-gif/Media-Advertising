import frappe
from frappe import _
from frappe.model.document import Document


class AdBooking(Document):
    def validate(self):
        self.calculate_net_rate()
        if self.ad_slot:
            self.media_channel = frappe.db.get_value("Ad Slot", self.ad_slot, "media_channel")

    def on_submit(self):
        self.db_set("status", "Confirmed")
        self.update_slot_availability("Booked")
        self.create_traffic_order()

    def on_cancel(self):
        self.db_set("status", "Cancelled")
        self.update_slot_availability("Available")

    def calculate_net_rate(self):
        comm = (self.agency_commission_pct or 0) / 100
        self.net_rate = (self.negotiated_rate or 0) * (1 - comm)

    def update_slot_availability(self, status):
        if self.ad_slot:
            frappe.db.set_value("Ad Slot", self.ad_slot, "availability_status", status)

    def create_traffic_order(self):
        if self.traffic_order:
            return
        to = frappe.new_doc("Traffic Order")
        to.naming_series = "TO-.YYYY.-"
        to.ad_booking = self.name
        to.campaign = self.campaign
        to.media_channel = self.media_channel
        to.air_date = self.air_date
        to.creative_asset = self.creative_asset
        to.insert(ignore_permissions=True)
        self.db_set("traffic_order", to.name)


def after_insert(doc, method=None):
    pass
