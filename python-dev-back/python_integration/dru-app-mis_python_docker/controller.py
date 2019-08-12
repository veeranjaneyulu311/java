import time
import os
import uuid

from flask_cors import CORS

import dao
import logging
from flask import Flask, jsonify, request
from flasgger import Swagger, APISpec

# logging configuration
logger = logging.getLogger("mislogging")
handler = logging.FileHandler('mis.log')
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.INFO)


app = Flask(__name__)


cors = CORS(app, resources={r"/reports/*": {"origins": "*"}})
app.config['SWAGGER'] = {
    'title': ' MIS Module Apis',
    'description': 'Created by Veeranjaneyulu Nakka, <veeranjaneyulu@dru.care> & Phani Kumar Raviprola, <phanikumar.r@dru.care>',
    'uiversion': 3

}

Swagger(app)


# It stores the UUID for each request
response_token = 0




# It returns the computer name from environment variables. otherwise Unknown Computer
def get_computer_name():
        if os.getenv('HOSTNAME') is not None:
                return os.getenv('HOSTNAME')
        elif os.getenv('COMPUTERNAME') is not None:
                return os.getenv('COMPUTERNAME')
        else:
                return 'Unknown Computer'


#: This method log's the every request given
@app.before_request
def start():
        global response_token
        response_token = str(uuid.uuid4()).upper()
        logger.info("{'transactionId':%s,'systemName':%s,'moduleName':'MIS','timeStamp':%s,'apiName':%s,'status':'START','payLoad':[%s]}",response_token, get_computer_name(), time.strftime('%Y-%m-%d %H:%M:%S'), request.url_rule, request.get_json())


#: This method log's the every request on successful completion
@app.after_request
def end(response):
        response.headers['Response_Token'] = response_token
        if response.status_code == 200:
                logger.info("{'transactionId':%s,'systemName':%s,'moduleName':'MIS','timeStamp':%s,'apiName':%s,'status':'END','payLoad':[%s]}", response_token, get_computer_name(), time.strftime('%Y-%m-%d %H:%M:%S'), request.url_rule, request.get_json())
        return response


#: 1.this api is used to fetch branch wise patient count
@app.route('/reports/fetchBranchWisePatientCount', methods=['POST'])
def fetch_branch_wise_patient_count():
    """
        This api is used to fetch branch wise patient visit count
        Call this api by passing below payload and get branch wise patient visit count
        ---
        tags:
          - Operational
        consumes:
          - application/json
        parameters:
          - in: body
            name: payload
            description: use this payload to get response
            schema:
              type: object
              properties:
                orgId:
                  type: integer
                authenticatedUserId:
                  type: integer
                orgGrpId:
                  type: integer
                  default: "lovely"
                key:
                  type: string
        responses:
          500:
            description: Operation Failed
          200:
            description: Data Fetched Successfully
            schema:
              properties:
                data:
                  type: object
                  properties:
                    branchWiseList:
                      type: array
                      items:
                        type: object
                        properties:
                          name:
                            type: string
                          orgId:
                            type: integer
                          y:
                            type: integer
                  totalCount:
                    type: integer
                responseCode:
                  type: string
                responseMessage:
                  type: string
                validations:
                  type: array
                  items:
                    type: object
                    properties:
                      errCode:
                        type: string
                      message:
                         type: string
       """

    query_response = dao.fetch_branch_wise_patient_count_dao(request, response_token)
    return jsonify(query_response[0]), query_response[1]


#: 2.this api is used to fetch branch wise patient visit count
@app.route('/reports/fetchBranchWisePatientVisitCount', methods=['POST'])
def fetch_branch_wise_patient_visit_count():
        """
            This api is used to fetch branch wise patient visit count
            Call this api by passing below payload and get branch wise patient visit count
            ---
            tags:
              - Operational
            consumes:
              - application/json
            parameters:
              - in: body
                name: payload
                description: use this payload to get response
                schema:
                  type: object
                  properties:
                    orgId:
                      type: integer
                    authenticatedUserId:
                      type: integer
                    orgGrpId:
                      type: integer
                    key:
                      type: string
            responses:
              500:
                description: Operation Failed
              200:
                description: Data Fetched Successfully
                schema:
                  properties:
                    data:
                      type: object
                      properties:
                        branchWiseList:
                          type: array
                          items:
                            type: object
                            properties:
                              name:
                                type: string
                              orgId:
                                type: integer
                              y:
                                type: integer
                        totalCount:
                          type: integer
                    responseCode:
                      type: string
                    responseMessage:
                      type: string
                    validations:
                      type: array
                      items:
                        type: object
                        properties:
                          errCode:
                            type: string
                          message:
                            type: string
         """
        query_response = dao.fetch_branch_wise_patient_visit_count_dao(request, response_token)
        return jsonify(query_response[0]), query_response[1]


#: 3.this api is used to fetch patient count of branch based on key
@app.route('/reports/fetchBranchPatientCount', methods=['POST'])
def fetch_branch_patient_count():
        """
            This api is used to fetch patient count of branch based on key
            Call this api by passing below payload and get patient count of branch
            ---
            tags:
              - Operational
            consumes:
              - application/json
            parameters:
              - in: body
                name: payload
                description: use this payload to get response
                schema:
                  type: object
                  properties:
                    orgId:
                      type: integer
                    authenticatedUserId:
                      type: integer
                    orgGrpId:
                      type: integer
                    key:
                      type: string
            responses:
              500:
                description: Operation Failed
              200:
                description: Data Fetched Successfully
                schema:
                  properties:
                    data:
                      type: object
                      properties:
                        patientCountList:
                          type: array
                          items:
                            type: object
                            properties:
                              name:
                                type: string
                              y:
                                type: integer
                        totalCount:
                          type: integer
                    responseCode:
                      type: string
                    responseMessage:
                      type: string
                    validations:
                      type: array
                      items:
                        type: object
                        properties:
                          errCode:
                            type: string
                          message:
                            type: string
        """
        query_response = dao.fetch_branch_patient_count_dao(request, response_token)
        return jsonify(query_response[0]), query_response[1]


# 4.this api is used to fetch patient count of branch based on key
@app.route('/reports/fetchBranchPatientVisitCount', methods=['POST'])
def fetch_branch_patient_visit_count():
        """
            This api is used to fetch patient count of branch based on key
            Call this api by passing below payload and get patient count of branch based on key
            ---
            tags:
              - Operational
            consumes:
              - application/json
            parameters:
              - in: body
                name: payload
                description: use this payload to get response
                schema:
                  type: object
                  properties:
                    orgId:
                      type: integer
                    authenticatedUserId:
                      type: integer
                    orgGrpId:
                      type: integer
                    key:
                      type: string
            responses:
              500:
                description: Operation Failed
              200:
                description: Data Fetched Successfully
                schema:
                  properties:
                    data:
                      type: object
                      properties:
                        patientCountList:
                          type: array
                          items:
                            type: object
                            properties:
                              name:
                                type: string
                              y:
                                type: integer
                        totalCount:
                          type: integer
                    responseCode:
                      type: string
                    responseMessage:
                      type: string
                    validations:
                      type: array
                      items:
                        type: object
                        properties:
                          errCode:
                            type: string
                          message:
                            type: string
        """

        query_response = dao.fetch_branch_patient_visit_count_dao(request, response_token)
        return jsonify(query_response[0]), query_response[1]


# This api is use to get Top ten diseases in an organisation
@app.route('/reports/fetchOrgWiseTopTenDiseases', methods=['POST'])
def fetch_org_wise_top_ten_diseases():
        """
            This api is used to fetch consultation count based on Doctor
            Call this api by passing below payload and get consultation count based on Doctor
            ---
            tags:
              - Clinical
            consumes:
              - application/json
            parameters:
              - in: body
                name: payload
                description: use this payload to get response
                schema:
                  type: object
                  properties:
                    orgId:
                      type: integer
                    authenticatedUserId:
                      type: integer
                    orgGrpId:
                      type: integer
                    key:
                      type: string
            responses:
              500:
                description: Operation Failed
              200:
                description: Data Fetched Successfully
                schema:
                  properties:
                    data:
                      type: array
                      items:
                        type: object
                        properties:
                          diseaseName:
                            type: integer
                          diseasesCount:
                            type: string
                    responseCode:
                      type: string
                    responseMessage:
                      type: string
                    validations:
                      type: array
                      items:
                        type: object
                        properties:
                          errCode:
                            type: string
                          message:
                            type: string
        """

        query_response = dao.fetch_org_wise_top_ten_diseases_dao(request, response_token)
        return jsonify(query_response[0]), query_response[1]


# This api is used for fetching respected Organisation Module wise inovices
@app.route('/reports/fetchOrgWiseTopTenDrugBrandQty', methods=['POST'])
def fetch_org_wise_top_ten_drug_brand_qty():
        """
            This api is used to fetch consultation count based on Doctor
            Call this api by passing below payload and get consultation count based on Doctor
            ---
            tags:
              - Clinical
            consumes:
              - application/json
            parameters:
              - in: body
                name: payload
                description: use this payload to get response
                schema:
                  type: object
                  properties:
                    orgId:
                      type: integer
                    authenticatedUserId:
                      type: integer
                    orgGrpId:
                      type: integer
                    key:
                      type: string
            responses:
              500:
                description: Operation Failed
              200:
                description: Data Fetched Successfully
                schema:
                  properties:
                    data:
                      type: array
                      items:
                        type: object
                        properties:
                          drugBrandNm:
                            type: integer
                          qty:
                            type: string
                    responseCode:
                      type: string
                    responseMessage:
                      type: string
                    validations:
                      type: array
                      items:
                        type: object
                        properties:
                          errCode:
                            type: string
                          message:
                            type: string
        """
        query_response = dao.fetch_org_wise_top_ten_drug_brand_qty_dao(request, response_token)
        return jsonify(query_response[0]), query_response[1]


# This api is used to fetch consultation count based on Doctor
@app.route('/reports/fetchTopTenSellingDrugBrands', methods=['POST'])
def fetch_top_ten_selling_drug_brands():
        """
            This api is used to fetch consultation count based on Doctor
            Call this api by passing below payload and get consultation count based on Doctor
            ---
            tags:
              - Clinical
            consumes:
              - application/json
            parameters:
              - in: body
                name: payload
                description: use this payload to get response
                schema:
                  type: object
                  properties:
                    orgId:
                      type: integer
                    authenticatedUserId:
                      type: integer
                    orgGrpId:
                      type: integer
                    key:
                      type: string
            responses:
              500:
                description: Operation Failed
              200:
                description: Data Fetched Successfully
                schema:
                  properties:
                    data:
                      type: array
                      items:
                        type: object
                        properties:
                          drugName:
                            type: integer
                          totalAmt:
                            type: string
                    responseCode:
                      type: string
                    responseMessage:
                      type: string
                    validations:
                      type: array
                      items:
                        type: object
                        properties:
                          errCode:
                            type: string
                          message:
                            type: string
        """
        query_response = dao.fetch_top_ten_selling_drug_brands_dao(request, response_token)
        return jsonify(query_response[0]), query_response[1]


# This api is used to fetch consultation count based on Doctor
@app.route('/reports/fetchDoctorWiseConsultationsCount', methods=['POST'])
def fetch_doctor_wise_consultations_count():
        """
            This api is used to fetch consultation count based on Doctor
            Call this api by passing below payload and get consultation count based on Doctor
            ---
            tags:
              - Clinical
            consumes:
              - application/json
            parameters:
              - in: body
                name: payload
                description: use this payload to get response
                schema:
                  type: object
                  properties:
                    orgId:
                      type: integer
                    authenticatedUserId:
                      type: integer
                    orgGrpId:
                      type: integer
                    key:
                      type: string
            responses:
              500:
                description: Operation Failed
              200:
                description: Data Fetched Successfully
                schema:
                  properties:
                    data:
                      type: array
                      items:
                        type: object
                        properties:
                          consultationCount:
                            type: string
                          doctorName:
                            type: integer
                    responseCode:
                      type: string
                    responseMessage:
                      type: string
                    validations:
                      type: array
                      items:
                        type: object
                        properties:
                          errCode:
                            type: string
                          message:
                            type: string
        """
        query_response = dao.fetch_doctor_wise_consultations_count_dao(request, response_token)
        return jsonify(query_response[0]), query_response[1]


# This api is used to fetch list of near expire drug
@app.route('/reports/fetchOrgWiseNearExpireDrugs', methods=['POST'])
def fetch_org_wise_near_expire_drugs():
        """
            This api is used to fetch list of near expire drug
            Call this api by passing below payload and get list of near expire drug
            ---
            tags:
              - Clinical
            consumes:
              - application/json
            parameters:
              - in: body
                name: payload
                description: use this payload to get response
                schema:
                  type: object
                  properties:
                    orgId:
                      type: integer
                    authenticatedUserId:
                      type: integer
                    orgGrpId:
                      type: integer
                    key:
                      type: string
            responses:
              500:
                description: Operation Failed
              200:
                description: Data Fetched Successfully
                schema:
                  properties:
                    data:
                      type: array
                      items:
                        type: object
                        properties:
                          drugBrandName:
                            type: string
                          drugTypeName:
                            type: string
                          expireDt:
                            type: string
                    responseCode:
                      type: string
                    responseMessage:
                      type: string
                    validations:
                      type: array
                      items:
                        type: object
                        properties:
                          errCode:
                            type: string
                          message:
                            type: string
        """
        query_response = dao.fetch_org_wise_near_expire_drugs_dao(request, response_token)
        return jsonify(query_response[0]), query_response[1]


# This api is used to get stock quantity deails from inventory
@app.route('/reports/fetchPharmacyCurrentInventory', methods=['POST'])
def fetch_pharmacy_current_inventory():
        """
            This api is used to get stock quantity deails from inventory
            Call this api by passing below payload and stock quantity deails from inventory
            ---
            tags:
              - Clinical
            consumes:
              - application/json
            parameters:
              - in: body
                name: payload
                description: use this payload to get response
                schema:
                  type: object
                  properties:
                    orgId:
                      type: integer
                    authenticatedUserId:
                      type: integer
                    orgGrpId:
                      type: integer
                    key:
                      type: string
            responses:
              500:
                description: Operation Failed
              200:
                description: Data Fetched Successfully
                schema:
                  properties:
                    data:
                      type: array
                      items:
                        type: object
                        properties:
                          drugBrandName:
                              type: string
                          drugQty:
                              type: integer
                    responseCode:
                      type: string
                    responseMessage:
                      type: string
                    validations:
                      type: array
                      items:
                        type: object
                        properties:
                          errCode:
                            type: string
                          message:
                            type: string
        """

        query_response = dao.fetch_pharmacy_current_inventory_dao(request, response_token)
        return jsonify(query_response[0]), query_response[1]


# PHANI"S APIS
# (1)API For TOTAL BILLS##
@app.route('/reports/fetchOrgGrpWiseInvoiceCount', methods=['POST'])
def fetch_org_grp_wise_invoice_count_dao_pool():
        """
        This api is used to fetch organisation group wise invoice count
        Call this api by passing below fields and organisation group wise invoice count
        ---
        tags:
          - Financial
        consumes:
            application/json
        parameters:
          - in: body
            name: payload
            description: We use this payload to get the required response
            schema:
              type: object
              properties:
                 orgId:
                   type: integer
                 authenticatedUserId:
                   type: integer
                 orgGrpId:
                   type: integer
                 key:
                   type: string
        responses:
         400:
           description: An Error Occured
         200:
           description: Data Fetched Successfully
           schema:
             properties:
               data:
                 type: object
                 properties:
                   branchWiseList:
                    type: array
                    items:
                       type: object
                       properties:
                        drilldown:
                          type: string
                        name:
                          type: string
                        orgId:
                          type: integer
                        y:
                          type: integer
                   totalInvoiceCount:
                    type: integer
               responseCode:
                 type: string
               responseMessage:
                 type: string
               validations:
                 type: array
                 items:
                   type: object
                   properties:
                     errCode:
                        type: string
                     message:
                        type: string
        """
        query_response = dao.fetch_org_grp_wise_invoice_count_dao(request, response_token)
        return jsonify(query_response[0]), query_response[1]


# (1(b))API For Organization Wise Invoice Count##
@app.route('/reports/fetchOrgWiseInvoiceCount', methods=['POST'])
def fetch_org_wise_invoice_count_dao_pool():

        """
        This api is used to fetch organisation wise invoive count
        Call this api by passing below fields and organisation wise invoive count
        ---
        tags:
          - Financial
        consumes:
            application/json
        parameters:
          - in: body
            name: payload
            description: We use this payload to get the required response
            schema:
              type: object
              properties:
                 orgId:
                   type: integer
                 authenticatedUserId:
                   type: integer
                 orgGrpId:
                   type: integer
                 key:
                   type: integer
        responses:
           400:
             description: An Error Occured
           200:
             description: Data Fetched Successfully
             schema:
             properties:
               data:
                 type: object
                 properties:
                   orgLevelInvoicesList:
                    type: array
                    items:
                       type: object
                       properties:
                        drilldown:
                          type: string
                        name:
                          type: string
                        orgId:
                          type: integer
                        startDate:
                           type: none
                        type:
                           type: none
                        y:
                          type: integer
                        yearMonth:
                          type: none
                   totalCount:
                    type: integer
               responseCode:
                 type: string
               responseMessage:
                 type: string
               validations:
                 type: array
                 items:
                   type: object
                   properties:
                     errCode:
                        type: string
                     message:
                        type: string
        """
        query_response = dao.fetch_org_wise_invoice_count_dao(request, response_token)
        return jsonify(query_response[0]), query_response[1]


# (2)API For IPD REVENUE##
@app.route('/reports/fetchOrgGrpWiseIpdCollections', methods=['POST'])
def fetch_org_grp_wise_ipd_collections_dao_pool():

        """
        This api is used to fetch organisation group wise IPD collections count
        Call this api by passing below fields and organisation group wise IPD collections count
        ---
        tags:
          - Financial
        consumes:
            application/json
        parameters:
          - in: body
            name: payload
            description: We use this payload to get the required response
            schema:
              type: object
              properties:
                 orgId:
                   type: integer
                 authenticatedUserId:
                   type: integer
                 orgGrpId:
                   type: integer
                 key:
                   type: string
        responses:
           400:
             description: An Error Occured
           200:
             description: Data Fetched Successfully
             schema:
             properties:
               data:
                 type: object
                 properties:
                   branchWiseList:
                    type: array
                    items:
                       type: object
                       properties:
                        drilldown:
                          type: string
                        name:
                          type: string
                        orgId:
                          type: integer
                        y:
                          type: integer
                   totalCount:
                    type: integer
               responseCode:
                 type: string
               responseMessage:
                 type: string
               validations:
                 type: array
                 items:
                   type: object
                   properties:
                     errCode:
                        type: string
                     message:
                        type: string
        """
        query_response = dao.fetch_org_grp_wise_Ipd_Collections_dao(request, response_token)
        return jsonify(query_response[0]), query_response[1]


# (2(b))API For Organiztion Wise IPD Collections##
@app.route('/reports/fetchOrgWiseIpdCollections', methods=['POST'])
def fetch_org_wise_ipd_collections_dao_pool():
        """
        This api is used to fetch organisation wise IPD collections count
        Call this api by passing below fields and organisation wise IPD collections count
        ---
        tags:
          - Financial
        consumes:
            application/json
        parameters:
          - in: body
            name: payload
            description: We use this payload to get the required response
            schema:
              type: object
              properties:
                 orgId:
                   type: integer
                 authenticatedUserId:
                   type: integer
                 orgGrpId:
                   type: integer
                 key:
                   type: string
        responses:
           400:
             description: An Error Occured
           200:
             description: Data Fetched Successfully
             schema:
                properties:
                   data:
                     type: object
                     properties:
                      orgWiseCollectionsList:
                         type: array
                         items:
                            type: object
                            properties:
                              drilldown:
                                type: string
                              name:
                                type: string
                              orgId:
                                type: integer
                              y:
                                type: integer
                      totalAmount:
                        type: integer
                   responseCode:
                     type: string
                   responseMessage:
                     type: string
                   validations:
                     type: array
                     items:
                       type: object
                       properties:
                        errCode:
                          type: string
                        message:
                          type: string
        """

        query_response = dao.fetch_org_wise_ipd_collections_dao(request, response_token)
        return jsonify(query_response[0]), query_response[1]


# (3)API For OPD REVENUE##
@app.route('/reports/fetchOrgGrpWiseOPDCollection', methods=['POST'])
def fetch_org_grp_wise_opd_collections_dao_pool():
        """
        This api is used to fetch organisation group wise OPD collections count
        Call this api by passing below fields and organisation group wise OPD collections count
        ---
        tags:
          - Financial
        consumes:
            application/json
        parameters:
          - in: body
            name: payload
            description: We use this payload to get the required response
            schema:
              type: object
              properties:
                 orgId:
                   type: integer
                 authenticatedUserId:
                   type: integer
                 orgGrpId:
                   type: integer
                 key:
                   type: string
        responses:
           400:
             description: An Error Occured
           200:
             description: Data Fetched Successfully
             schema:
               properties:
                 data:
                   type: object
                   properties:
                      branchWiseList:
                       type: array
                       items:
                         type: object
                         properties:
                           drilldown:
                             type: string
                           name:
                             type: string
                           orgId:
                             type: integer
                           y:
                             type: integer
                      totalCount:
                        type: integer
                 responseCode:
                   type: string
                 responseMessage:
                   type: string
                 validations:
                   type: array
                   items:
                     type: object
                     properties:
                       errCode:
                        type: string
                       message:
                        type: string
        """

        query_response = dao.fetch_org_grp_wise_OPD_collections_dao(request, response_token)
        return jsonify(query_response[0]), query_response[1]


# (3(b))API For Organization Wise OPD Collections##
@app.route('/reports/fetchOrgWiseOPDCollections', methods=['POST'])
def fetch_org_wise_opd_collections_dao_pool():
        """
        This api is used to fetch organisation wise OPD collections ccount
        Call this api by passing below fields and organisation wise OPD collections ccount
        ---
        tags:
          - Financial
        consumes:
            application/json
        parameters:
          - in: body
            name: payload
            description: We use this payload to get the required response
            schema:
              type: object
              properties:
                 orgId:
                   type: integer
                 authenticatedUserId:
                   type: integer
                 orgGrpId:
                   type: integer
                 key:
                   type: string
        responses:
           400:
             description: An Error Occured
           200:
             description: Data Fetched Successfully
             schema:
                properties:
                   data:
                     type: object
                     properties:
                      orgWiseCollectionsList:
                         type: array
                         items:
                            type: object
                            properties:
                              drilldown:
                                type: string
                              name:
                                type: string
                              orgId:
                                type: integer
                              y:
                                type: integer
                      totalAmount:
                        type: integer
                   responseCode:
                     type: string
                   responseMessage:
                     type: string
                   validations:
                     type: array
                     items:
                       type: object
                       properties:
                        errCode:
                          type: string
                        message:
                          type: string

        """
        query_response = dao.fetch_org_wise_opd_collections_dao(request, response_token)
        return jsonify(query_response[0]), query_response[1]


# (4)API For IPD+OPD+PHARMACY REVENUE##
@app.route('/reports/fetchOrgGrpWiseIpdAndOpdAndPharmacyCollections', methods=['POST'])
def fetch_org_grpwise_ipd_and_opd_and_pharmacy_collections_dao_pool():
        """
        This api is used to fetch oraganisation group wise IPD, OPD and Pharmacy collections total count
        Call this api by passing below fields and oraganisation group wise IPD, OPD and Pharmacy collections total count
        ---
        tags:
          - Financial
        consumes:
            application/json
        parameters:
          - in: body
            name: payload
            description: We use this payload to get the required response
            schema:
              type: object
              properties:
                 orgId:
                   type: integer
                 authenticatedUserId:
                   type: integer
                 orgGrpId:
                   type: integer
                 key:
                   type: string
        responses:
           400:
             description: An Error Occured
           200:
             description: Data Fetched Successfully
             schema:
               properties:
                 data:
                   type: object
                   properties:
                      branchWiseList:
                       type: array
                       items:
                         type: object
                         properties:
                           drilldown:
                             type: string
                           name:
                             type: string
                           orgId:
                             type: integer
                           y:
                             type: integer
                      totalCount:
                        type: integer
                 responseCode:
                   type: string
                 responseMessage:
                   type: string
                 validations:
                   type: array
                   items:
                     type: object
                     properties:
                       errCode:
                        type: string
                       message:
                        type: string
        """
        query_response = dao.fetch_org_grpwise_Ipd_and_Opd_and_pharmacy_collections_dao(request, response_token)
        return jsonify(query_response[0]), query_response[1]


# (4(b))API For Organization Module Wise IPD+OPD+PHARMACY REVENUE##
@app.route('/reports/fetchOrgModuleWiseIpdAndOpdAndPharmacyCollections', methods=['POST'])
def fetch_org_module_wise_ipd_and_opd_and_pharmacy_collections_dao_pool():
        """
                This api is used to fetch organisation module wise IPD, OPD, Pharmacy collections total count
                Call this api by passing below fields and organisation module wise IPD, OPD, Pharmacy collections total count
                ---
                tags:
                  - Financial
                consumes:
                    application/json
                parameters:
                  - in: body
                    name: payload
                    description: We use this payload to get the required response
                    schema:
                      type: object
                      properties:
                         orgId:
                           type: integer
                         authenticatedUserId:
                           type: integer
                         orgGrpId:
                           type: integer
                         key:
                           type: string
                responses:
                   400:
                     description: An Error Occured
                   200:
                     description: Data Fetched Successfully
                     schema:
                       properties:
                         data:
                           type: object
                           properties:
                             orgWiseCollectionsList:
                               type: array
                               items:
                                  type: object
                                  properties:
                                     drilldown:
                                        type: string
                                     name:
                                        type: string
                                     orgId:
                                        type: integer
                                     y:
                                        type: integer
                             totalAmount:
                                type: integer
                         responseCode:
                             type: string
                         responseMessage:
                             type: string
                         validations:
                             type: array
                             items:
                               type: object
                               properties:
                                  errCode:
                                    type: string
                                  message:
                                    type: string

                """
        query_response = dao.fetch_org_module_wise_ipd_and_opd_and_pharmacy_collections_dao(request, response_token)
        return jsonify(query_response[0]), query_response[1]


# (5)API For IP+OP REVENUE##
@app.route('/reports/fetchBranchWiseCollections', methods=['POST'])
def fetch_branch_wise_collections_dao_pool():
        """
                This api is used to fetch branch wise Total of IP and OP Revenue
                Call this api by passing below fields and branch wise Total of IP and OP Revenue
                ---
                tags:
                  - Financial
                consumes:
                    application/json
                parameters:
                  - in: body
                    name: payload
                    description: We use this payload to get the required response
                    schema:
                      type: object
                      properties:
                         orgId:
                           type: integer
                         authenticatedUserId:
                           type: integer
                         orgGrpId:
                           type: integer
                         key:
                           type: string
                responses:
                   400:
                     description: An Error Occured
                   200:
                     description: Data Fetched Successfully
                     schema:
                       properties:
                         data:
                           type: object
                           properties:
                             branchWiseList:
                               type: array
                               items:
                                  type: object
                                  properties:
                                     drilldown:
                                        type: string
                                     name:
                                        type: string
                                     orgId:
                                        type: integer
                                     y:
                                        type: integer
                             totalCount:
                                type: integer
                         responseCode:
                             type: string
                         responseMessage:
                             type: string
                         validations:
                             type: array
                             items:
                               type: object
                               properties:
                                  errCode:
                                    type: string
                                  message:
                                    type: string

        """
        query_response = dao.fetch_branch_wise_collections_dao(request, response_token)
        return jsonify(query_response[0]), query_response[1]


# (5(b))API For Branch Wise IP+OP REVENUE##
@app.route('/reports/fetchBranchCollections', methods=['POST'])
def fetch_branch_collections_dao_pool():

        """
        This api is used to fetch branch total collection count of IP and OP revenue
        Call this api by passing below fields and branch total collection count of IP and OP revenue
        ---
        tags:
          - Financial
        consumes:
            application/json
        parameters:
          - in: body
            name: payload
            description: We use this payload to get the required response
            schema:
              type: object
              properties:
                 orgId:
                   type: integer
                 authenticatedUserId:
                   type: integer
                 orgGrpId:
                   type: integer
                 key:
                   type: string
        responses:
           400:
            description: An Error Occured
           200:
            description: Data Fetched Successfully
            schema:
               properties:
                  data:
                    type: object
                    properties:
                        branchPatientVisitCollectionsList:
                               type: array
                               items:
                                  type: object
                                  properties:
                                     name:
                                        type: string
                                     y:
                                        type: integer
                        totalCount:
                            type: integer
                  responseCode:
                             type: string
                  responseMessage:
                             type: string
                  validations:
                             type: array
                             items:
                               type: object
                               properties:
                                  errCode:
                                    type: string
                                  message:
                                    type: string

        """
        query_response = dao.fetch_branch_collections_dao(request, response_token)
        return jsonify(query_response[0]), query_response[1]


# (6)API For REVENUE GENERATED FOR IPD BEDS##
@app.route('/reports/totalRevenueGeneratedForIPDBeds', methods=['POST'])
def total_revenue_generated_for_ipd_beds_dao_pool():
        """
                This api is used to fetch total revenue genaretd for IPD beds
                Call this api by passing below fields and total revenue genaretd for IPD beds
                ---
                tags:
                  - Financial
                consumes:
                    application/json
                parameters:
                  - in: body
                    name: payload
                    description: We use this payload to get the required response
                    schema:
                      type: object
                      properties:
                         orgId:
                           type: integer
                         authenticatedUserId:
                           type: integer
                         orgGrpId:
                           type: integer
                         key:
                           type: string
                responses:
                   400:
                     description: An Error Occured
                   200:
                     description: Data Fetched Successfully
                     schema:
                       properties:
                         data:
                           type: object
                           properties:
                            branchWiseList:
                              type: array
                              items:
                                type: object
                                properties:
                                  drilldown:
                                    type: string
                                  name:
                                    type: string
                                  orgId:
                                    type: integer
                                  perBedRevenue:
                                    type: integer
                                  y:
                                    type: integer
                            noOfBed:
                                type: integer
                            totalAmt:
                                type: integer
                         responseCode:
                            type: string
                         responseMessage:
                            type: string
                         validations:
                            type: array
                            items:
                              type: object
                              properties:
                                 errCode:
                                   type: string
                                 message:
                                   type: string
                """
        query_response = dao.total_revenue_generated_for_ipd_beds_dao(request, response_token)
        return jsonify(query_response[0]), query_response[1]


# (7)API For PHARMACY PROFIT DETAILS##
@app.route('/reports/fetchOrgWisePharmacyProfits', methods=['POST'])
def fetch_org_wise_pharmacy_profits_dao_pool():
        """
         This api is used to fetch organisation wise pharmacy profits count
         Call this api by passing below fields and organisation wise pharmacy profits count
         ---
         tags:
           - Financial
         consumes:
             application/json
         parameters:
           - in: body
             name: payload
             description: We use this payload to get the required response
             schema:
               type: object
               properties:
                  orgId:
                    type: integer
                  authenticatedUserId:
                    type: integer
                  orgGrpId:
                    type: integer
                  key:
                    type: string
         responses:
            400:
              description: An Error Occured
            200:
              description: Data Fetched Successfully
              schema:
                 properties:
                     data:
                        type: array
                        items:
                           type: object
                           properties:
                              drugBrandName:
                                type: string
                              profit:
                                type: integer
                              purchaseCost:
                                type: integer
                              saleAmt:
                                type: integer
                     responseCode:
                        type: string
                     responseMessage:
                        type: string
                     validations:
                        type: array
                        items:
                           type: object
                           properties:
                              errCode:
                                type: string
                              message:
                                type: string
         """
        query_response = dao.fetch_org_wise_pharmacy_profits_dao(request, response_token)
        return jsonify(query_response[0]), query_response[1]


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
