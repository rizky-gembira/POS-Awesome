# Copyright (c) 2021, Youssef Restom and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _
from posawesome.posawesome.doctype.referral_code.referral_code import (
    create_referral_code,
)


def after_insert(doc, method):
    create_customer_referral_code(doc)
    create_gift_coupon(doc)


def validate(doc, method):
    validate_referral_code(doc)


def create_customer_referral_code(doc):
    if doc.posa_referral_company:
        company = frappe.get_cached_doc("Company", doc.posa_referral_company)
        if not company.posa_auto_referral:
            return
        create_referral_code(
            doc.posa_referral_company,
            doc.name,
            company.posa_customer_offer,
            company.posa_primary_offer,
            company.posa_referral_campaign,
        )


def create_gift_coupon(doc):
    if doc.posa_referral_code:
        coupon = frappe.new_doc("POS Coupon")
        coupon.customer = doc.name
        coupon.referral_code = doc.posa_referral_code
        coupon.create_coupon_from_referral()


def validate_referral_code(doc):
    referral_code = doc.posa_referral_code
    exist = None
    if referral_code:
        exist = frappe.db.exists("Referral Code", referral_code)
        if not exist:
            exist = frappe.db.exists("Referral Code", {"referral_code": referral_code})
        if not exist:
            frappe.throw(_("This Referral Code {0} not exists").format(referral_code))

@frappe.whitelist()
def check_customer_status(customer):
    """Return enabled/disabled status of customer"""
    if not customer:
        return {"status": "not_found"}

    disabled = frappe.db.get_value("Customer", customer, "disabled")
    customer_name = frappe.db.get_value("Customer", customer, "customer_name")
    gem_poin = frappe.db.get_value("Customer", customer, "gem_poin")

    if "UMUM" not in customer:
        if disabled == 1:
            return {
                "status": "disabled",
                "message": (
                    f"⚠️ Status Member Customer <b><big>{customer_name}</big></b> ({customer}) sudah Berakhir! "
                    f"Silakan perpanjang untuk bisa digunakan kembali.<br>"
                    f"<b><big>Poin Gembira = {gem_poin} poin</big></b>"
                ),
            }
        else:
            return {
                "status": "enabled",
                "message": (
                    f"✅ Customer <b><big>{customer_name}</big></b> ({customer}) aktif dan bisa digunakan.<br>"
                    f"<b><big>Poin Gembira = {gem_poin} poin</big></b>"
                )
            }
