frappe.query_reports["Media Delivery Report"] = {
    filters: [
        {fieldname: "campaign", label: __("Campaign"), fieldtype: "Link", options: "Campaign"},
        {fieldname: "from_date", label: __("From Date"), fieldtype: "Date"},
        {fieldname: "to_date", label: __("To Date"), fieldtype: "Date"},
    ],
};
