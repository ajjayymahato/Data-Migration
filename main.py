#!/usr/bin/python3
import xmlrpc.client
import mysql.connector
from maps import items_table_map, jobsite_table_map, customer_table_map, customer_masters_table_map, contact_map, \
    quotation_map, quotation_items_map

odoo_db = 'newlocaldb3'

betaDB = mysql.connector.connect(
    user='admin', password='', host='beta.ctwij5r61eet.ap-south-1.rds.amazonaws.com', database='youngman',
    port='3306'
)

connLocalBeta = betaDB.cursor()

keys = {
    'local': {
        'url': 'http://localhost:8069',
        'db': odoo_db,
        'username': 'admin',
        'password': ''
    },
    'test': '',
    'prod': ''
}

env = 'local'

url = keys[env]['url']
db = keys[env]['db']
username = keys[env]['username']
password = keys[env]['password']

common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
uid = common.authenticate(db, username, password, {})

models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))


def getContactDesignationId(name):
    ids = models.execute_kw(db, uid, password, 'res.partner.category', 'search', [[['name', '=', name]]], {'limit': 1})
    if len(ids) > 0:
        return ids[0]
    else:
        return models.execute_kw(db, uid, password, 'res.partner.category', 'create', [{'name': name}])


def getCountryId():
    ids = models.execute_kw(db, uid, password, 'res.country', 'search', [[['code', '=', "IN"]]], {'limit': 1})
    if len(ids) > 0:
        return ids[0]
    return False


contact_designation_category_id = getContactDesignationId('Contact Designation')
india_country_id = getCountryId()


def getAllCustomerMasters():
    connLocalBeta.execute("select * from customer_masters")
    customerMasters = connLocalBeta.fetchall()

    customerMastersDS = []

    for customerMasterRow in customerMasters:
        customerMastersDS.append(customer_masters_table_map(*customerMasterRow))

    return customerMastersDS


def getAllbranches(customer_master_id):
    connLocalBeta.execute("select * from customers where customer_master_id = %s", [customer_master_id])
    customers = connLocalBeta.fetchall()

    customersDS = []

    for customer in customers:
        customersDS.append(customer_table_map(*customer))

    return customersDS


def getAllContactsForBranch(beta_customer_id):
    connLocalBeta.execute(
        "SELECT * from contacts where (email is not null or phone_number is null) and customer_id = %s order by id desc",
        [beta_customer_id])
    contacts = connLocalBeta.fetchall()

    contactsDS = []

    for contact in contacts:
        contactsDS.append(contact_map(*contact))

    return contactsDS


def getOdooUserIdFromEmail(email):
    ids = models.execute_kw(db, uid, password, 'res.users', 'search', [[['email', '=', email]]], {'limit': 1})
    if len(ids) > 0:
        return ids[0]
    return False


def getPaymentTermIdFromDays(days):
    ids = models.execute_kw(db, uid, password, 'account.payment.term', 'search_read', [[['name', 'ilike', days]]],
                            {'limit': 1})
    if len(ids) > 0:
        return ids[0]['id']
    return False


def getBetaUserEmailFromId(user_id):
    connLocalBeta.execute("select email from users where id = %s", [user_id])
    email = connLocalBeta.fetchone()
    return email


def getCategoryId(role):
    ids = models.execute_kw(db, uid, password, 'res.partner.category', 'search',
                            [[['name', '=', role], ['parent_id', '=', contact_designation_category_id]]], {'limit': 1})
    if len(ids) > 0:
        return ids[0]
    return models.execute_kw(db, uid, password, 'res.partner.category', 'create',
                             [{'name': role, 'parent_id': contact_designation_category_id}])


def searchContactInOdoo(email, phone, branch_id):
    ids = models.execute_kw(db, uid, password, 'res.partner', 'search',
                            [[['email', '=', email], ['phone', '=', phone], ['parent_id', '=', branch_id]]],
                            {'limit': 1})
    if len(ids) > 0:
        return ids[0]
    return False


def searchOdooCompanyByPan(pan):
    ids = models.execute_kw(db, uid, password, 'res.partner', 'search', [[['vat', 'ilike', pan]]], {'limit': 1})
    if len(ids) > 0:
        return ids[0]
    return False


def searchOdooBranchByGSTN(partner_id, gstn):
    ids = models.execute_kw(db, uid, password, 'res.partner', 'search',
                            [[['parent_id', '=', partner_id], ['gstn', '=', gstn]]], {'limit': 1})
    if len(ids) > 0:
        return ids[0]
    return False


def getTeamId(team_name):
    ids = models.execute_kw(db, uid, password, 'crm.team', 'search',
                            [[['name', '=', team_name]]], {'limit': 1})
    if len(ids) > 0:
        return ids[0]
    return models.execute_kw(db, uid, password, 'crm.team', 'create',
                             [{'name': team_name}])


def getStageId(site_stage):
    ids = models.execute_kw(db, uid, password, 'jobsite_stage', 'search',
                            [[['name', '=', site_stage]]], {'limit': 1})
    if len(ids) > 0:
        return ids[0]
    return models.execute_kw(db, uid, password, 'jobsite_stage', 'create',
                             [{'name': site_stage}])


def getCPLStatus(status):
    if status == "BLOCKED":
        return '1'
    elif status == "UNBLOCKED":
        return '2'
    elif status == "LEGAL":
        return '0'
    else:
        return False


def getProductCategoryId(category_id):
    if category_id is None:
        category_name = "All"
    else:
        connLocalBeta.execute("SELECT name FROM category WHERE id = %s", [category_id])
        result = connLocalBeta.fetchone()
        category_name = result[0]

    ids = models.execute_kw(db, uid, password, 'product.category', 'search',
                            [[['name', '=', category_name]]], {'limit': 1})
    if len(ids) > 0:
        return ids[0]
    return models.execute_kw(db, uid, password, 'product.category', 'create',
                             [{'name': category_name}])


def getProductStatus(status):
    if status == "Active":
        return '0'
    elif status == "Deactive":
        return '1'
    elif status == "Disable":
        return '2'
    else:
        return False


def getJobsiteStatus(status):
    if status == "Active":
        return '0'
    elif status == "Closed":
        return '1'
    elif status == "Virgin":
        return '2'
    else:
        return False


def getCreditRating(rating):
    if rating == "A":
        return '0'
    elif rating == "B":
        return '1'
    elif rating == "C":
        return '2'
    else:
        return False


def prepareCustomerData(customerDS):
    account_manager_email = getBetaUserEmailFromId(customerDS.account_manager)
    account_receivable_email = getBetaUserEmailFromId(customerDS.account_receivable)

    account_manager_odoo_id = False if account_manager_email is None else getOdooUserIdFromEmail(account_manager_email)
    account_receivable_odoo_id = False if account_receivable_email is None else  getOdooUserIdFromEmail(account_receivable_email)

    payment_term_id = getPaymentTermIdFromDays(customerDS.due_days)

    team_id = False  # getTeamId()

    data = {
        'name': customerDS.company,
        'user_id': account_manager_odoo_id,
        'user_recievable_id': account_receivable_odoo_id,
        'email': customerDS.email,
        'email_normalized': customerDS.email,
        'phone': False if customerDS.phone_number is None or customerDS.phone_number == 0 else str(
            customerDS.phone_number),
        'credit_limit': customerDS.credit_limit,
        'property_payment_term_id': payment_term_id,

        'street': False if customerDS.billing_address_line is None else customerDS.billing_address_line,
        'city': False if customerDS.billing_address_city is None else customerDS.billing_address_city,
        'zip': False if customerDS.billing_address_pincode is None else customerDS.billing_address_pincode,

        'mailing_street': False if customerDS.mailing_address_line is None else customerDS.mailing_address_line,
        'mailing_city': False if customerDS.mailing_address_city is None else customerDS.mailing_address_city,
        'mailing_zip': False if customerDS.mailing_address_pincode is None else customerDS.mailing_address_pincode,

        # 'sap_ref': customerDS.sap_ref,
        'credit_rating': False if customerDS.credit_rating is None else getCreditRating(customerDS.credit_rating),
        'cpl_status': False if customerDS.status is None else getCPLStatus(customerDS.status),
        # 'bill_submission': customerDS.bill_submission ==>  Convert freetext to context and provide as dropdown, skip for now
        'security_letter': True if customerDS.security_etter == 1 else False,
        'rental_advance': True if customerDS.rental_advance == 1 else False,
        'rental_order': True if customerDS.rental_order == 1 else False,
        'security_cheque': True if customerDS.security_cheque == 1 else False,

        'create_date': customerDS.created_at,
        'display_name': customerDS.company,
        'lang': 'en_US',
        'credit_limit': False if customerDS.credit_limit is None else str(customerDS.credit_limit),
        'active': 'true',
        'type': 'contact',
        'team_id': team_id,
        'is_company': 'true',
        'in_beta': 'true',
        'color': 0,
        'create_uid': 1,
        'write_uid': 1,
        'message_bounce': 0,
    }
    return data


def saveContactsForBranch(odoo_branch_id, beta_branch_id):
    contacts = getAllContactsForBranch(beta_branch_id)
    sanitized_contacts = {}

    for contact in contacts:

        if contact.email is None and contact.phone_number is None:
            continue

        role = contact.role

        if role is None:
            role = contact.designation

        if contact.email is not None:
            key = contact.email
        else:
            key = contact.phone_number

        if key in sanitized_contacts:
            category_id = getCategoryId(role)
            if category_id not in sanitized_contacts[key]['category_id']:
                sanitized_contacts[key]['category_id'].append(category_id)
        else:
            sanitized_contacts[key] = {
                'name': contact.contact_name,
                'email': False if contact.email is None else contact.email,
                'email_normalized': False if contact.email is None else contact.email,
                'function': False if contact.designation is None else contact.designation,
                'phone': False if contact.phone_number is None or contact.phone_number == 0 else str(
                    contact.phone_number),
                'create_date': contact.created_at,
                'display_name': contact.contact_name,
                'parent_id': odoo_branch_id,
                'category_id': [getCategoryId(role)],
                'lang': 'en_US',
                'active': 'true',
                'type': 'contact',
                'is_company': False,
                'in_beta': 'true',
                'color': 0,
                'create_uid': 1,
                'write_uid': 1,
            }

    for key, contact in sanitized_contacts.items():
        try:
            contact_id = searchContactInOdoo(contact['email'], contact['phone'], odoo_branch_id)
            if contact_id:
                models.execute_kw(db, uid, password, 'res.partner', 'write', [[contact_id], contact])
            else:
                contact_id = models.execute_kw(db, uid, password, 'res.partner', 'create', [contact])
        except:
            print(contact)
            raise Exception("Contact creation failed")


def saveCustomerAndBranchToOdoo(customerMaster, branches):
    data = prepareCustomerData(customerMaster)
    data['vat'] = customerMaster.pan
    data['sap_ref'] = False if customerMaster.sap_ref is None else customerMaster.sap_ref

    id = searchOdooCompanyByPan(customerMaster.pan)

    try:
        if id:
            models.execute_kw(db, uid, password, 'res.partner', 'write', [[id], data])
        else:
            id = models.execute_kw(db, uid, password, 'res.partner', 'create', [data])
    except:
        print(data)
        raise Exception("Customer creation failed")

    for branch in branches:
        if branch.gstn is None:
            continue
        branch_id = searchOdooBranchByGSTN(id, branch.gstn)
        branch_data = prepareCustomerData(branch)
        branch_data['gstn'] = branch.gstn
        branch_data['parent_id'] = id
        branch_data['is_customer_branch'] = True

        # For testing only
        branch_data['name'] = branch.company + " - Branch"
        branch_data['display_name'] = branch.company + " - Branch"

        try:
            if branch_id:
                models.execute_kw(db, uid, password, 'res.partner', 'write', [[branch_id], branch_data])
            else:
                branch_id = models.execute_kw(db, uid, password, 'res.partner', 'create', [branch_data])

            saveContactsForBranch(branch_id, branch.id)

        except:
            print(branch_data)
            raise Exception("Branch creation failed")

    pass


def findItemByCodeInOdoo(item_code):
    ids = models.execute_kw(db, uid, password, 'product.template', 'search', [[['default_code', '=', item_code]]],
                            {'limit': 1})
    if len(ids) > 0:
        return ids[0]
    return False


def getAllItemsInBeta():
    connLocalBeta.execute("select * from items")
    items = connLocalBeta.fetchall()

    itemsDS = []

    for item in items:
        itemsDS.append(items_table_map(*item))

    return itemsDS


def saveItems():
    items = getAllItemsInBeta()

    for item in items:
        item_id = findItemByCodeInOdoo(item.code)

        # TODO: add other fields
        data = {
            'name': str(item.name),
            'default_code': False if item.code is None else str(item.code),
            'description': False if item.description is None else str(item.description),
            'list_price': str(item.rental_value),
            'standard_price': str(item.esimate_value),
            'bundle': True if item.bundle == 1 else False,
            'meters': False if item.meters is None else str(item.meters),
            'l10n_in_hsn_code': False if item.hsn is None else item.hsn,
            'material': False if item.material is None else str(item.material),
            'missing_estimate_value': False if item.missing_estimate_value is None else str(
                item.missing_estimate_value),
            'serialized': True if item.serialized == 1 else False,
            'detailed_type': 'service',
            'consumable': True if item.consumable == 1 else False,
            'length': False if item.length is None else item.length,
            'breadth': False if item.breadth is None else item.breadth,
            'height': False if item.height is None else item.height,
            'actual_weight': False if item.actual_weight is None else item.actual_weight,
            'vol_weight': False if item.vol_weight is None else item.vol_weight,
            'cft': False if item.CFT is None else item.CFT,
            # 'item_type': item.item_type, #to do
            'purchase_code': '0' if item.purchase_code is None else item.purchase_code,
            'supplier': False if item.supplier is None else item.supplier,
            'barcode': False if item.qr_code is None else item.qr_code,
            'status': False if item.status is None else getProductStatus(item.status),
            'categ_id': getProductCategoryId(item.category),
            'sale_ok': True,
            'purchase_ok': True,
        }

        if item_id:
            models.execute_kw(db, uid, password, 'product.template', 'write', [[item_id], data])
        else:
            item_id = models.execute_kw(db, uid, password, 'product.template', 'create', [data])


def getAllJobsitesFromBeta():
    connLocalBeta.execute("select * from job_site")
    jobSites = connLocalBeta.fetchall()

    jobSitessDS = []

    for jobSite in jobSites:
        jobSitessDS.append(jobsite_table_map(*jobSite))

    return jobSitessDS


def findJobSiteByNameInOdoo(name):
    if name is None:
        return False

    ids = models.execute_kw(db, uid, password, 'jobsite', 'search', [[['name', '=', name]]], {'limit': 1})
    if len(ids) > 0:
        return ids[0]
    return False


def saveJobSites():
    jobsites = getAllJobsitesFromBeta()

    for jobsite in jobsites:
        jobsite_id = findJobSiteByNameInOdoo(jobsite.site_name)

        data = {
            'name': jobsite.site_name,
            'street': False if jobsite.site_address is None else jobsite.site_address,
            'city': False if jobsite.city is None else jobsite.city,
            'zip': False if jobsite.pincode is None else jobsite.pincode,
            'latitude': str(jobsite.lat),
            'longitude': str(jobsite.lng),
            # 'branch_id': str(jobsite.branch_id),
            'siteteam': False if getTeamId(jobsite.site_type) is None else getTeamId(jobsite.site_type),  # check
            'stage_id': False if jobsite.site_stage is None else getStageId(jobsite.site_stage),  # check
            # 'beta_godown_id': jobsite.branch_id, #to do
            'status': False if jobsite.status is None else getJobsiteStatus(jobsite.status),
            'create_date': jobsite.created_at,
            'write_date': jobsite.updated_at,
            # 'user_id': ""

        }

        if jobsite_id:
            models.execute_kw(db, uid, password, 'jobsite', 'write', [[jobsite_id], data])
        else:
            jobsite_id = models.execute_kw(db, uid, password, 'jobsite', 'create', [data])


def getAllQuotationsOfCurrentFY():
    connLocalBeta.execute(
        "select * from quotations WHERE order_id is null and MONTH(created_at) >= 4 AND YEAR(created_at) = YEAR(CURRENT_TIMESTAMP)")
    quotations = connLocalBeta.fetchall()

    quotationDS = []

    for quotation in quotations:
        quotationDS.append(quotation_map(*quotation))

    return quotationDS


def getQuotatoinItemsFromBeta(quotation_id):
    connLocalBeta.execute("select * from quotation_items WHERE quotation_id = %s", [quotation_id])
    quotationItems = connLocalBeta.fetchall()

    quotationItemsDS = []

    for quotationItem in quotationItems:
        quotationItemsDS.append(quotation_items_map(*quotationItem))

    return quotationItemsDS


def getFreightPaidBy(freight_payment):
    if freight_payment == "It has been agreed 1st Dispatch and final Pickup will be done by Youngman":
        return "freight_type1"
    elif freight_payment == "It has been agreed 1st Dispatch will be done by Youngman and final Pickup will be done by Customer on his cost":
        return "freight_type2"
    elif freight_payment == "It has been agreed 1st Dispatch will be done by Customer on his cost and final Pickup would be done by Youngman":
        return "freight_type3"
    elif freight_payment == "It has been agreed 1st Dispatch will be done by Customer on his cost and final Pickup is already paid by Customer":
        return "freight_type4"
    elif freight_payment == "It has been agreed 1st Dispatch and final Pickup will be done by Customer on his cost":
        return "freight_type5"
    return False


def getProductIdFromItemCode(item_code):
    ids = models.execute_kw(db, uid, password, 'product.product', 'search', [[['default_code', '=', item_code]]], {'limit': 1})
    return ids[0]



def getBranchIdAndCustomerId(beta_branch_id):
    connLocalBeta.execute(
        "SELECT customer_masters.pan, customers.gstn FROM customers, customer_masters WHERE customer_masters.id = customers.customer_master_id and customers.id = %s",
        [beta_branch_id])
    result = connLocalBeta.fetchone()
    vat = result[0]
    gst = result[1]

    company_id = searchOdooCompanyByPan(vat)
    branch_id = False if gst is None else searchOdooBranchByGSTN(company_id, gst)
    return company_id, branch_id


def saveQuotationsOfCurrentFinancialYear():
    quotations = getAllQuotationsOfCurrentFY()

    for quotation in quotations:
        if quotation.customer_id is None:
            continue

        quotationItems = getQuotatoinItemsFromBeta(quotation.id)

        branch_id, customer_id = getBranchIdAndCustomerId(quotation.customer_id)

        if customer_id is False:
            continue

        data = {
            'partner_id': customer_id,
            'jobsite_id': findJobSiteByNameInOdoo(quotation.site_name),
            # 'godown': False if quotation.godown_id is None else quotation.godown_id,
            'billing_street': quotation.billing_address_line,
            'billing_street2': False if quotation.billing_address_city is None else quotation.billing_address_city,
            'billing_state_id': False,
            'billing_country_id': india_country_id,
            'billing_zip': False if quotation.billing_address_pincode is None else quotation.billing_address_pincode,
            'delivery_street': False if quotation.delivery_address_line is None else quotation.delivery_address_line,
            'delivery_street2': False if quotation.delivery_address_city is None else quotation.delivery_address_city,
            'delivery_state_id': False,
            'delivery_country_id': india_country_id,
            'delivery_zip': False if quotation.delivery_address_pincode is None else quotation.delivery_address_pincode,
            'freight_amount': str(quotation.freight),
            'delivery_date': False if quotation.delivery_date is None else str(quotation.delivery_date),
            'pickup_date': False if quotation.pickup_date is None else str(quotation.pickup_date),
            'security_amount': str(quotation.security_amt),
            'freight_paid_by': getFreightPaidBy(quotation.freight_payment),
            'price_type': False if quotation.price_type == "NA" else quotation.price_type.lower(),
            'purchaser_phone': False if quotation.phone_number is None else str(quotation.phone_number),
            # 'purchaser_name': False if quotation.contact_name is None else quotation.contact_name,
            # 'purchaser_email': False,
            'order_line': []
        }

        for quotationItem in quotationItems:
            data['order_line'].append({
                'order_id': quotationItem.quotation_id,
                'product_id': getProductIdFromItemCode(quotationItem.item_code),
                'price_unit': str(quotationItem.unit_price),
                'product_uom_qty': quotationItem.quantity,
                # 'create_date': quotationItem.created_at,
                # 'write_date': quotationItem.updated_at,

            })


        models.execute_kw(db, uid, password, 'sale.order', 'create', [data])


def process():
    ids = models.execute_kw(db, uid, password, 'sale.order.line', 'search_read', [[['id', '=', 46]]], {'limit': 1})

    # print("Saving jobsites")
    #saveJobSites()
    # print("Saving Items")
    #saveItems()
    #
    # print("Saving customers")
    # for customerMaster in getAllCustomerMasters():
    #     branches = getAllbranches(customerMaster.id)
    #     saveCustomerAndBranchToOdoo(customerMaster, branches)

    saveQuotationsOfCurrentFinancialYear()


process()

connLocalBeta.close()
