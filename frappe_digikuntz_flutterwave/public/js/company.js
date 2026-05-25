// frappe.ui.form.on("Company", {

//     refresh(frm) {

//         if (!frm.doc.custom_activer) {
//             return;
//         }

//         // PAS encore synchronisé
//         if (!frm.doc.custom_id_du_compte) {

//             frm.add_custom_button( __("Sync Flutterwave"),() => sync_flutterwave(frm) );

//         } else {

//             frm.dashboard.add_comment(
//                 __( "Flutterwave subaccount connected: {0}", [frm.doc.custom_id_du_compte]),
//                 "green",
//                 true
//             );

//         }

//     }

// });


function sync_flutterwave(frm) {   
    frappe.call({
        method: "frappe_digikuntz_flutterwave.api.company.sync_flutterwave_company",
        args: {
            company: frm.doc.name,
        },
        freeze: true,
        freeze_message: __("Sync Flutterwave subaccount..."),
        callback(e) {
            // console.log("R ",e,e.exc)
            if (!e.exc) {
                if (e.message && e.message.status=="success")
                {
                    frappe.show_alert({
                        message: __("Flutterwave synchronized"),
                        indicator: "green"
                    });
                    frm.reload_doc();
                }
                else if(e.message && e.message.status=="error")
                {
                    frappe.show_alert({
                        message: __(e.message.message),
                        indicator: "red"
                    });
                }
                else
                {
                    frappe.msgprint({
                        title: __('Erreur'),
                        message: e.message.error || __('An error occured'),
                        indicator: 'red'
                    });
                }
                
            }
            else {
                frappe.msgprint({
                    title: __('Erreur'),
                    message: e.message.error || __('An error occured'),
                    indicator: 'red'
                });
            }

        }

    });

}


frappe.ui.form.on("Company", {
    refresh(frm) {
        // frm.dashboard.add_comment(
        //     __( "Flutterwave subaccount connected: "),"green",true
        // );

        if (!frm.doc.custom_activer) {
            return;
        }      
        frm.add_custom_button( __("Sync Flutterwave"),() => sync_flutterwave(frm) );
    }

});