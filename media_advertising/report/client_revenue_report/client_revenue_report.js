frappe.query_reports["Client Revenue Report"] = {
    filters: [
        {fieldname: "client", label: __("Client"), fieldtype: "Link", options: "Agency Client"},
        {fieldname: "from_date", label: __("From Date"), fieldtype: "Date"},
        {fieldname: "to_date", label: __("To Date"), fieldtype: "Date"},
    ],
};
