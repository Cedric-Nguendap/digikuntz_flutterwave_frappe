import frappe

def get_current_user_email():
    current_user = frappe.session.user    
    # Do not return 'Administrator' if you are testing in the console 
    if current_user == "Administrator":
        return "choudja@gic.cm" # Or handle as needed
        
    return current_user


def shoudl_use_subaccount(company):
    company_doc = frappe.get_doc("Company", company)
    return company_doc.custom_activer and company_doc.custom_subaccount_bank and company_doc.custom_subaccount_number and company_doc.custom_id_du_compte