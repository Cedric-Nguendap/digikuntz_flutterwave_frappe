import frappe

from frappe_digikuntz_flutterwave.integrations.flutterwave_client import (
    FlutterwaveClient
)


class FlutterwaveService:

    def __init__(self):

        self.client = FlutterwaveClient()

    def create_payment_link( self, reference_doc, payer_email=None):

        

        if reference_doc.outstanding_amount <= 0:
            frappe.throw("reference_doc already paid")

        tx_ref = f"PR-{reference_doc.name}"

        redirect_url = (
            frappe.utils.get_url()
            + "/flutterwave-payment-success"
        )
        
        email = payer_email or reference_doc.email_to or reference_doc.contact_email or reference_doc.owner
        customer = reference_doc.party or reference_doc.customer_name
        

        # DEBUG TEMPORAIRE
        # email = "tonemail@gmail.com"

        if not email or "@" not in email:
            frappe.throw(
                "Customer email is required for Flutterwave payment"
            )

        response = self.client.initialize_payment(
            amount=reference_doc.outstanding_amount,
            email=email,
            tx_ref=tx_ref,
            redirect_url=redirect_url,
            customer_name=customer,
            currency=reference_doc.currency
        )

        if response.get("status_code") != "success":

            frappe.throw(
                response.get("message")
                or "Flutterwave payment initialization failed"
            )

        return response