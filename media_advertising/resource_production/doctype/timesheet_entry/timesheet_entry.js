frappe.ui.form.on("Timesheet Entry", {
    hours(frm) { frm.trigger("calc"); },
    hourly_rate(frm) { frm.trigger("calc"); },
    billable(frm) { frm.trigger("calc"); },
    calc(frm) {
        if (frm.doc.billable) {
            frm.set_value("billable_amount", (frm.doc.hours || 0) * (frm.doc.hourly_rate || 0));
        } else {
            frm.set_value("billable_amount", 0);
        }
    },
});
