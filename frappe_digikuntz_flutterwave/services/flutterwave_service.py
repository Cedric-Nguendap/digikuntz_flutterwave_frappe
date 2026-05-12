import frappe

from frappe_digikuntz_flutterwave.integrations.flutterwave_client import (
    FlutterwaveClient
)


class FlutterwaveService:

    def __init__(self):

        self.client = FlutterwaveClient()

    def create_payment_link( self, reference_doc):

         # Si Payment Request
        if reference_doc.doctype == "Payment Request":

            invoice = frappe.get_doc(
                reference_doc.reference_doctype,
                reference_doc.reference_name
            )

        else:
            invoice = reference_doc

        if invoice.outstanding_amount <= 0:
            frappe.throw("Invoice already paid")

        tx_ref = f"PR-{invoice.name}"

        redirect_url = (
            frappe.utils.get_url()
            + "/flutterwave-payment-success"
        )

        email = invoice.contact_email or invoice.owner

        # DEBUG TEMPORAIRE
        # email = "tonemail@gmail.com"

        if not email or "@" not in email:
            frappe.throw(
                "Customer email is required for Flutterwave payment"
            )

        response = self.client.initialize_payment(
            amount=invoice.outstanding_amount,
            email=email,
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

        return response