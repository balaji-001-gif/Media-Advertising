frappe.ui.form.on("Media Invoice", {
    refresh(frm) {
        if (frm.doc.docstatus === 1 && !frm.doc.sales_invoice) {
            frm.add_custom_button(__("Create Sales Invoice"), () => {
                frappe.call({
                    method: "media_advertising.billing_finance.utils.create_sales_invoice",
                    args: { media_invoice: frm.doc.name },
                    callback(r) {
                        if (r.message) frappe.set_route("Form", "Sales Invoice", r.message);
                    }
                });
            });
        }
    },
});
