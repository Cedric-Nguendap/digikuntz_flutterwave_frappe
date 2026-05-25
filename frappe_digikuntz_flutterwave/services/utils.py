import frappe

def get_current_user_email():
    current_user = frappe.session.user    
    # Do not return 'Administrator' if you are testing in the console 
    if current_user == "Administrator":
        return "choudja@gic.cm" # Or handle as needed
        
    return current_user


def shoudl_use_subaccount(company):
    return company.custom_activer and company.custom_sous_compte_par_defaut