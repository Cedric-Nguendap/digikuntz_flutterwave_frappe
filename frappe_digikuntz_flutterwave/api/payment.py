import frappe

from frappe_digikuntz_flutterwave.integrations.flutterwave_client import FlutterwaveClient

from frappe_digikuntz_flutterwave.services.flutterwave_service import (
    FlutterwaveService
)


@frappe.whitelist()
def create_payment_link( sales_invoice ):

    service = FlutterwaveService()
    print("Sales invoices ",sales_invoice)


    return service.create_invoice_payment(
        sales_invoice
    )