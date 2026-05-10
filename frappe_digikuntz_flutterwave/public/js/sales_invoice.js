frappe.ui.form.on('Sales Invoice', {
    refresh: function(frm) {

        if (frm.doc.docstatus === 1 && frm.doc.outstanding_amount > 0) {

            frm.add_custom_button(__('Pay with Flutterwave'), function() {

                frappe.call({
                    method: "frappe_digikuntz_flutterwave.api.payment.create_payment_link",
                    args: {
                        sales_invoice: frm.doc.name
                    },
                    callback: function(r) {

                        if (r.message && r.message.payment_link) {

                            window.open(r.message.payment_link, "_blank");

                        } else {

                            frappe.msgprint("Failed to create payment link");
                        }
                    }
                });

            }, __("Payment"));
        }
    }
});