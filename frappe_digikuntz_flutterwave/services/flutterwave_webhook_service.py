import json
import frappe

from frappe_digikuntz_flutterwave.integrations.flutterwave_client import (
    FlutterwaveClient
)
from erpnext.accounts.doctype.payment_entry.payment_entry import get_payment_entry


class FlutterwaveWebhookService:

    def __init__(self):

        self.settings = frappe.get_single("Flutterwave Setting")
        self.client = FlutterwaveClient()


    def process_successful_payment(self, transaction):

        data = transaction.get("data", {})

        tx_ref = data.get("tx_ref")
        pr_name = frappe.db.get_value( "Payment Request", {"name": tx_ref.replace("PR-", "",1)}, "name")
        pr = frappe.get_doc("Payment Request", pr_name)
        pr.set_as_paid() 
        # amount = data.get("amount")
        # currency = data.get("currency")
        # customer_email = data.get("customer", {}).get("email")

        # if not tx_ref:
        #     frappe.throw("Missing transaction reference")

        # # 1. Trouver la facture liée
        # invoice_name = frappe.db.get_value( "Sales Invoice", {"name": tx_ref.replace("INV-", "",1)}, "name")
        # invoice = frappe.get_doc("Sales Invoice", invoice_name)

        

        # if invoice.docstatus != 1:
        #     frappe.throw("Invoice is not submitted")

        # # 2. Vérifier montant
        # if float(amount) < float(invoice.outstanding_amount):
        #     frappe.throw("Payment amount mismatch")

        # existing = frappe.db.exists(
        #     "Payment Entry",
        #     {"reference_no": data.get("id")}
        # )
        # if existing:
        #     return "Already processed"

        # # 3. Créer Payment Entry standard ERPNext
        # payment_entry = get_payment_entry(
        #     dt="Sales Invoice",
        #     dn=invoice.name
        # )


        # # 4. Ajuster infos
        # payment_entry.mode_of_payment = "Flutterwave"
        # payment_entry.reference_no = data.get("id")
        # payment_entry.reference_date = frappe.utils.today()

        # # 5. Insérer et soumettre
        # payment_entry.insert(ignore_permissions=True)
        # payment_entry.submit()
        # frappe.db.commit()
        # print("Payement entry created: ", payment_entry.name)

        # # 6. Log
        # frappe.logger().info({
        #     "payment_entry_created": payment_entry.name
        # })

        # return payment_entry.name
    
    def process_success_by_transaction_id(self, transaction_id):
        transaction = self.client.verify_transaction(transaction_id)
        return self.process_successful_payment(transaction)

    def handle_transaction_status(self, transaction_id):

        transaction = self.client.verify_transaction(transaction_id)

        status = transaction.get("data", {}).get("status")

        if status == "successful":
            self.process_successful_payment(transaction)

        return status