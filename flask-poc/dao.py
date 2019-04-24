from psycopg2.extras import RealDictCursor
import connectionpool
import queries
import controller

# Operational


@connectionpool.transaction_connection_pool
def fetch_branch_wise_patient_count_dao(conn, req):
    controller.logger.debug("Entered Into fetchBranchWisePatientCount Python API")
    sql_parameters = {'empId': req['authenticatedUserId']}
    # calling for checking the user is super Admin or not
    cursor = conn.cursor()
    user_type = is_admin(cursor, sql_parameters)
    query = queries.queryToFetchPatientCountOfGroup
    query = get_formatted_query(query, req, sql_parameters, 'PROGX.CREATED_DTTM')
    if (not user_type[0]) and (not user_type[0] == ""):
        query += " AND PROGX.ORG_ID=%(orgId)s  "
    query += " GROUP BY PROGX.ORG_ID,ORG_NM ORDER BY ORG_NM "
    sql_parameters.update({'orgId': req['orgId'], 'ORG_GRP_ID': req['orgGrpId']})
    cursor.execute(query, sql_parameters)
    rows = cursor.fetchall()
    response_entity = response_mapper_for_branch_wise_patient(rows)
    controller.logger.debug("End Of fetchBranchWisePatientCount Python API")
    return response_entity


@connectionpool.transaction_connection_pool
def fetch_branch_wise_patient_visit_count_dao(conn, req):
    controller.logger.debug("Entered Into fetchBranchWisePatientVisitCount Python API")
    sql_parameters = {'empId': req['authenticatedUserId']}
    # calling for checking the user is super Admin or not
    cursor = conn.cursor()
    user_type = is_admin(cursor, sql_parameters)
    query = queries.queryToFetchPatientVisitCountOfGroup
    query = get_formatted_query(query, req, sql_parameters, 'PVT.CREATED_DTTM')
    if (not user_type[0]) and (not user_type[0] == ""):
        query += " AND PVT.ORG_ID=%(orgId)s  "
    query += " GROUP BY PVT.ORG_ID,ORG_NM ORDER BY ORG_NM "
    sql_parameters.update({'ORG_GRP_ID': req['orgGrpId'], 'orgId': req['orgId']})
    cursor.execute(query, sql_parameters)
    rows = cursor.fetchall()
    response_entity = response_mapper_for_branch_wise_patient(rows)
    controller.logger.debug("End Of fetchBranchWisePatientVisitCount Python API")
    return response_entity


# It verifies and returns true if user is admin
def is_admin(cursor, sql_parameters):
    cursor.execute(queries.fetchUserType, sql_parameters)
    user_type = cursor.fetchone()
    return user_type


# This function formats response for below functions
# fetch_branch_wise_patient_visit_count_dao
# fetch_branch_wise_patient_count_dao
def response_mapper_for_branch_wise_patient(rows):
    total_count = 0
    branch_wise_patient_count_values = []
    for row in rows:
        total_count += row[0]
        branch_wise_patient_count_values.append(dict(zip(('y', 'orgId', 'name'), row)))
    branch_wise_patient_count_dto = {'branchWiseList': branch_wise_patient_count_values, 'totalCount': total_count}
    return branch_wise_patient_count_dto


@connectionpool.transaction_connection_pool
def fetch_branch_patient_count_dao(conn, req):
    controller.logger.debug("Entered Into fetchBranchPatientCount Python API")
    sql_parameters = {'ORG_ID': req['orgId']}
    # calling for checking the user is super Admin or not
    query = queries.queryToFetchPatientCount
    if req['key'].lower() == "today":
        query += " AND CAST(CREATED_DTTM  AS DATE) BETWEEN CURRENT_DATE  AND CURRENT_DATE GROUP BY DATE(CREATED_DTTM) ORDER BY DATE(CREATED_DTTM) ";
    if req['key'].lower() == "week":
        query += " AND CAST(CREATED_DTTM  AS DATE) BETWEEN CURRENT_DATE - INTERVAL '7DAYS' AND CURRENT_DATE GROUP BY DATE(CREATED_DTTM) ORDER BY DATE(CREATED_DTTM)";
    if req['key'].lower() == "month":
        query = queries.queryToFetchPatientCountForMonth + " AND CREATED_DTTM::DATE BETWEEN CURRENT_DATE- INTERVAL '1 MONTH'  AND CURRENT_DATE GROUP BY DATE,MONT ORDER BY MONT";
    if req['key'].lower() == "3months":
        query = queries.queryToFetchPatientCountForMonth + " AND CREATED_DTTM::DATE BETWEEN CURRENT_DATE- INTERVAL '3 MONTH'  AND CURRENT_DATE GROUP BY DATE,MONT ORDER BY MONT ";
    if req['key'].lower() == "custom":
        sql_parameters.update({'START_DT': req['startDt'], 'END_DT': req['endDt']})
        query += " AND CAST(PVT.CREATED_DTTM AS DATE) BETWEEN %(START_DT)s AND %(END_DT)s "
    if req['key'].lower() == "all":
        query = queries.queryToFetchAllPatientsCount;
    cursor = conn.cursor()
    cursor.execute(query, sql_parameters)
    rows = cursor.fetchall()
    response_entity = response_mapper_for_branch_patient_count(rows)
    controller.logger.debug("End Of fetchBranchPatientCount Python API")
    return response_entity


@connectionpool.transaction_connection_pool
def fetch_branch_patient_visit_count_dao(conn, req):
    controller.logger.debug("Entered Into fetchBranchPatientVisitCount Python API")
    sql_parameters = {'ORG_ID': req['orgId']}
    # calling for checking the user is super Admin or not
    query = queries.queryToFetchPatientVisitCount
    if req['key'].lower() == "today":
        query += " AND CAST(CREATED_DTTM  AS DATE) BETWEEN CURRENT_DATE  AND CURRENT_DATE GROUP BY DATE(CREATED_DTTM) ORDER BY DATE(CREATED_DTTM) ";
    if req['key'].lower() == "week":
        query += " AND CAST(CREATED_DTTM  AS DATE) BETWEEN CURRENT_DATE - INTERVAL '7DAYS' AND CURRENT_DATE GROUP BY DATE(CREATED_DTTM) ORDER BY DATE(CREATED_DTTM)";
    if req['key'].lower() == "month":
        query = queries.queryToFetchPatientVisitCountForMonth + " AND CREATED_DTTM::DATE BETWEEN CURRENT_DATE- INTERVAL '1 MONTH'  AND CURRENT_DATE GROUP BY DATE,MONT ORDER BY MONT";
    if req['key'].lower() == "3months":
        query = queries.queryToFetchPatientVisitCountForMonth + " AND CREATED_DTTM::DATE BETWEEN CURRENT_DATE- INTERVAL '3 MONTH'  AND CURRENT_DATE GROUP BY DATE,MONT ORDER BY MONT ";
    if req['key'].lower() == "custom":
        sql_parameters.update({'START_DT': req['startDt'], 'END_DT': req['endDt']})
        query += " AND CAST(PVT.CREATED_DTTM AS DATE) BETWEEN %(START_DT)s AND %(END_DT)s "
    if req['key'].lower() == "all":
        query = queries.queryToFetchAllPatientVisitsCount;
    cursor = conn.cursor()
    cursor.execute(query, sql_parameters)
    rows = cursor.fetchall()
    response_entity = response_mapper_for_branch_patient_count(rows)
    controller.logger.debug("End Of fetchBranchPatientVisitCount Python API")
    return response_entity


# This function formats response for below functions
# fetch_branch_patient_count_dao
# fetch_branch_patient_visit_count_dao
def response_mapper_for_branch_patient_count(rows):
    total_count = 0
    registered_patient_count = []
    for row in rows:
        total_count += row[0]
        registered_patient_count.append(dict(zip(('y', 'name'), row)))
    branch_wise_patient_count_dto = {'patientCountList': registered_patient_count, 'totalCount': total_count}
    return branch_wise_patient_count_dto


'''
 this is common query formatter function for below api's
    fetchBranchWisePatientCount
    fetchBranchWisePatientVisitCount
    fetchOrgWiseTopTenDiseases
    fetchOrgWiseTopTenDrugBrandQty
    fetchTopTenSellingDrugBrands
    fetchDoctorWiseConsultationsCount
    fetchOrgWiseNearExpireDrugs
    fetchPharmacyCurrentInventory

'''


def get_formatted_query(query, req, sql_parameters, table=None):
    if table is None:
        if req['key'].lower() == "today":
            query += " AND CAST(CREATED_DTTM AS DATE)=CURRENT_DATE "
        elif req['key'].lower() == "week":
            query += " AND CAST(CREATED_DTTM AS DATE) BETWEEN CURRENT_DATE -INTERVAL '7DAYS' AND CURRENT_DATE "
        elif req['key'].lower() == "month":
            query += " AND CAST(CREATED_DTTM AS DATE) BETWEEN CURRENT_DATE -INTERVAL '1MONTH' AND CURRENT_DATE "
        elif req['key'].lower() == "3months":
            query += " AND CAST(CREATED_DTTM AS DATE) BETWEEN CURRENT_DATE -INTERVAL '3MONTH' AND CURRENT_DATE "
        elif req['key'].lower() == "custom":
            sql_parameters.update({'START_DT': req['startDt'], 'END_DT': req['endDt']})
            query += " AND CAST(CREATED_DTTM AS DATE) BETWEEN %(START_DT)s AND %(END_DT)s "
        elif req['key'].lower() == "all":
            pass
    else:
        if req['key'].lower() == "today":
            query += " AND CAST({} AS DATE)=CURRENT_DATE ".format(table)
        elif req['key'].lower() == "week":
            query += " AND CAST({} AS DATE) BETWEEN CURRENT_DATE -INTERVAL '7DAYS' AND CURRENT_DATE ".format(table)
        elif req['key'].lower() == "month":
            query += " AND CAST({} AS DATE) BETWEEN CURRENT_DATE -INTERVAL '1MONTH' AND CURRENT_DATE ".format(table)
        elif req['key'].lower() == "3months":
            query += " AND CAST({} AS DATE) BETWEEN CURRENT_DATE -INTERVAL '3MONTH' AND CURRENT_DATE ".format(table)
        elif req['key'].lower() == "custom":
            sql_parameters.update({'START_DT': req['startDt'], 'END_DT': req['endDt']})
            query += " AND CAST({} AS DATE) BETWEEN %(START_DT)s AND %(END_DT)s ".format(table)
        elif req['key'].lower() == "all":
            pass
    return query


# clinical


@connectionpool.transaction_connection_pool
def fetch_org_wise_top_ten_diseases_dao(conn, req):
    controller.logger.debug("Entered Into fetchOrgWiseTopTenDiseases Python API")
    sql_parameters = {'orgId': req['orgId']}
    # calling for checking the user is super Admin or not
    query = queries.queryToFetchOrgWiseTopTenDiseases
    query = get_formatted_query(query, req, sql_parameters)
    query += " GROUP BY DISEASES_NM ORDER BY DISEASES_COUNT DESC LIMIT 10 "
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    cursor.execute(query, sql_parameters)
    rows = cursor.fetchall()
    data = [dict(zip(('diseasesCount', 'diseaseName'), (row['diseases_count'],row['diseases_nm']))) for row in rows]
    controller.logger.debug("End Of fetchOrgWiseTopTenDiseases Python API")
    return data


@connectionpool.transaction_connection_pool
def fetch_org_wise_top_ten_drug_brand_qty_dao(conn, req):
    controller.logger.debug("Entered Into fetchOrgWiseTopTenDrugBrandQty Python API")
    sql_parameters = {'orgId': req['orgId']}
    # calling for checking the user is super Admin or not
    query_1 = queries.queryToFetchTopTenSellingDrugBrandQtyFirst
    query_1 = get_formatted_query(query_1, req, sql_parameters)
    query_1 += " GROUP BY brand_id, org_id, drug_brand_nm "
    query_2 = queries.queryToFetchTopTenSellingDrugBrandQtySecond
    query_2 = get_formatted_query(query_2, req, sql_parameters)
    query_2 += " GROUP BY brand_id, org_id, drug_brand_nm) SUB_QUERY GROUP BY brand_id, org_id, drug_brand_nm ORDER BY qty DESC LIMIT 10 "
    query = query_1+" UNION "+query_2
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    cursor.execute(query, sql_parameters)
    rows = cursor.fetchall()
    data = [dict(zip(('drugBrandNm', 'qty'), (row['drug_brand_nm'], row['qty']))) for row in rows]
    controller.logger.debug("Entered Into fetchOrgWiseTopTenDrugBrandQty Python API")
    return data


@connectionpool.transaction_connection_pool
def fetch_top_ten_selling_drug_brands_dao(conn, req):
    controller.logger.debug("Entered Into fetchTopTenSellingDrugBrands Python API")
    sql_parameters = {'orgId': req['orgId']}
    # calling for checking the user is super Admin or not
    query_1 = queries.queryToFetchTopTenSellingDrugBrandsFirst
    query_1 = get_formatted_query(query_1, req, sql_parameters)
    query_1 += "  GROUP BY PPOSDIT.org_id, PPOSDIT.drug_brand_nm, PPOSDIT.batch_no  "
    query_2 = queries.queryToFetchTopTenSellingDrugBrandsSecond
    query_2 = get_formatted_query(query_2, req, sql_parameters)
    query_2 += " GROUP BY PIUDIT.org_id, PIUDIT.drug_brand_nm, PIUDIT.batch_no) SUB_QUERY GROUP BY org_id, drug_brand_nm, batch_no ORDER BY total_amt DESC LIMIT 10 "
    query = query_1+" UNION "+query_2
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    cursor.execute(query, sql_parameters)
    rows = cursor.fetchall()
    data = [dict(zip(('drugName', 'totalAmt'), (float(row['total_amt']), row['drug_brand_nm']))) for row in rows]
    controller.logger.debug("End Of fetchTopTenSellingDrugBrands Python API")
    return data


@connectionpool.transaction_connection_pool
def fetch_doctor_wise_consultations_count_dao(conn, req):
    controller.logger.debug("Entered Into fetchDoctorWiseConsultationsCount Python API")
    sql_parameters = {'orgId': req['orgId']}
    # calling for checking the user is super Admin or not
    query = queries.queryToFetchDoctorWiseConsultations
    query = get_formatted_query(query, req, sql_parameters, 'PVT.visit_dt')
    query += " GROUP BY PVT.doctor_id, PVT.org_id, EIR.first_nm, EIR.last_nm order by Consultations desc  "
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    cursor.execute(query, sql_parameters)
    rows = cursor.fetchall()
    data = [dict(zip(('consultationCount', 'doctorName'), (row['consultations'], row['doctor_nm']))) for row in rows]
    controller.logger.debug("End Of fetchDoctorWiseConsultationsCount Python API")
    return data


@connectionpool.transaction_connection_pool
def fetch_org_wise_near_expire_drugs_dao(conn, req):
    controller.logger.debug("Entered Into fetchOrgWiseNearExpireDrugs Python API")
    sql_parameters = {'orgId': req['orgId']}
    # calling for checking the user is super Admin or not
    query = queries.queryToFetchOrgWiseNearExpireDrugs
    query = get_formatted_query(query, req, sql_parameters, 'EXPIRE_DATE')
    query += " ORDER BY EXPIRE_DT, DRUG_BRAND_NM "
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    cursor.execute(query, sql_parameters)
    rows = cursor.fetchall()
    data = [dict(zip(('drugBrandName', 'drugTypeName', 'expireDt'), (row['drug_brand_nm'], row['drug_type_nm'], row['expire_dt']))) for row in rows]
    controller.logger.debug("End Of fetchOrgWiseNearExpireDrugs Python API")
    return data


@connectionpool.transaction_connection_pool
def fetch_pharmacy_current_inventory_dao(conn, req):
    controller.logger.debug("Entered Into fetchPharmacyCurrentInventory Python API")
    sql_parameters = {'orgId': req['orgId']}
    # calling for checking the user is super Admin or not
    query = queries.queryToFetchPharmacyCurrentInventory
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    cursor.execute(query, sql_parameters)
    rows = cursor.fetchall()
    data = [dict(zip(('drugBrandName', 'drugQty'), (row['drug_brand_nm'], row['available_qty']))) for row in rows]
    controller.logger.debug("End Of fetchPharmacyCurrentInventory Python API")
    return data


#PHANI's- CODE:

############################################START OF "Functional" TAB APIS#######################################################################

##(1)Python API For Fetching Organization Group Wise Invoice Counts(TOTAL BILLS)##

@connectionpool.transaction_connection_pool
def fetch_org_grp_wise_invoice_count_dao(conn, req):
    controller.logger.debug("Entered fetchOrgGrpWiseInvoices Python API")
    sql_parameters = {'empId': req['authenticatedUserId']}
    # calling for checking the user is super Admin or not
    cursor = conn.cursor()
    user_type = is_admin(cursor, sql_parameters)
    # calling for checking the user is super Admin or not
    if req['key'].lower() == "all":
        query = queries.fetchOrGgrpInvoiceCountAndOrgDetailsForAll
    elif req['key'].lower() == "today":
        query = queries.fetchOrGgrpInvoiceCountAndOrgDetailsForToday
    elif req['key'].lower() == "week":
        query = queries.fetchOrGgrpInvoiceCountAndOrgDetailsForWeek
    elif req['key'].lower() == "month":
        query = queries.fetchOrGgrpInvoiceCountAndOrgDetailsForMonth
    elif req['key'].lower() == "3months":
        query = queries.fetchOrGgrpInvoiceCountAndOrgDetailsForThreeMonths
    elif req['key'].lower() == "custom":
        sql_parameters.update({'START_DT': req['startDt'], 'END_DT': req['endDt']})
        query = queries.fetchOrGgrpInvoiceCountAndOrgDetailsForCustom
    if (not user_type[0]) and (not user_type[0] == ""):
        query += " WHERE ORG_ID=%(orgId)s "
    query += " GROUP BY ORG_ID,ORG_NM,ORG_GRP_ID ORDER BY ORG_NM "
    sql_parameters.update({'orgId': req['orgId'], 'orgGrpId': req['orgGrpId']})
    cursor.execute(query, sql_parameters)
    rows = cursor.fetchall()
    total_invoice_count = 0
    total_invoice_count_values = []
    for row in rows:
        total_invoice_count += float(row[0])
        total_invoice_count_values.append(dict(zip(('y', 'orgId', 'name', 'drilldown'), (float(row[0]), row[1], row[3], row[3]))))
        data = {'totalInvoiceCount': total_invoice_count, 'branchWiseInvoiceCount': total_invoice_count_values}
        controller.logger.debug("End Of fetchOrgGrpWiseInvoices Python API")
        return data


# (1(b)) Python API For Fetching Organization Level Invoices Collections(TOTAL BILLS)##
@connectionpool.transaction_connection_pool
def fetch_org_wise_invoice_count_dao(conn, req):
    controller.logger.debug("Entered Into fetchOrgLevelInvoices Python API")
    sql_parameters = {'orgId': req['orgId'], 'empId': req['authenticatedUserId'], 'orgGrpId': req['orgGrpId']}
    if req['key'].lower() == "today":
        query = queries.fetchOrgWiseModuleInvoices
    elif req['key'].lower() == "week":
        query = queries.fetchOrgWiseModuleInvoicesForWeek
    elif req['key'].lower() == "month":
        query = queries.fetchOrgWiseModuleInvoicesForMonth
    elif req['key'].lower() == "3months":
        query = queries.fetchOrgWiseModuleInvoicesForThree
    elif req['key'].lower() == "custom":
        sql_parameters.update({'START_DT': req['startDt'], 'END_DT': req['endDt']})
        query = queries.fetchOrgWiseModuleInvoicesForCustom
    elif req['key'].lower() == "all":
        query = queries.fetchOrgWiseModuleInvoicesForAll
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    cursor.execute(query, sql_parameters)
    rows = cursor.fetchall()
    total_count = 0
    org_level_invoices_list_values = []
    for row in rows:
        total_count += row['invoice_no']
        org_level_invoices_list_values.append(dict(
            zip(('name', 'y', 'yearMonth', 'startDate', 'type', 'drilldown', 'orgId'),(row['type'], row['invoice_no'], None, None, None, row['type'], row['org_id']))))
        data = {'totalCount': total_count, 'orgLevelInvoicesList': org_level_invoices_list_values}
    controller.logger.debug("End Of fetchOrgLevelInvoices Python API")
    return data


# (2)Python API For Fetching Organization Group Wise IPD Collections(TOTAL IPD REVENUE AMOUNT)##
@connectionpool.transaction_connection_pool
def fetch_org_grp_wise_Ipd_Collections_dao(conn, req):
    controller.logger.debug("Entered Into fetchOrgLevelInvoices Python API")
    sql_parameters = {'empId': req['authenticatedUserId']}
    # calling for checking the user is super Admin or not
    cursor = conn.cursor()
    user_type = is_admin(cursor, sql_parameters)
    query = queries.fetchOrgGrpWiseIpdCollections
    if (not user_type[0]) and (not user_type[0] == ""):
        query += " AND PBI.ORG_ID=%(orgId)s  "

    if req['key'].lower() == "today":
        query += " AND  CAST(PBI.CREATED_DTTM AS DATE) =CURRENT_DATE GROUP BY POR.ORG_ID,POR.ORG_GRP_ID,POR.ORG_NM "
    elif req['key'].lower() == "week":
        query += "  AND CAST(PBI.CREATED_DTTM AS DATE) BETWEEN CURRENT_DATE -INTERVAL '7DAYS' AND CURRENT_DATE GROUP BY POR.ORG_ID,POR.ORG_GRP_ID,POR.ORG_NM "
    elif req['key'].lower() == "month":
        query += " AND CAST(PBI.CREATED_DTTM AS DATE) BETWEEN CURRENT_DATE -INTERVAL '1MONTH' AND CURRENT_DATE GROUP BY POR.ORG_ID,POR.ORG_GRP_ID,POR.ORG_NM "
    elif req['key'].lower() == "3months":
        query += "  AND CAST(PBI.CREATED_DTTM AS DATE) BETWEEN CURRENT_DATE -INTERVAL '3MONTH' AND CURRENT_DATE GROUP BY POR.ORG_ID,POR.ORG_GRP_ID,POR.ORG_NM "
    elif req['key'].lower() == "custom":
        sql_parameters.update({'START_DT': req['startDt'], 'END_DT': req['endDt']})
        query += " AND CAST(PBI.CREATED_DTTM AS DATE) BETWEEN %(startDt)s AND %(endDt)s GROUP BY POR.ORG_ID,POR.ORG_GRP_ID,POR.ORG_NM  "
    elif req['key'].lower() == "all":
        query += " GROUP BY POR.ORG_ID,POR.ORG_GRP_ID,POR.ORG_NM ORDER BY POR.ORG_NM "

    sql_parameters.update({'orgId': req['orgId'], 'orgGrpId': req['orgGrpId']})
    cursor.execute(query, sql_parameters)
    rows = cursor.fetchall()
    total_IPD_amount = 0
    branch_wise_collection_values = []

    for row in rows:
        total_IPD_amount += float(row[3])
        branch_wise_collection_values.append(dict(zip(('name', 'y', 'orgId', 'drilldown'), (row[1], float(row[3]), row[0], row[1]))))
        result = {'branchWiseList': branch_wise_collection_values, 'totalCount': total_IPD_amount}
        controller.logger.debug("End Of fetchOrgLevelInvoices Python API")
        return result


# (2(b)) Python API For Fetching Organization Wise IPD COllections(IP REVENUE)##
@connectionpool.transaction_connection_pool
def fetch_org_wise_ipd_collections_dao(conn, req):
    controller.logger.debug("Entered Into fetchOrgWiseIpdCollections Python API")
    sql_parameters = {'orgId': req['orgId'], 'empId': req['authenticatedUserId'], 'orgGrpId': req['orgGrpId']}
    query = queries.queryTofetchOrgWiseIpdCollections

    if req['key'].lower() == "today":
        query += "    AND  CAST(PBI.CREATED_DTTM AS DATE) =CURRENT_DATE GROUP BY PBI.ORG_ID,DATE "
    elif req['key'].lower() == "week":
        query += "  AND CAST(PBI.CREATED_DTTM AS DATE) BETWEEN CURRENT_DATE -INTERVAL '7DAYS' AND CURRENT_DATE GROUP BY DATE,PBI.ORG_ID "
    elif req['key'].lower() == "month":
        query = queries.fetchOrgWiseIpdCollectionsForMonth
    elif req['key'].lower() == "3months":
        query = queries.fetchOrgWiseIpdCollectionsForThree
    elif req['key'].lower() == "custom":
        sql_parameters.update({'START_DT': req['startDt'], 'END_DT': req['endDt']})
        query += "   AND CAST(PBI.CREATED_DTTM AS DATE) BETWEEN %(startDt)s AND %(endDt)s GROUP BY DATE,PBI.ORG_ID "
    elif req['key'].lower() == "all":
        query = queries.fetchOrgWiseIpdCollectionsForAll

    cursor = conn.cursor(cursor_factory=RealDictCursor)
    cursor.execute(query, sql_parameters)
    rows = cursor.fetchall()
    print(rows)
    total_amount = 0.00
    fetch_org_wise_ipd_collections_values = []

    for row in rows:
        total_amount += float(row['total_amt'])
        fetch_org_wise_ipd_collections_values.append(
            dict(zip(('name', 'y', 'drilldown', 'orgId'), (row['date'], float(row['total_amt']), row['date'], row['org_id']))))
        data = {'totalAmount': total_amount, 'orgWiseCollectionsList': fetch_org_wise_ipd_collections_values}
    controller.logger.debug("End Of fetchOrgWiseIpdCollections Python API")
    return data


# (3)Python API For Fetching Organization Group Wise OPD Collections(TOTAL OPD REVENUE AMOUNT)##

@connectionpool.transaction_connection_pool
def fetch_org_grp_wise_OPD_collections_dao(conn, req):
    controller.logger.debug("Entered Into fetchOrgGrpWiseOPDCollection Python API")
    sql_parameters = {'empId': req['authenticatedUserId']}
    # calling for checking the user is super Admin or not
    cursor = conn.cursor()
    user_type = is_admin(cursor, sql_parameters)
    # calling for checking the user is super Admin or not

    if req['key'].lower() == "all":
        query = queries.fetchOrgGrpWiseOPDCollectionForAll
    elif req['key'].lower() == "today":
        query = queries.fetchOrgGrpWiseOPDCollectionForToday
    elif req['key'].lower() == "week":
        query = queries.fetchOrgGrpWiseOPDCollectionForWeek
    elif req['key'].lower() == "month":
        query = queries.fetchOrGgrpWiseOPDCollectionForMonth
    elif req['key'].lower() == "3months":
        query = queries.fetchOrGgrpWiseOPDCollectionForThreeMonths
    elif req['key'].lower() == "custom":
        sql_parameters.update({'START_DT': req['startDt'], 'END_DT': req['endDt']})
        query = queries.fetchOrGgrpWiseOPDCollectionForCustom

    if (not user_type[0]) and (not user_type[0] == ""):
        query += " AND PBI.ORG_ID=%(orgId)s  "

    query += " GROUP BY PBI.ORG_ID,PBI.ORG_GRP_ID,POR.ORG_NM ORDER BY POR.ORG_NM "
    sql_parameters.update({'orgId': req['orgId'], 'orgGrpId': req['orgGrpId']})
    cursor.execute(query, sql_parameters)
    rows = cursor.fetchall()
    total_amount = 0
    branch_wise_OPD_collections_values = []

    for row in rows:
        total_amount += float(row[3])
        print("total", total_amount)
        branch_wise_OPD_collections_values.append(
            dict(zip(('orgId', 'name', 'y', 'drilldown'), (row[0], row[1], float(row[3]), row[1], float(row[3])))))

        data = {'totalAmt': total_amount, 'branchWiseOPDCollections': branch_wise_OPD_collections_values}
        controller.logger.debug("End Of fetchOrgGrpWiseOPDCollection Python API")
        return data


# (3(b))Python API For Fetching Organization Wise OPD Collections(OP REVENUE)-modify##

@connectionpool.transaction_connection_pool
def fetch_org_wise_opd_collections_dao(conn, req):
    controller.logger.debug("Entered Into fetchOrgWiseOPDCollections Python API")
    sql_parameters = {'orgId': req['orgId'], 'empId': req['authenticatedUserId'], 'orgGrpId': req['orgGrpId']}
    if req['key'].lower() == "today":
        query = queries.fetchOrgWiseOPDCollectionsForToday
    elif req['key'].lower() == "week":
        query = queries.fetchOrgWiseOPDCollectionsForWeek
    elif req['key'].lower() == "month":
        query = queries.fetchOrgWiseOPDCollectionsForMonth
    elif req['key'].lower() == "3months":
        query = queries.fetchOrgWiseOPDCollectionsForThreeMonths
    elif req['key'].lower() == "custom":
        sql_parameters.update({'START_DT': req['startDt'], 'END_DT': req['endDt']})
        query = queries.fetchOrgWiseOPDCollectionsForCustom
    elif req['key'].lower() == "all":
        query = queries.fetchOrgWiseOPDCollectionsForAll
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    cursor.execute(query, sql_parameters)
    rows = cursor.fetchall()
    print(rows)
    total_amount = 0.00
    fetch_org_wise_opd_collections_values = []
    for row in rows:
        total_amount += float(row['total_amt'])
        fetch_org_wise_opd_collections_values.append(
            dict(zip(('name', 'y', 'drilldown', 'orgId'), (row['date'], float(row['total_amt']), row['date'], row['org_id']))))
        data = {'totalAmount': total_amount, 'orgWiseCollectionsList': fetch_org_wise_opd_collections_values}
    controller.logger.debug("End Of fetchOrgWiseOPDCollections Python API")
    return data


##(4) Python API For Fetching Organization Group Wise IP+OP+Pharmacy Revenue(IP+OP+PHARMACY TOTAL REVENUE)##

@connectionpool.transaction_connection_pool
def fetch_org_grpwise_Ipd_and_Opd_and_pharmacy_collections_dao(conn, req):
    controller.logger.debug("Entered into fetchOrgGrpWiseIpdAndOpdAndPharmacyCollections Python API")
    cursor = conn.cursor()
    sql_parameters = {'empId': req['authenticatedUserId']}
    # calling for checking the user is super Admin or not
    cursor = conn.cursor()
    user_type = is_admin(cursor, sql_parameters)

    if req['key'].lower() == "today":
        query = queries.fetchOrgGrpWiseIpdAndOpdAndPharmacyCollectionsToday
    elif req['key'].lower() == "week":
        query = queries.fetchOrgGrpWiseIpdAndOpdAndPharmacyCollectionsSevenDays
    elif req['key'].lower() == "month":
        query = queries.fetchOrgGrpWiseIpdAndOpdAndPharmacyCollectionsOneMonths
    elif req['key'].lower() == "3months":
        query = queries.fetchOrgGrpWiseIpdAndOpdAndPharmacyCollectionsThreeMonths
    elif req['key'].lower() == "custom":
        sql_parameters.update({'START_DT': req['startDt'], 'END_DT': req['endDt']})
        query = queries.fetchOrgGrpWiseIpdAndOpdAndPharmacyCollectionsCustom
    elif req['key'].lower() == "all":
        query = queries.fetchOrgGrpWiseIpdAndOpdAndPharmacyCollectionsAll

    if (not user_type[0]) and (not user_type[0] == ""):
        query += " WHERE ORG_ID=%(orgId)s  "

    query += " GROUP BY ORG_ID,ORG_NM,ORG_GRP_ID ORDER BY ORG_NM  "
    sql_parameters.update({'orgGrpId': req['orgGrpId'], 'orgId': req['orgId']})
    cursor = conn.cursor()
    cursor.execute(query, sql_parameters)
    rows = cursor.fetchall()
    total_amount = 0.00
    ipd_op_pharmacy_revenue_values = []
    for row in rows:
        total_amount += float(row[3])
        ipd_op_pharmacy_revenue_values.append(
            dict(zip(('orgId', 'name', 'drilldown', 'y'), (row[0], row[1], row[1], float(row[3])))))
        data = {'orgWiseCollectionsList': ipd_op_pharmacy_revenue_values, 'totalAmount': total_amount}
        controller.logger.debug("End Of fetchOrgGrpWiseIpdAndOpdAndPharmacyCollections Python API")
        return data


##(4(b))Python API For Fetching Organization Module Wise IP+OP+PHARMACY Revenue(IP+OP+PHARMACY)##
@connectionpool.transaction_connection_pool
def fetch_org_module_wise_ipd_and_opd_and_pharmacy_collections_dao(conn, req):
    controller.logger.debug("Entered Into fetchOrgLevelInvoices Python API ")
    cursor = conn.cursor()
    sql_parameters = {'orgId': req['orgId'], 'empId': req['authenticatedUserId'], 'orgGrpId': req['orgGrpId']}

    if req['key'].lower() == "today":
        query = queries.fetchOrgModuleWiseIpdAndOpdAndPharmacyCollectionsToday
    elif req['key'].lower() == "week":
        query = queries.fetchOrgModuleWiseIpdAndOpdAndPharmacyCollectionsSevenDays
    elif req['key'].lower() == "month":
        query = queries.fetchOrgModuleWiseIpdAndOpdAndPharmacyCollectionsOneMonths
    elif req['key'].lower() == "3months":
        query = queries.fetchOrgModuleWiseIpdAndOpdAndPharmacyCollectionsThreeMonths
    elif req['key'].lower() == "custom":
        sql_parameters.update({'START_DT': req['startDt'], 'END_DT': req['endDt']})
        query = queries.fetchOrgModuleWiseIpdAndOpdAndPharmacyCollectionsCustom
    elif req['key'].lower() == "all":
        query = queries.fetchOrgModuleWiseIpdAndOpdAndPharmacyCollectionsAll

    cursor = conn.cursor()
    cursor.execute(query, sql_parameters)
    rows = cursor.fetchall()
    print(rows)
    total_amount = 0.00
    orgModule_Wise_ipd_opd_pharmacy_collections_values = []
    for row in rows:
        total_amount += float(row[3])
        orgModule_Wise_ipd_opd_pharmacy_collections_values.append(
            dict(zip(('name', 'y', 'drilldown', 'orgId'), (row[4], float(row[3]), row[4], row[0]))))
        data = {'totalAmount': total_amount,
                'orgWiseCollectionsList': orgModule_Wise_ipd_opd_pharmacy_collections_values}
    controller.logger.debug("End Of fetchOrgLevelInvoices Python API")
    return data


##(5)Python API For Fetching Branch Wise IP+OP Revenue(IP+OP REVENUE)##
@connectionpool.transaction_connection_pool
def fetch_branch_wise_collections_dao(conn, req):
    controller.logger.debug("Entered Into fetchBranchWiseCollections Python API")
    cursor = conn.cursor()
    sql_parameters = {'empId': req['authenticatedUserId']}
    # calling for checking the user is super Admin or not
    cursor = conn.cursor()
    user_type = is_admin(cursor, sql_parameters)
    query = queries.fetchCollectionsOfGroup

    if req['key'].lower() == "today":
        query += " AND CAST(PBT.CREATED_DTTM AS DATE)=CURRENT_DATE  "
    elif req['key'].lower() == "week":
        query += " AND CAST(PBT.CREATED_DTTM AS DATE) BETWEEN CURRENT_DATE- INTERVAL '7DAYS' AND CURRENT_DATE "
    elif req['key'].lower() == "month":
        query += " AND CAST(PBT.CREATED_DTTM AS DATE) BETWEEN CURRENT_DATE- INTERVAL '1MONTH' AND CURRENT_DATE "
    elif req['key'].lower() == "3months":
        query += " AND CAST(PBT.CREATED_DTTM AS DATE) BETWEEN CURRENT_DATE- INTERVAL '3MONTH' AND CURRENT_DATE "
    elif req['key'].lower() == "custom":
        sql_parameters.update({'START_DT': req['startDt'], 'END_DT': req['endDt']})
        query += " AND CAST(PBT.CREATED_DTTM AS DATE) BETWEEN %(START_DT)s AND %(END_DT)s "
    elif req['key'].lower() == "all":
        pass

    if (not user_type[0]) and (not user_type[0] == ""):
        query += " AND PBT.ORG_ID=%(orgId)s  "

    query += " GROUP BY PBT.ORG_ID,ORG_NM ORDER BY ORG_NM "
    sql_parameters.update({'orgId': req['orgId'], 'orgGrpId': req['orgGrpId']})
    cursor = conn.cursor()
    cursor.execute(query, sql_parameters)
    rows = cursor.fetchall()
    total_count = 0
    branch_wise_collection_values = []

    for row in rows:
        total_count += float(row[0])
        branch_wise_collection_values.append(
            dict(zip(('name', 'y', 'orgId', 'drilldown'), (row[2], float(row[0]), row[1], row[2]))))
        branch_wise_patient_count_dto = {'branchWiseList': branch_wise_collection_values, 'totalCount': total_count}
        controller.logger.debug("End Of fetchBranchWiseCollections Python API")
        return branch_wise_patient_count_dto


##(5(b))Python API For Fetching Fetching Branch Collections(IP+OP REVENUE)##

@connectionpool.transaction_connection_pool
def fetch_branch_collections_dao(conn, req):
    controller.logger.debug("Entered Into fetchBranchCollections Python API")
    sql_parameters = {'orgGrpId': req['orgGrpId'], 'orgId': req['orgId'], 'empId': req['authenticatedUserId']}
    query = queries.fetchBranchPatientVisitCountCollections
    if req['key'].lower() == "today":
        query += " AND CAST(CREATED_DTTM  AS DATE) BETWEEN CURRENT_DATE  AND CURRENT_DATE GROUP BY DATE(CREATED_DTTM) ORDER BY DATE(CREATED_DTTM) "
    elif req['key'].lower() == "week":
        query += " AND CAST(CREATED_DTTM  AS DATE) BETWEEN CURRENT_DATE - INTERVAL '7DAYS' AND CURRENT_DATE GROUP BY DATE(CREATED_DTTM) ORDER BY DATE(CREATED_DTTM)"
    elif req['key'].lower() == "month":
        query = queries.fetchBranchPatientVisitCountCollectionsForMonth + " AND CREATED_DTTM::DATE BETWEEN CURRENT_DATE- INTERVAL '1 MONTH'  AND CURRENT_DATE GROUP BY DATE,MONT ORDER BY MONT"
    elif req['key'].lower() == "3months":
        query = queries.fetchBranchPatientVisitCountCollectionsForMonth + " AND CREATED_DTTM::DATE BETWEEN CURRENT_DATE- INTERVAL '3 MONTH'  AND CURRENT_DATE GROUP BY DATE,MONT ORDER BY MONT "
    elif req['key'].lower() == "custom":
        sql_parameters.update({'START_DT': req['startDt'], 'END_DT': req['endDt']})
        query += " AND CAST(CREATED_DTTM AS DATE) BETWEEN %(startDt)s AND %(endDt)s GROUP BY DATE"
    elif req['key'].lower() == "all":
        query = queries.fetchBranchPatientVisitCountCollectionsForAll
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    cursor.execute(query, sql_parameters)
    rows = cursor.fetchall()
    total_count = 0.00
    fetch_branch_collections_values = []
    for row in rows:
        total_count += float(row['sum'])
        fetch_branch_collections_values.append(dict(zip(('name', 'y'), (row['date'], float(row['sum'])))))
        data = {'branchPatientVisitCollectionsList': fetch_branch_collections_values, 'totalCount': total_count}
    controller.logger.debug("End Of fetchBranchCollections Python API")
    return data


# (6)Python API For Fetching Total Revenue Generated From IPD Beds(REVENUE FOR IP BEDS)##
@connectionpool.transaction_connection_pool
def total_revenue_generated_for_ipd_beds_dao(conn, req):
    controller.logger.debug("Entered Into fetchorgGrpWisetotalRevenueGeneratedForIPDBeds Python API")
    cursor = conn.cursor()
    # calling for checking the user is super Admin or not
    sql_parameters = {'empId': req['authenticatedUserId']}
    cursor = conn.cursor()
    user_type = is_admin(cursor, sql_parameters)

    if req['key'].lower() == "all":
        query = queries.fetchorgGrpWisetotalRevenueGeneratedForIPDBedsForAll
    elif req['key'].lower() == "today":
        query = queries.fetchorgGrpWisetotalRevenueGeneratedForIPDBedsForToday
    elif req['key'].lower() == "week":
        query = queries.fetchorgGrpWisetotalRevenueGeneratedForIPDBedsForWeek
    elif req['key'].lower() == "month":
        query = queries.fetchorgGrpWisetotalRevenueGeneratedForIPDBedsForMonth
    elif req['key'].lower() == "3months":
        query = queries.fetchorgGrpWisetotalRevenueGeneratedForIPDBedsForThreeMonths
    elif req['key'].lower() == "custom":
        sql_parameters.update({'START_DT': req['startDt'], 'END_DT': req['endDt']})
        query = queries.fetchorgGrpWisetotalRevenueGeneratedForIPDBedsForCustom

    if (not user_type[0]) and (not user_type[0] == ""):
        query += " AND INVOICE_SUM.org_id=%(orgId)s "

    query += " ORDER BY ORG_NM "
    sql_parameters.update({'orgId': req['orgId'], 'orgGrpId': req['orgGrpId']})
    cursor = conn.cursor()
    cursor.execute(query, sql_parameters)
    rows = cursor.fetchall()
    total_amount = 0
    branch_wise_Ipd_bed_revenue_values = []
    for row in rows:
        total_amount += float(row[2])
        print("total", total_amount)
        branch_wise_Ipd_bed_revenue_values.append([dict(zip(('orgId', 'name', 'y', 'drilldown', 'perBedRevenue'),
                                                            (row[4], row[3], float(row[2]), row[3], float(row[2]))))])
        data = {'totalAmt': total_amount, 'noOfBed': row[1], 'branchWiseIPDRevenue': branch_wise_Ipd_bed_revenue_values}
    controller.logger.debug("End Of fetchorgGrpWisetotalRevenueGeneratedForIPDBeds Python API")
    return data


# (7)Python API For Fetching Organization Wise Pharmacy Profits Report(PHARMACY PROFIT DETAILS) ##
@connectionpool.transaction_connection_pool
def fetch_org_wise_pharmacy_profits_dao(conn, req):
    controller.logger.debug("Entered Into fetchOrgWisePhramacyProfits Python API")
    sql_parameters = {'orgId': req['orgId']}
    if req['key'].lower() == "today":
        query = queries.fetchOrgWisePhramacyProfitsForToday
    elif req['key'].lower() == "week":
        query = queries.fetchOrgWisePhramacyProfitsForWeek
    elif req['key'].lower() == "month":
        query = queries.fetchOrgWisePhramacyProfitsForMonth
    elif req['key'].lower() == "3months":
        query = queries.fetchOrgWisePhramacyProfitsForThreeMonths
    elif req['key'].lower() == "custom":
        sql_parameters.update({'START_DT': req['startDt'], 'END_DT': req['endDt']})
        query = queries.fetchOrgWisePhramacyProfitsForCustom
    elif req['key'].lower() == "all":
        query = queries.fetchOrgWisePhramacyProfitsForAll

    query += " GROUP BY EI.DRUG_BRAND_NM ORDER BY EI.DRUG_BRAND_NM "
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    cursor.execute(query, sql_parameters)
    rows = cursor.fetchall()
    data = [dict(zip(('drugBrandName', 'purchaseCost', 'saleAmt', 'profit'),(row['drug_brand_nm'], float(row['purchase_cost']), float(row['sale_amt']), float(row['profit'])))) for row in rows]
    controller.logger.debug("End Of fetchOrgWisePhramacyProfits Python API")
    return data


################################################END OF "Financial" TAB APIS#####################################################################################

