import frappe

from frappe_digikuntz_flutterwave.services.flutterwave_service import (
    FlutterwaveService
)

@frappe.whitelist()
def sync_flutterwave_company(company,banque_de_reglement,account_number):

    company_doc = frappe.get_doc("Company", company)

    if company_doc.custom_id_du_compte:
        return {
            "status": "already_synced"
        }   

    service = FlutterwaveService()

    response = service.create_subaccount(company_doc,banque_de_reglement,account_number)

    print("Response sync flutterwave ",response)
    data = response.get("data", {})

    company_doc.custom_id_du_compte = data.get(
        "subaccount_id"
    )

    company_doc.custom_account_number = data.get(
        "account_number"
    )

    company_doc.custom_banque_de_reglement = data.get(
        "bank_name"
    )

    company_doc.custom_nom_du_compte = company


    company_doc.save(ignore_permissions=True)

    frappe.db.commit()

    return {
        "status": "success"
    }