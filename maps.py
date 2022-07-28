from collections import namedtuple

items_table_map = namedtuple("items_table_map", (
"id", "code", "name", "description", "esimate_value", "rental_value", "bundle", "bundle_status", "meters", "hsn",
"material", "missing_estimate_value", "serialized", "unserialized", "consumable", "length", "breadth", "height",
"actual_weight", "vol_weight", "CFT", "item_type", "category", "purchase_code", "supplier", "qr_code", "status",
"created_at", "updated_at"))


jobsite_table_map = namedtuple("jobsite_table_map", ("id","site_name","site_address","city","pincode","lat","lng","coordinates","active_site_count","site_type","site_stage","branch_id","duplicate_job_sites","status","created_at","updated_at","update_status","created_by"))


customer_table_map = namedtuple("customer_table_map", (
    "id", "customer_master_id", "quickbooks_id", "account_manager", "account_receivable",
    "business_development_executive",
    "credit_rating", "first_name", "last_name", "company", "email", "phone_number", "credit_limit", "due_days",
    "outstanding", "billing_address_line", "billing_address_city", "billing_address_pincode", "mailing_address_line",
    "mailing_address_city", "mailing_address_pincode", "gstn", "security_etter", "rental_advance", "rental_order",
    "security_cheque", "customer_form", "notifications", "business_type", "created_at", "updated_at",
    "same_month_billing",
    "bill_submission", "is_verified", "status"))

customer_masters_table_map = namedtuple("customer_masters_table_map", (
    "id", "company", "account_manager", "account_receivable", "email", "phone_number", "credit_limit", "due_days",
    "billing_address_line", "billing_address_city", "billing_address_pincode", "mailing_address_line",
    "mailing_address_city", "mailing_address_pincode", "customer_form", "sap_ref", "first_name", "last_name", "pan",
    "credit_rating", "is_verified", "business_type", "created_at", "updated_at", "status", "bill_submission",
    "security_etter", "rental_advance", "rental_order", "security_cheque", "req_otp", "crm_account_id", "type",
    "open_acc"))

contact_map = namedtuple("contact_map", (
    "id", "crm_id", "contact_name", "customer_id", "designation", "email", "phone_number", "role", "created_at",
    "updated_at"
))

quotation_map = namedtuple("quotation_map", (
    "id", "created_by", "customer_id", "order_id", "contact_name", "phone_number", "site_name", "price_type", "total", "freight", "gstn", "billing_address_line", "billing_address_city", "billing_address_pincode", "delivery_address_line", "delivery_address_city", "delivery_address_pincode", "delivery_date", "pickup_date", "converted_at", "security_amt", "active", "lead_id", "freight_payment","godown_id", "sign_type", "created_at", "updated_at"
))

quotation_items_map = namedtuple("quotation_items_map", ("quotation_id", "item_code", "unit_price", "quantity", "created_at", "updated_at"))

