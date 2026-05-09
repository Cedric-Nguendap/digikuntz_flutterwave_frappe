import frappe

from frappe_digikuntz_flutterwave.integrations.flutterwave_client import FlutterwaveClient

from frappe_digikuntz_flutterwave.services.flutterwave_service import (
    FlutterwaveService
)



@frappe.whitelist()
def test_payment():

    client = FlutterwaveClient()

    return client.initialize_payment(
        amount=100,
        email="test@example.com",
        tx_ref="TEST-001",
        redirect_url="https://google.com"
    )


@frappe.whitelist()
def create_payment_link( sales_invoice ):

    service = FlutterwaveService()
    print("Sales invoices ",sales_invoice)


    return service.create_invoice_payment(
        sales_invoice
    )