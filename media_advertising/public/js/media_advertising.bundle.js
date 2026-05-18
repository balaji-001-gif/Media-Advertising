frappe.provide("media_advertising");
media_advertising = {
    format_currency(amount, currency) {
        return frappe.format(amount, {fieldtype: "Currency", currency: currency || "INR"});
    },
};
