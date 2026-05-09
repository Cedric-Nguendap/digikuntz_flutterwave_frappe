import frappe

def execute():
    create_mode_of_payment()


def create_mode_of_payment():

    if not frappe.db.exists("Mode of Payment", "Flutterwave"):
        mop = frappe.get_doc({
            "doctype": "Mode of Payment",
            "mode_of_payment": "Flutterwave",
            "type": "General",
            "enabled": 1,
            "accounts": [
                {
                    "company": frappe.defaults.get_global_default("company"),
                    "default_account": get_or_create_account()
                }
            ]
        })

        mop.insert(ignore_permissions=True)


def get_or_create_account():

    account_name = "Flutterwave Wallet"
    company = frappe.defaults.get_global_default("company")

    if frappe.db.exists("Account", account_name):
        return account_name

    # récupérer un parent valide dynamiquement
    parent = frappe.db.get_value(
        "Account",
        {
            "account_name": "Current Assets",
            "company": company
        },
        "name"
    )

    if not parent:
        # fallback plus robuste
        parent = frappe.db.get_value(
            "Account",
            {
                "is_group": 1,
                "company": company
            },
            "name"
        )

    if not parent:
        frappe.throw("No valid parent account found for Flutterwave Wallet")

    account = frappe.get_doc({
        "doctype": "Account",
        "account_name": account_name,
        "parent_account": parent,
        "account_type": "Bank",
        "company": company,
        "is_group": 0
    })

    account.insert(ignore_permissions=True)

    return account.name
