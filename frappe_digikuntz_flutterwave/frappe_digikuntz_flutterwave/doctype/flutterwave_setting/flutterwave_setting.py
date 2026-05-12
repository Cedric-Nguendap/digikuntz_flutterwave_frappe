# Copyright (c) 2026, Digikuntz and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe_digikuntz_flutterwave.services.payment_gateway import ( FlutterwavePaymentGateway )


class FlutterwaveSetting(Document):
	supported_currencies = ['NGN', 'GHS', 'ZAR', 'USD','XAF','XOF','EUR','KES']

	def get_payment_url(self, **kwargs):
		gateway = FlutterwavePaymentGateway()
		return gateway.get_payment_url(**kwargs)
	
	
	def validate_transaction_currency(self, currency):
		if currency not in self.supported_currencies:
			frappe.throw(
				_(
					"Please select another payment method. Paystack does not support transactions in currency '{0}'"
				).format(currency)
			)
	
	def get_supported_currency(self):
		return self.supported_currencies

