// Copyright (c) 2026, Digikuntz and contributors
// For license information, please see license.txt

frappe.listview_settings['Flutterwave Bank'] = {
	refresh(listview) {
        listview.page.add_inner_button( "Sync Banks", () => {

            frappe.call({
                method: "frappe_digikuntz_flutterwave.api.flutterwave_bank.sync_flutterwave_banks",
                freeze: true,
                freeze_message: __("Syncing banks...")
            });

        })
    }
};
