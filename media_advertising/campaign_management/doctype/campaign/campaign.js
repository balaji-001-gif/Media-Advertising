// Copyright (c) 2024, Your Company and contributors
// For license information, please see license.txt

frappe.ui.form.on("Campaign", {
    refresh(frm) {
        frm.trigger("set_status_indicators");

        if (!frm.is_new()) {
            frm.add_custom_button(__("Campaign Brief"), () => {
                frappe.new_doc("Campaign Brief", { campaign: frm.doc.name });
            }, __("Create"));

            frm.add_custom_button(__("Media Plan"), () => {
                frappe.new_doc("Media Plan", {
                    campaign: frm.doc.name,
                    client: frm.doc.client,
                });
            }, __("Create"));

            frm.add_custom_button(__("Ad Placement"), () => {
                frappe.new_doc("Ad Placement", { campaign: frm.doc.name });
            }, __("Create"));

            frm.add_custom_button(__("Campaign Budget"), () => {
                frappe.new_doc("Campaign Budget", {
                    campaign: frm.doc.name,
                    total_budget: frm.doc.total_budget,
                });
            }, __("Create"));

            // Summary dashboard
            if (frm.doc.docstatus === 1) {
                frm.call("get_campaign_summary").then(r => {
                    if (r.message) {
                        const d = r.message;
                        frm.dashboard.add_indicator(
                            __("Budget Used: {0}%", [d.utilisation_pct]),
                            d.utilisation_pct > 90 ? "red" : d.utilisation_pct > 70 ? "orange" : "green"
                        );
                        frm.dashboard.add_indicator(__("Phases: {0}", [d.phases]), "blue");
                        frm.dashboard.add_indicator(__("Placements: {0}", [d.placements]), "cyan");
                    }
                });
            }
        }
    },

    set_status_indicators(frm) {
        const map = {
            Draft: "gray", Planning: "blue", Active: "green",
            "On Hold": "orange", Completed: "cyan", Cancelled: "red",
        };
        if (frm.doc.status) {
            frm.set_indicator_formatter("status", () => map[frm.doc.status] || "gray");
        }
    },

    start_date(frm) {
        if (frm.doc.start_date && frm.doc.end_date) {
            if (frm.doc.end_date < frm.doc.start_date) {
                frappe.msgprint(__("End Date cannot be before Start Date"));
                frm.set_value("end_date", "");
            }
        }
    },

    total_budget(frm) {
        if (frm.doc.total_budget <= 0) {
            frappe.msgprint(__("Total Budget must be positive"));
        }
    },
});
