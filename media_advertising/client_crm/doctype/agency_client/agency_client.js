frappe.ui.form.on("Agency Client", {
    refresh(frm) {
        if (!frm.is_new()) {
            frm.add_custom_button(__("View Campaigns"), () => {
                frappe.set_route("List", "Campaign", { client: frm.doc.name });
            });
        }
    },
});
