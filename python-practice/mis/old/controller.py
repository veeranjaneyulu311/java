from flask import Flask, jsonify, request
from dao import *


app = Flask(__name__)

'''
@app.errorhandler(Exception)
def exception_handler(error):
    print(error)
    response = {'responseCode': RES_CODE_FAILURE, 'responseMessage': OPERATION_FAILED_GENERIC_MESSAGE, 'validations':{'errCode': RES_CODE_OFG001,'errMessage': OPERATION_FAILED_GENERIC_MESSAGE}, 'data':''}
    return jsonify(response), 500

hello_args = {"orgId": fields.Str(required=True)}
'''


@app.route('/fetchBranchWisePatientCount', methods=['POST'])
def fetch_branch_wise_patient_count():
        request_data = request.get_json()
        query_response = fetch_branch_wise_patient_count_dao(request_data)
        return jsonify(query_response[0]), query_response[1]


@app.route('/fetchBranchWisePatientVisitCount', methods=['POST'])
def fetch_branch_wise_patient_visit_count():
        request_data = request.get_json()
        query_response = fetch_branch_wise_patient_visit_count_dao(request_data)
        return jsonify(query_response[0]), query_response[1]


@app.route('/fetchBranchPatientCount', methods=['POST'])
def fetch_branch_patient_count():
        request_data = request.get_json()
        query_response = fetch_branch_patient_count_dao(request_data)
        return jsonify(query_response[0]), query_response[1]


@app.route('/fetchBranchPatientVisitCount', methods=['POST'])
def fetch_branch_patient_visit_count():
        request_data = request.get_json()
        query_response = fetch_branch_patient_visit_count_dao(request_data)
        return jsonify(query_response[0]), query_response[1]


@app.route('/fetchOrgWiseTopTenDiseases', methods=['POST'])
def fetch_org_wise_top_ten_diseases():
        request_data = request.get_json()
        query_response = fetch_org_wise_top_ten_diseases_dao(request_data)
        return jsonify(query_response[0]), query_response[1]


@app.route('/fetchOrgWiseTopTenDrugBrandQty', methods=['POST'])
def fetch_org_wise_top_ten_drug_brand_qty():
        request_data = request.get_json()
        query_response = fetch_org_wise_top_ten_drug_brand_qty_dao(request_data)
        return jsonify(query_response[0]), query_response[1]


@app.route('/fetchTopTenSellingDrugBrands', methods=['POST'])
def fetch_top_ten_selling_drug_brands():
        request_data = request.get_json()
        query_response = fetch_top_ten_selling_drug_brands_dao(request_data)
        return jsonify(query_response[0]), query_response[1]


@app.route('/fetchDoctorWiseConsultationsCount', methods=['POST'])
def fetch_doctor_wise_consultations_count():
        request_data = request.get_json()
        query_response = fetch_doctor_wise_consultations_count_dao(request_data)
        return jsonify(query_response[0]), query_response[1]


@app.route('/fetchOrgWiseNearExpireDrugs', methods=['POST'])
def fetch_org_wise_near_expire_drugs():
        request_data = request.get_json()
        query_response = fetch_org_wise_near_expire_drugs_dao(request_data)
        return jsonify(query_response[0]), query_response[1]


@app.route('/fetchPharmacyCurrentInventory', methods=['POST'])
def fetch_pharmacy_current_inventory():
        request_data = request.get_json()
        query_response = fetch_pharmacy_current_inventory_dao(request_data)
        return jsonify(query_response[0]), query_response[1]


# PHANI"S APIS
# (1)API For TOTAL BILLS##
@app.route('/OrgGrpWiseInvoiceCountPool', methods=['POST'])
def fetch_org_grp_wise_invoice_count_dao_pool():
        request_data = request.get_json()
        query_response = fetch_org_grp_wise_invoice_count_dao(request_data)
        return jsonify(query_response[0]), query_response[1]


# (1(b))API For Organization Wise Invoice Count##
@app.route('/fetchOrgWiseInvoiceCountPool', methods=['POST'])
def fetch_org_wise_invoice_count_dao_pool():
        request_data = request.get_json()
        query_response = fetch_org_wise_invoice_count_dao(request_data)
        return jsonify(query_response[0]), query_response[1]


# (2)API For IPD REVENUE##
@app.route('/OrgGrpWiseIpdCollectionsPool', methods=['POST'])
def fetch_org_grp_wise_Ipd_Collections_dao_pool():
        request_data = request.get_json()
        query_response = fetch_org_grp_wise_Ipd_Collections_dao(request_data)
        return jsonify(query_response[0]), query_response[1]


# (2(b))API For Organiztion Wise IPD Collections##
@app.route('/fetchOrgWiseIpdCollectionsPool', methods=['POST'])
def fetch_org_wise_ipd_collections_dao_pool():
        request_data = request.get_json()
        query_response = fetch_org_wise_ipd_collections_dao(request_data)
        return jsonify(query_response[0]), query_response[1]


# (3)API For OPD REVENUE##
@app.route('/OrgGrpWiseOPDCollectionPool', methods=['POST'])
def fetch_org_grp_wise_OPD_collections_dao_pool():
        request_data = request.get_json()
        query_response = fetch_org_grp_wise_OPD_collections_dao(request_data)
        return jsonify(query_response[0]), query_response[1]


# (3(b))API For Organization Wise OPD Collections##
@app.route('/fetchOrgWiseOPDCollectionsPool', methods=['POST'])
def fetch_org_wise_opd_collections_dao_pool():
        request_data = request.get_json()
        query_response = fetch_org_wise_opd_collections_dao(request_data)
        return jsonify(query_response[0]), query_response[1]


# (4)API For IPD+OPD+PHARMACY REVENUE##
@app.route('/fetchOrgGrpWiseIpdAndOpdAndPharmacyCollectionsPool', methods=['POST'])
def fetch_org_grpwise_Ipd_and_Opd_and_pharmacy_collections_dao_pool():
        request_data = request.get_json()
        query_response = fetch_org_grpwise_Ipd_and_Opd_and_pharmacy_collections_dao(request_data)
        return jsonify(query_response[0]), query_response[1]


# (4(b))API For Organization Module Wise IPD+OPD+PHARMACY REVENUE##
@app.route('/fetchOrgModuleWiseIpdAndOpdAndPharmacyCollectionsPool', methods=['POST'])
def fetch_org_module_wise_ipd_and_opd_and_pharmacy_collections_dao_pool():
        request_data = request.get_json()
        query_response = fetch_org_module_wise_ipd_and_opd_and_pharmacy_collections_dao(request_data)
        return jsonify(query_response[0]), query_response[1]


# (5)API For IP+OP REVENUE##
@app.route('/BranchWiseCollectionsPool', methods=['POST'])
def fetch_branch_wise_collections_dao_pool():
        request_data = request.get_json()
        query_response = fetch_branch_wise_collections_dao(request_data)
        return jsonify(query_response[0]), query_response[1]


# (5(b))API For Branch Wise IP+OP REVENUE##
@app.route('/fetchBranchCollectionsPool', methods=['POST'])
def fetch_branch_collections_dao_pool():
        request_data = request.get_json()
        query_response = fetch_branch_collections_dao(request_data)
        return jsonify(query_response[0]), query_response[1]


# (6)API For REVENUE GENERATED FOR IPD BEDS##
@app.route('/totalRevenueGeneratedForIPDBedsPool', methods=['POST'])
def total_revenue_generated_for_ipd_beds_dao_pool():
        request_data = request.get_json()
        query_response = total_revenue_generated_for_ipd_beds_dao(request_data)
        return jsonify(query_response[0]), query_response[1]


# (7)API For PHARMACY PROFIT DETAILS##
@app.route('/OrgWisePharmacyProfitsPool', methods=['POST'])
def fetch_org_wise_pharmacy_profits_dao_pool():
        request_data = request.get_json()
        query_response = fetch_org_wise_pharmacy_profits_dao(request_data)
        return jsonify(query_response[0]), query_response[1]


# (8)API For Branch Wise Patient Count Details##
@app.route('/fetchBranchPatientCountPool', methods=['POST'])
def fetch_branch_patient_count_dao_pool():
        request_data = request.get_json()
        query_response = fetch_branch_patient_count_dao(request_data)
        return jsonify(query_response[0]), query_response[1]


# (9)API For Branch Wise Patient Visit Count Details##
@app.route('/fetchBranchPatientVisitCountPool', methods=['POST'])
def fetch_branch_patient_visit_count_dao_pool():
        request_data = request.get_json()
        query_response = fetch_branch_patient_visit_count_dao(request_data)
        return jsonify(query_response[0]), query_response[1]


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
