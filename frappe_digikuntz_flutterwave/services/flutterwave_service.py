import frappe

from frappe_digikuntz_flutterwave.integrations.flutterwave_client import (
    FlutterwaveClient
)


class FlutterwaveService:

    def __init__(self):

        self.client = FlutterwaveClient()

    def create_invoice_payment(
        self,
        sales_invoice
    ):

        invoice = frappe.get_doc(
            "Sales Invoice",
            sales_invoice
        )

        if invoice.outstanding_amount <= 0:
            frappe.throw("Invoice already paid")

        tx_ref = f"INV-{invoice.name}"

        redirect_url = (
            frappe.utils.get_url()
            + "/flutterwave-payment-success"
        )

        response = self.client.initialize_payment(
            amount=invoice.outstanding_amount,
            email=invoice.contact_email  or frappe.session.user,
            tx_ref=tx_ref,
            redirect_url=redirect_url,
            customer_name=invoice.customer_name,
            currency=invoice.currency
        )

        if response.get("status") != "success":
            frappe.throw(
                response.get("message")
                or "Flutterwave payment initialization failed"
            )

        payment_link = response["data"]["link"]

        return {
            "payment_link": payment_link,
            "tx_ref": tx_ref
        }