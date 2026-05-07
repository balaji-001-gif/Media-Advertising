frappe.ui.form.on("Ad Placement", {
    rate(frm) { frm.trigger("calc_cost"); },
    quantity(frm) { frm.trigger("calc_cost"); },
    calc_cost(frm) {
        frm.set_value("total_cost", (frm.doc.rate || 0) * (frm.doc.quantity || 1));
    },
});
