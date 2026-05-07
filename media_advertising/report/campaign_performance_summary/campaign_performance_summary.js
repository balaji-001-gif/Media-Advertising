frappe.query_reports["Campaign Performance Summary"] = {
    filters: [
        {fieldname: "client", label: __("Client"), fieldtype: "Link", options: "Agency Client"},
        {fieldname: "status", label: __("Status"), fieldtype: "Select",
         options: "\nDraft\nPlanning\nActive\nOn Hold\nCompleted\nCancelled"},
        {fieldname: "from_date", label: __("From Date"), fieldtype: "Date"},
        {fieldname: "to_date", label: __("To Date"), fieldtype: "Date"},
    ],
    formatter(value, row, column, data, default_formatter) {
        value = default_formatter(value, row, column, data);
        if (column.fieldname === "utilisation_pct") {
            const pct = data.utilisation_pct || 0;
            const color = pct > 90 ? "red" : pct > 70 ? "orange" : "green";
            value = `<span style="color:${color};font-weight:bold">${value}</span>`;
        }
        return value;
    },
};
