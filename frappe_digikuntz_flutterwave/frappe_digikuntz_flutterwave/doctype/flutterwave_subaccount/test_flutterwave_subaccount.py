# Copyright (c) 2026, Digikuntz and Contributors
# See license.txt

# import frappe
from frappe.tests import IntegrationTestCase


# On IntegrationTestCase, the doctype test records and all
# link-field test record dependencies are recursively loaded
# Use these module variables to add/remove to/from that list
EXTRA_TEST_RECORD_DEPENDENCIES = []  # eg. ["User"]
IGNORE_TEST_RECORD_DEPENDENCIES = []  # eg. ["User"]



class IntegrationTestFlutterwaveSubAccount(IntegrationTestCase):
	"""
	Integration tests for FlutterwaveSubAccount.
	Use this class for testing interactions between multiple components.
	"""

	pass
