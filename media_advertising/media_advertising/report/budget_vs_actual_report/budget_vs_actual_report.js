frappe.query_reports["Budget vs Actual Report"] = {
    filters: [
        {fieldname: "campaign", label: __("Campaign"), fieldtype: "Link", options: "Campaign"},
        {fieldname: "client", label: __("Client"), fieldtype: "Link", options: "Agency Client"},
    ],
};
