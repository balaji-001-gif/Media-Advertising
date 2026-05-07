frappe.ui.form.on("Ad Booking", {
    negotiated_rate(frm) { frm.trigger("calc_net"); },
    agency_commission_pct(frm) { frm.trigger("calc_net"); },
    calc_net(frm) {
        const comm = (frm.doc.agency_commission_pct || 0) / 100;
        frm.set_value("net_rate", (frm.doc.negotiated_rate || 0) * (1 - comm));
    },
    ad_slot(frm) {
        if (frm.doc.ad_slot) {
            frappe.db.get_value("Ad Slot", frm.doc.ad_slot, ["media_channel", "rate"], r => {
                if (r) {
                    frm.set_value("media_channel", r.media_channel);
                    if (!frm.doc.negotiated_rate) frm.set_value("negotiated_rate", r.rate);
                }
            });
        }
    },
});
