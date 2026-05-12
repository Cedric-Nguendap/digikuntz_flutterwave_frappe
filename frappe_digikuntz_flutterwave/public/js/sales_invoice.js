// frappe.ui.form.on('Sales Invoice', {
//     refresh: function(frm) {

//         if (frm.doc.docstatus === 1 && frm.doc.outstanding_amount > 0) {

//             frm.add_custom_button(__('Pay with Flutterwave'), function() {

//                 frappe.call({
//                     method: "frappe_digikuntz_flutterwave.api.payment.create_payment_link",
//                     freeze: true,
//                     freeze_message: __("Generating payment link..."),
//                     args: {
//                         sales_invoice: frm.doc.name
//                     },
//                     callback: function(r) {

//                         if (r.message && r.message.payment_link) {

//                             // window.open(r.message.payment_link, "_blank");
//                             frappe.msgprint({
//                                 title: __('Notification'),
//                                 message: __('Lien de paiement créé <b/><br/>{0}', [r.message.payment_link]),
//                                 primary_action: {
//                                 'label': 'Copier le lien',
//                                 action: function() {
//                                     navigator.clipboard.writeText(r.message.payment_link)
//                                         .then(function() {
//                                             frappe.show_alert({ message:__('Lien copié dans le press-papier'), indicator:'green' }, 5);
//                                         })
//                                     }
//                                 }
//                             });

//                         } else {

//                             frappe.msgprint("Failed to create payment link");
//                         }
//                     }
//                 });

//             }, __("Payment"));
//         }
//     }
// });