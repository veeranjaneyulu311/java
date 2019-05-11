'''
@transaction
def fetch_branch_wise_patient_count_dao(conn,req):
    print("hello")
    with transaction() as conn:
        with conn.cursor() as curs:
                print("hhi")
                query = "SELECT COUNT (*),PROGX.ORG_ID, ORG_NM FROM PUBLIC.PATIENT_ORGANISATION_XREF PROGX JOIN PUBLIC.ORGANISATION_REF ORG ON ORG.ORG_ID=PROGX.ORG_ID WHERE PROGX.ORG_GRP_ID=%(ORG_GRP_ID)s AND PROGX.ORG_ID=%(ORG_ID)s GROUP BY PROGX.ORG_ID,ORG_NM ORDER BY ORG_NM"
                curs.execute(query, {'ORG_GRP_ID': req['orgGrpId'], 'ORG_ID': req['orgId']})
                patient_count = curs.fetchall()
                print(patient_count)
                res = [dict(zip([key[0] for key in curs.description], row)) for row in patient_count]
                print(res)
                return res

'''