frappe.ui.form.on("Company", {

    refresh(frm) {

        if (!frm.doc.custom_activer) {
            return;
        }

        // PAS encore synchronisé
        if (!frm.doc.custom_id_du_compte) {

            frm.add_custom_button( __("Sync Flutterwave"),() => sync_flutterwave(frm) );

        } else {

            frm.dashboard.add_comment(
                __( "Flutterwave subaccount connected: {0}", [frm.doc.custom_id_du_compte]),
                "green",
                true
            );

        }

    }

});


function sync_flutterwave(frm) {

    if(!frm.doc.custom_account_number)
    {
        frappe.show_alert({ message:__('Bank account number not defined.'), indicator:'red' });
        return;
    }
    if(!frm.doc.custom_banque_de_reglement)
    {
        frappe.show_alert({ message:__('Bank account not defined.'), indicator:'red' });
        return;
    }

    frappe.call({
        method: "frappe_digikuntz_flutterwave.api.company.sync_flutterwave_company",
        args: {
            company: frm.doc.name,
            banque_de_reglement:frm.doc.custom_banque_de_reglement,
            account_number:frm.doc.custom_account_number
        },

        freeze: true,
        freeze_message: __("Creating Flutterwave subaccount..."),

        callback(r) {

            if (!r.exc) {

                frappe.show_alert({
                    message: __("Flutterwave synchronized"),
                    indicator: "green"
                });

                frm.reload_doc();
            }
            else {
                    frappe.msgprint({
                        title: __('Erreur'),
                        message: r.message.error || __('Impossible de créer le sous compte'),
                        indicator: 'red'
                    });
                }

        }

    });

}