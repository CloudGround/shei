# -*- coding: utf-8 -*-
# Copyright (c) 2015, Frappe Technologies and contributors
# For license information, please see license.txt

import frappe

@frappe.whitelist()
def get_account_for_advance_payment(origin_account):
	return str(frappe.db.get_value("Advance Payment Setup", {'origin_account':origin_account}, "destination_account"))

@frappe.whitelist()
def get_account_for_regulare_payment(destination_account):
	return str(frappe.db.get_value("Advance Payment Setup", {"destination_account":destination_account}, "origin_account"))

@frappe.whitelist()
def get_customer_from_project(project):
        return str(frappe.db.get_value("Project", {"name":project}, "customer"))


@frappe.whitelist()
def get_cheque_series(account):
	#frappe.msgprint(str(account))
	if frappe.db.exists("Cheque Series", account):
		cheque_series = frappe.db.get_value("Cheque Series", account, "cheque_series")
        	cheque_series = int(cheque_series) + 1
		frappe.client.set_value("Cheque Series", account, "cheque_series", int(cheque_series))
		#frappe.msgprint(str(cheque_series))	
		return str(cheque_series)
	else:
		return " "

@frappe.whitelist()
def get_project_deposit(project_name):
	pj = frappe.get_doc("Project", project_name)
	if pj.customer_deposit_item:
		to_remove = []
		for i in pj.get('customer_deposit_item'):
			to_remove.append(i)
		[pj.remove(d) for d in to_remove]
	for i in frappe.get_list("Customer Deposit", fields="name", filters={"project": project_name, "docstatus": 1}):
		cd = frappe.get_doc("Customer Deposit", i.name)
		for i in cd.get('customer_deposit_quotation'):
			pj.append("customer_deposit_item", {
                                "customer_deposit": cd.name,
                                "customer_deposit_invoice": i.quotation,
                                "net_total": i.total_before_taxes,
                                "deposit_reception_date": cd.posting_date				
			})
	pj.save()
#	return cd_list

@frappe.whitelist()
def get_project_adv_paid(project_name):
	if frappe.db.get_value("Customer Deposit", {"project": project_name, "docstatus": 1}, "name"):
		return True
#	total = 0.0
#        for cd in frappe.get_list("Customer Deposit", fields="name", filters={"project": project_name, "docstatus": 1}):
#                total = cd.net_total
#        return str(total)
