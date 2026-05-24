import requests
import frappe
import frappe_digikuntz_flutterwave.services.utils as utils_func


class FlutterwaveClient:

    def __init__(self):
        self.settings = frappe.get_single("Flutterwave Settings")
        self.base_url = "https://api.flutterwave.com/v3"
        self.secret_key = self.settings.get_password("secret_key")


    @property
    def headers(self):
        return {
            "Authorization": f"Bearer {self.secret_key}",
            "Content-Type": "application/json"
        }

    def initialize_web_payment(
        self,
        amount,
        email,
        tx_ref,
        redirect_url,
        currency="XAF",
        company = None,
        customer_name=None
    ):
    
        payload = {
            "tx_ref": tx_ref,
            "amount": amount,
            "currency": currency,
            "redirect_url": redirect_url,
            "customer": {
                "email": email,
                "name": customer_name or email
            },
            "customizations": {
                "title": "ERPNext Payment",
                "description": "Invoice Payment"
            }
        }

        if utils_func.shoudl_use_subaccount(company):
            payload["subaccounts"]= {
                "id": company.custom_sous_compte_par_defaut
            }

        try:
            response = requests.post(
                f"{self.base_url}/payments",
                json=payload,
                headers=self.headers
            )            
            data = {**response.json(), "status_code": "success"}
            print("Web payment initialization response: ", data)
        except requests.exceptions.HTTPError as http_err:
            data = {"status_code": "error", "message": str(http_err)}
        return data

    def initialize_mobile_money_payment(
        self,
        amount,
        email,
        tx_ref,
        redirect_url,
        phone_number,
        network,
        country="CM",
        currency="XAF",
        company = None,
        customer_name=None
    ):
    
        payload = {
            "tx_ref": tx_ref,
            "amount": amount,
            "currency": currency,
            "country": country,
            "email": email,
            "phone_number": phone_number,
            "fullname": customer_name or email,
            "network": network,
            "redirect_url": redirect_url
        }

        if utils_func.shoudl_use_subaccount(company):
            payload["subaccounts"]= {
                "id": company.custom_sous_compte_par_defaut
            }

        try:
            response = requests.post(
                f"{self.base_url}/charges?type=mobile_money_franco",
                json=payload,
                headers=self.headers
            )            
            data = {**response.json(), "status_code": "success"}
        except requests.exceptions.HTTPError as http_err:
            data = {"status_code": "error", "message": str(http_err)}
        return data
    

    def verify_transaction(self,transaction_id):
        try:
            response = requests.get(
                f"{self.base_url}/transactions/{transaction_id}/verify",
                headers=self.headers
            )
            data = {**response.json(), "status_code": "success"}
        except requests.exceptions.HTTPError as http_err:
            data = {"status_code": "error", "message": str(http_err)}

        return data
    

    def verify_transaction_by_reference(self,reference):
        try:
            response = requests.get(
                f"{self.base_url}/transactions/verify_by_reference?tx_ref={reference}",
                headers=self.headers
            )
            data = {**response.json(), "status_code": "success"}
        except requests.exceptions.HTTPError as http_err:
            data = {"status_code": "error", "message": str(http_err)}

        return data
    

    def create_subaccount(self, company,account_bank,account_number,business_email):
        payload = {
            "account_bank": account_bank,
            "account_number": account_number,
            "business_name": company.company_name,
            "business_email": business_email,
            "split_type": "percentage",
            "split_value": 0
        }
        response = requests.post(
            f"{self.base_url}/subaccounts",
            json=payload,
            headers=self.headers
        )
        return response.json()
    
    def get_all_subaccount(self):
        response = requests.get(
            f"{self.base_url}/subaccounts",
            headers=self.headers
        )
        return response.json()


    def get_banks(self, country):

        response = requests.get(f"{self.base_url}/banks/{country}",headers=self.headers)

        return response.json()
    
