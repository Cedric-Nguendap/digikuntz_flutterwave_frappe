import frappe

from frappe_digikuntz_flutterwave.services.flutterwave_service import (
    FlutterwaveService
)

@frappe.whitelist()
def sync_flutterwave_company(company):


    service = FlutterwaveService()

    response = service.sync_subaccount()

    if response.get("status")!="success":
        return {
            "status":"error",
            "message":response.get("message")
        }
    print("Response sync flutterwave ",response)
    data = response.get("data", {})

    company_doc = frappe.get_doc("Company",company)
    company_doc.set("custom_sous_compte_disponible", [])
	
    for d in data:
        company_doc.append("custom_sous_compte_disponible", {
            "subaccount_id": d["subaccount_id"],
            "bank_name": d["bank_name"],
            "pourcentance": d["split_value"],
            "business_name":d["business_name"],
            "country":d["country"],
        })
    company_doc.save()

    company_doc.save(ignore_permissions=True)

    frappe.db.commit()

    return {
        "status": "success"
    }