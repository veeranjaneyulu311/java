import json
import logging

import psycopg2
from flask_cors import CORS
from psycopg2 import pool
from flask import request, jsonify, Flask
from psycopg2.extras import RealDictCursor


'''
payload:
--------
uid : String
node_id : String
timestamp: Integer
clid: String
input: Integer
'''

app = Flask(__name__)


# The below line handles the CORS issue
cors = CORS(app, resources={r"*": {"origins": "*"}})

# queries
query_to_fetch_node_type_and_org_id = "SELECT MYOP_NODE_TYPE, ORG_ID FROM PUBLIC.MYOPERATOR_NODE_ORG_REF WHERE MYOP_NODE_CODE=%(node_id)s"

# departments
query_to_fetch_department_list = "SELECT ROW_NUMBER () OVER (ORDER BY DEPT_NM) AS SNO,OD.DEPT_ID,DEPT.DEPT_NM FROM PUBLIC.ORGANISATION_DEPARTMENT_XREF OD JOIN DEPARTMENT_REF DEPT ON OD.DEPT_ID=DEPT.DEPT_ID WHERE ORG_ID=%(org_id)s"
query_to_insert_uid_and_department_list = "INSERT INTO PUBLIC.MYOPERATOR_APPOINTMENT_TEMP_TRANS(MYOP_CALLER_CODE, DEPT_LIST, ORG_ID) VALUES (%(caller_uid)s, %(dept_list)s, %(org_id)s)"

# doctors
query_to_fetch_dep_id = "SELECT DEPT_LIST -> %(input)s AS DEPT_ID FROM PUBLIC.MYOPERATOR_APPOINTMENT_TEMP_TRANS WHERE ORG_ID=%(org_id)s AND MYOP_CALLER_CODE=%(uid)s"
query_to_update_dep_id_selected = "UPDATE PUBLIC.MYOPERATOR_APPOINTMENT_TEMP_TRANS SET DEPT_LIST = JSONB_SET(DEPT_LIST, '{%(input)s}', %(dept_selected_update)s) WHERE ORG_ID=%(org_id)s AND MYOP_CALLER_CODE=%(uid)s"
query_to_fetch_doctors_list = "SELECT ROW_NUMBER () OVER (ORDER BY EMP_USER_NM) AS SNO,OE.EMP_ID, REPLACE(CONCAT(INITCAP(EIR.FIRST_NM),' ',INITCAP(EIR.MIDDLE_NM),' ',INITCAP(EIR.LAST_NM)),' ',' ') AS EMP_USER_NM FROM ORGANISATION_EMPLOYEE_XREF OE JOIN EMPLOYEES_INFO_REF EIR ON EIR.EMP_ID=OE.EMP_ID JOIN EMPLOYEE_DEPT_XREF ED ON ED.EMP_ID= EIR.EMP_ID WHERE OE.ORG_ID=%(org_id)s AND DEPT_ID=%(dept_id)s AND DOCTOR_REGISTER_NO IS NOT NULL"
query_to_update_doctors_list = "UPDATE PUBLIC.MYOPERATOR_APPOINTMENT_TEMP_TRANS SET DOCTORS_LIST= %(doctors_list)s WHERE ORG_ID=%(org_id)s AND MYOP_CALLER_CODE=%(uid)s"

# time slots
query_to_fetch_doct_id = "SELECT DOCTORS_LIST -> %(input)s AS DOCT_ID FROM PUBLIC.MYOPERATOR_APPOINTMENT_TEMP_TRANS WHERE ORG_ID=%(org_id)s AND MYOP_CALLER_CODE=%(uid)s"
query_to_update_doct_id_selected = "UPDATE PUBLIC.MYOPERATOR_APPOINTMENT_TEMP_TRANS SET DOCTORS_LIST = JSONB_SET(DOCTORS_LIST, '{%(input)s}', %(selected_doct_update)s) WHERE ORG_ID=%(org_id)s AND MYOP_CALLER_CODE=%(uid)s"
query_to_fetch_time_slots = "days,slots where org_id and doc_id"
query_to_update_doctors_list = "UPDATE PUBLIC.MYOPERATOR_APPOINTMENT_TEMP_TRANS SET DOCTORS_LIST= %(doctors_list)s WHERE ORG_ID=%(org_id)s AND MYOP_CALLER_CODE=%(uid)s"


# logging configuration
logger = logging.getLogger("my_operator")
handler = logging.FileHandler('my_operator.log')
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.INFO)


# connection pool;
try:
    threaded_postgres_sql_pool = psycopg2.pool.ThreadedConnectionPool(5, 15, database="drucare_dev", user="drucare_emp", password="Dru@143$care", host="192.168.1.111", port="5432")
except (Exception, psycopg2.DatabaseError) as error :
    logger.info("Error while connecting to PostgreSQL", error)


# storing users current_status
response = {"action": 'tts', "value": ''}
department_message = 'PRESS {} FOR {}, '


# steps:
# fetch node_type, org_id for given node_id
# insert the uid and org_id into booking table
# fetch departments of the corresponding org_id
#


@app.route('/bookAppointment', methods=['POST'])
def fetch_all():
    uid = request.form["uid"]
    node_id = request.form['node_id']
    clid = request.form['clid']

    conn = threaded_postgres_sql_pool.getconn()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    sql_parameters_node_id = {'node_id': node_id}
    cursor.execute(query_to_fetch_node_type_and_org_id, sql_parameters_node_id)
    result = cursor.fetchone()

    # fetching departments of an organization for given node id
    if result['myop_node_type'] == 'departments':
        sql_parameters_org_id = {'org_id': result['org_id']}
        cursor.execute(query_to_fetch_department_list, sql_parameters_org_id)
        departments_list = cursor.fetchall()
        insert_departments_as_json = {}
        data = ''
        for department in departments_list:
            insert_departments_as_json[str(department['sno'])] = {"dept_id": department['dept_id'], "dept_nm": department['dept_nm'], "selected": 0}
            data = data + department_message.format(department['sno'], department['dept_nm'])
        sql_parameters_for_transaction = {'caller_uid': uid, 'dept_list': json.dumps(insert_departments_as_json), 'org_id': result['org_id']}
        cursor.execute(query_to_insert_uid_and_department_list, sql_parameters_for_transaction)
        conn.commit()
        response['value'] = data
        return jsonify(response)
    # doctors
    elif result['myop_node_type'] == 'doctors':
        cursor_non_real_dict = conn.cursor()
        selected_input_option = request.form['input']
        print(int(selected_input_option))
        # fetch the selected dept id
        sql_parameters_input = {'input': selected_input_option, 'org_id': result['org_id'], 'uid': uid}
        cursor_non_real_dict.execute(query_to_fetch_dep_id, sql_parameters_input)
        dept_id_selected = cursor_non_real_dict.fetchone()[0]
        # # fetch doctors of the selected dept id
        sql_parameters_org_id = {'org_id': result['org_id'], 'dept_id': dept_id_selected['dept_id']}
        cursor.execute(query_to_fetch_doctors_list, sql_parameters_org_id)
        doctors_list = cursor.fetchall()
        insert_doctors_as_json = {}
        data = ''
        for doctor in doctors_list:
            insert_doctors_as_json[str(doctor['sno'])] = {"doct_id": doctor['emp_id'], "doct_nm": doctor['emp_user_nm'], "selected": 0}
            data = data + department_message.format(doctor['sno'], doctor['emp_user_nm'])

        # insert all the doctors available into transaction table
        sql_parameters_for_transaction = {'doctors_list': json.dumps(insert_doctors_as_json), 'org_id': result['org_id'], 'uid': uid}
        cursor.execute(query_to_update_doctors_list, sql_parameters_for_transaction)

        # update "selected=1" for the user opted dept id
        dept_id_selected['selected'] = 1
        sql_parameters_for_transaction = {'input': int(selected_input_option), 'dept_selected_update': json.dumps(dept_id_selected), 'org_id': result['org_id'], 'uid': uid}
        cursor.execute(query_to_update_dep_id_selected, sql_parameters_for_transaction)
        conn.commit()
        response['value'] = data
        return jsonify(response)

    # time slots
    elif result['myop_node_type'] == 'timings':
        cursor_non_real_dict = conn.cursor()
        selected_input_option = request.form['input']
        # fetch the selected doct id
        sql_parameters_input = {'input': selected_input_option, 'org_id': result['org_id'], 'uid': uid}
        cursor_non_real_dict.execute(query_to_fetch_doct_id, sql_parameters_input)
        doct_id_selected = cursor_non_real_dict.fetchone()[0]

        # fetch doctors of the selected dept id
        sql_parameters_org_id = {'org_id': result['org_id'], 'dept_id': doct_id_selected['dept_id']}
        cursor.execute(query_to_fetch_doctors_list, sql_parameters_org_id)
        doctors_list = cursor.fetchall()
        insert_doctors_as_json = {}
        data = ''
        for doctor in doctors_list:
            insert_doctors_as_json[str(doctor['sno'])] = {"doct_id": doctor['emp_id'], "doct_nm": doctor['emp_user_nm'], "selected": 0}
            data = data + department_message.format(doctor['sno'], doctor['emp_user_nm'])

        # insert all the doctors available into transaction table
        sql_parameters_for_transaction = {'doctors_list': json.dumps(insert_doctors_as_json), 'org_id': result['org_id'], 'uid': uid}
        cursor.execute(query_to_update_doctors_list, sql_parameters_for_transaction)

        # update "selected=1" for the user opted dept id
        doct_id_selected['selected'] = 1
        sql_parameters_for_transaction = {'input': selected_input_option, 'selected_doct_update': doct_id_selected, 'org_id': result['org_id'], 'uid': uid}
        cursor.execute(query_to_update_doct_id_selected, sql_parameters_for_transaction)
        conn.commit()
        response['value'] = data
    elif node_id == '55555':
        pass


@app.route('/test', methods=['POST'])
def test():
    conn = threaded_postgres_sql_pool.getconn()
    cursor = conn.cursor()
    query_to_fetch_dep_id = "SELECT DEPT_LIST -> %(input)s AS DEPT_ID FROM PUBLIC.MYOPERATOR_APPOINTMENT_TEMP_TRANS WHERE ORG_ID=1333 AND MYOP_CALLER_CODE='123456'"
    param = {'input': request.form['input']}
    cursor.execute(query_to_fetch_dep_id, param)
    print(type(cursor.fetchone()[0]))

    return "success"


if __name__ == '__main__':
    app.run(host="0.0.0.0", port="5000", debug=True)
