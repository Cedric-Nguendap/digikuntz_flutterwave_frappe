from frappe.integrations.utils import create_request_log
import frappe
from frappe_digikuntz_flutterwave.services.flutterwave_service import (
            FlutterwaveService
        )

class FlutterwavePaymentGateway:

    def __init__(self):

        self.settings = frappe.get_single("Flutterwave Setting")

    def get_payment_url(self, **kwargs):

        reference_doctype = kwargs.get("reference_doctype")
        reference_docname = kwargs.get("reference_docname")

        doc = frappe.get_doc(reference_doctype, reference_docname)

        service = FlutterwaveService()

        response  = service.create_payment_link(doc)

        # return payment_link
        return response["data"]["link"]