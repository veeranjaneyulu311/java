from connectionpool import transaction_connection_pool
from sqlqueries import *
from connections import *


@transaction_management_local
def sample_api(conn):
    query_insert_one = "INSERT INTO EMPLOYEES VALUES(7,'v','mahesh')"
    query_insert_two = "INSERT INTO EMPLOYEES VALUES(8,'k','santhosh')"
    curs = conn.cursor()
    curs.execute(query_insert_one)
    curs.execute(query_insert_two)
    return "success"


@transaction_management_dev
def fetch_branch_wise_patient_count_dao(conn, req):
    patient_count_query = sampleQuery
    curs = conn.cursor()
    curs.execute(patient_count_query, ({'ORG_GRP_ID': req['orgGrpId'], 'ORG_ID': req['orgId']}))
    result = curs.fetchall()
    data = [dict(zip([key[0] for key in curs.description], row)) for row in result]
    return data


@transaction_connection_pool
def fetch_branch_wise_patient_count_dao_pool(conn, req):
    patient_count_query = sampleQuery
    print("dao req", req)
    cursor = conn.cursor()
    print(type(req['key']))
    sqlParameters = {'empId': req['authenticatedUserId']}
    print(sqlParameters)
    # calling for checking the user is super Admin or not
    cursor.execute(fetchUserType, (sqlParameters))
    userType = cursor.fetchone()
    descr = cursor.description[0][0]
    print(type(descr))
    print(userType[0])
    query = queryToFetchPatientCountOfGroup
    if req['key'].lower()=="today":
        query += " AND CAST(PROGX.CREATED_DTTM AS DATE)=CURRENT_DATE "
        if (not userType[0]) and (not userType[0] == ""):
            query += " AND PROGX.ORG_ID=:orgId  "
    elif req['key'].lower()=="week":
        query+=" AND CAST(PROGX.CREATED_DTTM AS DATE) BETWEEN CURRENT_DATE- INTERVAL '7DAY' AND CURRENT_DATE "
        if (not userType[0]) and (not userType[0] == ""):
            query += " AND PROGX.ORG_ID=:orgId  "
    elif req['key'].lower() == "month":
        query+=" AND CAST(PROGX.CREATED_DTTM AS DATE) BETWEEN CURRENT_DATE- INTERVAL '1MONTH' AND CURRENT_DATE "
        if (not userType[0]) and (not userType[0] == ""):
            query += " AND PROGX.ORG_ID=:orgId  "
    elif req['key'].lower() == "3months":
        query+=" AND CAST(PROGX.CREATED_DTTM AS DATE) BETWEEN CURRENT_DATE- INTERVAL '3MONTH' AND CURRENT_DATE "
        if (not userType[0]) and (not userType[0] == ""):
                query += " AND PROGX.ORG_ID=:orgId  "
    elif req['key'].lower() == "custom":
        sqlParameters.update({'START_DT': req['startDt'], 'END_DT': req['endDt']})
        query+=" AND CAST(PROGX.CREATED_DTTM AS DATE) BETWEEN :START_DT AND :END_DT "
        if (not userType[0]) and (not userType[0] == ""):
            query += " AND PROGX.ORG_ID=:orgId  "
    elif req['key'].lower() == "all":
        if (not userType[0]) and (not userType[0] == ""):
            query += " AND PROGX.ORG_ID=:orgId  "

    query += " GROUP BY PVT.ORG_ID,ORG_NM ORDER BY ORG_NM "
    print(sqlParameters)
    print(query)
    cursor.execute(patient_count_query, ({'ORG_GRP_ID': req['orgGrpId'], 'ORG_ID': req['orgId']}))
    rows = cursor.fetchall()
    total_count = 0
    branch_wise_patient_count_values = []
    print("rows", rows)
    for row in rows:
        total_count += row[0]
        branch_wise_patient_count_values.append(dict(zip(('y', 'orgId', 'name'), row)))
    print("total", total_count)
    branch_wise_patient_count_dto = [branch_wise_patient_count_values, total_count]
    return branch_wise_patient_count_dto

# data.append(dict(zip([key[0] for key in cursor.description], row)))