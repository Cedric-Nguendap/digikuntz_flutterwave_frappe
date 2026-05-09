import requests
import frappe


class FlutterwaveClient:

    def __init__(self):

        self.settings = frappe.get_single("Flutterwave Setting")

        self.base_url = "https://api.flutterwave.com/v3"

        self.secret_key = self.settings.get_password("secret_key")

    @property
    def headers(self):

        return {
            "Authorization": f"Bearer {self.secret_key}",
            "Content-Type": "application/json"
        }

    def initialize_payment(
        self,
        amount,
        email,
        tx_ref,
        redirect_url,
        currency="XAF",
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

        response = requests.post(
            f"{self.base_url}/payments",
            json=payload,
            headers=self.headers
        )

        return response.json()

    
    def verify_transaction(self,transaction_id):

        response = requests.get(
            f"{self.base_url}/transactions/{transaction_id}/verify",
            headers=self.headers
        )

        return response.json()