frappe.ui.form.on("Commission Entry", {
    gross_media_value(frm) { frm.trigger("calc"); },
    commission_pct(frm) { frm.trigger("calc"); },
    calc(frm) {
        frm.set_value("commission_amount",
            (frm.doc.gross_media_value || 0) * ((frm.doc.commission_pct || 0) / 100)
        );
    },
});
