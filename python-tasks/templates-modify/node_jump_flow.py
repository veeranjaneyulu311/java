import calendar
import datetime
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

#: constants
DEPARTMENTS_NODE_TYPE = 'departments'
DOCTORS_NODE_TYPE = 'doctors'
DAYS_NODE_TYPE = 'days'
TIME_SLOTS_NODE_TYPE = 'timings'
BOOK_APPOINTMENT_NODE_TYPE = 'bookappointment'


#: queries
query_to_fetch_node_type_and_org_id = "SELECT MYOP_NODE_TYPE, ORG_ID FROM PUBLIC.MYOPERATOR_NODE_ORG_REF WHERE MYOP_NODE_CODE=%(node_id)s"
query_to_fetch_node_id = "SELECT MYOP_NODE_CODE FROM PUBLIC.MYOPERATOR_NODE_ORG_REF WHERE MYOP_NODE_TYPE=%(node_type)s, ORG_ID=%(org_id)s"


#: node=departments
#: queries
query_to_fetch_department_list = "SELECT ROW_NUMBER () OVER (ORDER BY DEPT_NM) AS SNO,OD.DEPT_ID,DEPT.DEPT_NM FROM PUBLIC.ORGANISATION_DEPARTMENT_XREF OD JOIN DEPARTMENT_REF DEPT ON OD.DEPT_ID=DEPT.DEPT_ID WHERE ORG_ID=%(org_id)s"
query_to_insert_uid_and_department_list = "INSERT INTO PUBLIC.MYOPERATOR_APPOINTMENT_TEMP_TRANS(MYOP_CALLER_CODE, DEPT_LIST, ORG_ID) VALUES (%(caller_uid)s, %(dept_list)s, %(org_id)s)"

#: messages
department_message = 'PRESS {} FOR {}, '

#: node=doctors
#: queries
query_to_fetch_dep_id = "SELECT DEPT_LIST -> %(input)s AS DEPT_ID FROM PUBLIC.MYOPERATOR_APPOINTMENT_TEMP_TRANS WHERE ORG_ID=%(org_id)s AND MYOP_CALLER_CODE=%(uid)s"
query_to_update_dep_id_selected = "UPDATE PUBLIC.MYOPERATOR_APPOINTMENT_TEMP_TRANS SET DEPT_LIST = JSONB_SET(DEPT_LIST, '{%(input)s}', %(dept_selected_update)s) WHERE ORG_ID=%(org_id)s AND MYOP_CALLER_CODE=%(uid)s"
query_to_fetch_doctors_list = "SELECT ROW_NUMBER () OVER (ORDER BY EMP_USER_NM) AS SNO,OE.EMP_ID, REPLACE(CONCAT(INITCAP(EIR.FIRST_NM),' ',INITCAP(EIR.MIDDLE_NM),' ',INITCAP(EIR.LAST_NM)),' ',' ') AS EMP_USER_NM FROM ORGANISATION_EMPLOYEE_XREF OE JOIN EMPLOYEES_INFO_REF EIR ON EIR.EMP_ID=OE.EMP_ID JOIN EMPLOYEE_DEPT_XREF ED ON ED.EMP_ID= EIR.EMP_ID WHERE OE.ORG_ID=%(org_id)s AND DEPT_ID=%(dept_id)s AND DOCTOR_REGISTER_NO IS NOT NULL"
query_to_update_doctors_list = "UPDATE PUBLIC.MYOPERATOR_APPOINTMENT_TEMP_TRANS SET DOCTORS_LIST= %(doctors_list)s WHERE ORG_ID=%(org_id)s AND MYOP_CALLER_CODE=%(uid)s"

#: messages

#: node=days
#: queries
query_to_fetch_doct_id = "SELECT DOCTORS_LIST -> %(input)s AS DOCT_ID FROM PUBLIC.MYOPERATOR_APPOINTMENT_TEMP_TRANS WHERE ORG_ID=%(org_id)s AND MYOP_CALLER_CODE=%(uid)s"
query_to_update_doct_id_selected = "UPDATE PUBLIC.MYOPERATOR_APPOINTMENT_TEMP_TRANS SET DOCTORS_LIST = JSONB_SET(DOCTORS_LIST, '{%(input)s}', %(selected_doct_update)s) WHERE ORG_ID=%(org_id)s AND MYOP_CALLER_CODE=%(uid)s"
query_to_fetch_days = "SELECT DISTINCT(WORKING_DAY) FROM APPOINTMENT.DOCTOR_WORK_INFO_TRANS WHERE ORG_ID=%(org_id)s AND DOCTOR_ID=%(doctor_id)s AND DOCTOR_REGISTER_NO IS NOT NULL"

#: messages
doctor_available_days_message = "The doctor will be available on {} Please enter the date of appointment"

#: node=time slots
#: queries
query_to_fetch_doct_id_for_time_slot = "SELECT DOCTORS_LIST FROM PUBLIC.MYOPERATOR_APPOINTMENT_TEMP_TRANS WHERE ORG_ID=%(org_id)s AND MYOP_CALLER_CODE=%(uid)s"
query_to_fetch_time_slots = "SELECT DOCTOR_ID, START_TM, END_TM FROM APPOINTMENT.DOCTOR_WORK_INFO_TRANS WHERE ISACTIVE=TRUE AND DOCTOR_ID=%(doctor_id)s AND ORG_ID=%(org_id)s AND WORKING_DAY ilike %(day)s"
query_to_update_appointment_date = "UPDATE PUBLIC.MYOPERATOR_APPOINTMENT_TEMP_TRANS SET TIMESLOT_LIST= %(appointment_date)s WHERE ORG_ID=%(org_id)s AND MYOP_CALLER_CODE=%(uid)s"

#: messages
doctor_available_time_slots_message = "On {}/{}/{}, the doctor will be available from {}.please enter the time for booking the appointment"
slots_not_available_on_given_date_message = "The Doctor has no appointments on {}/{}/{}.Please select another date"
incorrect_date_format_message = "Please enter correct date format"


#: node=book appointment
#: queries
query_to_fetch_appointment_date = "select timeslot_list->'appointment_date' from public.myoperator_appointment_temp_trans WHERE ORG_ID=%(org_id)s AND MYOP_CALLER_CODE=%(uid)s"
# query_to_fetch_slots_booked_on_given_date = "SELECT PAT.DOCTOR_ID, DST.APPOINTMENT_DURATION, APPOINTMENT_DT FROM APPOINTMENT.PATIENT_APPOINTMENT_TRANS PAT LEFT JOIN APPOINTMENT.DOCTOR_SETTINGS_TRANS DST ON PAT.DOCTOR_ID=DST.DOCTOR_ID AND PAT.ORG_ID=DST.ORG_ID WHERE PAT.DOCTOR_ID=%(doctor_id)s AND PAT.ORG_ID=%(org_id)s AND date(APPOINTMENT_DT)=date(%(date)s) and PAT.isactive=true"
query_to_fetch_slots_booked_on_given_date = "SELECT PAT.DOCTOR_ID, DST.APPOINTMENT_DURATION, APPOINTMENT_DT FROM APPOINTMENT.PATIENT_APPOINTMENT_TRANS PAT LEFT JOIN APPOINTMENT.DOCTOR_SETTINGS_TRANS DST ON PAT.DOCTOR_ID=DST.DOCTOR_ID AND PAT.ORG_ID=DST.ORG_ID WHERE PAT.DOCTOR_ID=%(doctor_id)s AND PAT.ORG_ID=%(org_id)s AND APPOINTMENT_DT=timestamp %(appointment_starttime)s and PAT.isactive=true"
query_to_check_doctor_available = "SELECT start_tm, end_tm FROM APPOINTMENT.DOCTOR_WORK_INFO_TRANS where TO_TIMESTAMP(%(time)s, 'HH24:MI')::TIME between start_tm::time and end_tm::time and working_day = %(day)s and doctor_id = %(doctor_id)s and org_id = %(org_id)s"

#: messages
incorrect_time_format_message = "Please enter correct time format"
slot_confirmation_request_message = "The Doctor is available from {} to {}.please confirm the appointment"
slot_not_available_at_given_time_message = "The doctor has no appointments at given time"

#: logging configuration
logger = logging.getLogger("my_operator")
handler = logging.FileHandler('my_operator.log')
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.INFO)


#: connection pool;
try:
    threaded_postgres_sql_pool = psycopg2.pool.ThreadedConnectionPool(5, 15, database="drucare_dev", user="drucare_emp", password="Dru@143$care", host="192.168.1.111", port="5432")
except (Exception, psycopg2.DatabaseError) as error :
    logger.info("Error while connecting to PostgreSQL", error)


#: success response
continue_response = {"action": 'tts', "value": ''}
jump_to_node_response = {"action": 'tts', "value": '', "operation": 'jump-node', "operation_data": {"node_id": ''}}


#: the cursor object that returns the result set as list of tuples
def get_non_real_dict_cursor(conn):
    return conn.cursor()


#: the cursor object that returns the result set as list of Real Dict objects that each contains column names as keys
def get_real_dict_cursor(conn):
    return conn.cursor(cursor_factory=RealDictCursor)


#: This function gets executed when node type is departments
def fetch_departments_node(conn, org_id, uid):
    #: fetch all the departments of a organisation based on org id
    real_dict_cursor = get_real_dict_cursor(conn)
    sql_parameters_org_id = {'org_id': org_id}
    real_dict_cursor.execute(query_to_fetch_department_list, sql_parameters_org_id)
    departments_list = real_dict_cursor.fetchall()

    insert_departments_as_json = {}

    data = ''
    for department in departments_list:
        insert_departments_as_json[str(department['sno'])] = {"dept_id": department['dept_id'],
                                                                  "dept_nm": department['dept_nm'], "selected": 0}
        data = data + department_message.format(department['sno'], department['dept_nm'])

    #: insert all the departments of a organisation into my operator temp trans table
    sql_parameters_for_transaction = {'caller_uid': uid, 'dept_list': json.dumps(insert_departments_as_json), 'org_id': org_id}
    real_dict_cursor.execute(query_to_insert_uid_and_department_list, sql_parameters_for_transaction)

    #: check is organisation having exactly one department
    if len(departments_list) > 1:
        return data, None
    #: check is organisation having exactly one department
    elif len(departments_list) == 1:
        selected_input_option = "0"
        is_myoperator = False
        data, jump_node = fetch_doctors_node(conn, org_id, uid, selected_input_option, is_myoperator)
        return data
    conn.commit()


def fetch_doctors_node(conn, org_id, uid, selected_input_option, is_myoperator):
    non_real_dict_cursor = get_non_real_dict_cursor(conn)

    # fetch the selected dept id for the given selected_input_option
    sql_parameters_to_get_dept_id = {'input': selected_input_option, 'org_id': org_id, 'uid': uid}
    non_real_dict_cursor.execute(query_to_fetch_dep_id, sql_parameters_to_get_dept_id)
    dept_id_selected = non_real_dict_cursor.fetchone()[0]

    # fetch doctors of the selected dept id
    real_dict_cursor = get_real_dict_cursor(conn)
    sql_parameters_org_id = {'org_id': org_id, 'dept_id': dept_id_selected['dept_id']}
    real_dict_cursor.execute(query_to_fetch_doctors_list, sql_parameters_org_id)
    doctors_list = real_dict_cursor.fetchall()
    insert_doctors_as_json = {}
    data = ''

    for doctor in doctors_list:
        insert_doctors_as_json[str(doctor['sno'])] = {"doctor_id": doctor['emp_id'], "doctor_nm": doctor['emp_user_nm'],
                                                      "selected": 0}
        data = data + department_message.format(doctor['sno'], doctor['emp_user_nm'])

    # insert all the doctors available into transaction table
    sql_parameters_for_transaction = {'doctors_list': json.dumps(insert_doctors_as_json), 'org_id': org_id, 'uid': uid}
    real_dict_cursor.execute(query_to_update_doctors_list, sql_parameters_for_transaction)

    # update "selected=1" for the user opted dept id
    dept_id_selected['selected'] = 1
    sql_parameters_for_transaction = {'input': int(selected_input_option),
                                      'dept_selected_update': json.dumps(dept_id_selected), 'org_id': org_id,
                                      'uid': uid}
    real_dict_cursor.execute(query_to_update_dep_id_selected, sql_parameters_for_transaction)

    #: check is department having more than one doctor
    if len(doctors_list) > 1:
        conn.commit()
        if is_myoperator:
            return data, None
        else:
            non_real_dict_cursor.execute(query_to_fetch_node_id, {'org_id': org_id, 'node_type': DAYS_NODE_TYPE})
            jump_node = non_real_dict_cursor.fetchone()[0]
            return data, jump_node

    #: check is department having exactly one doctor
    elif len(doctors_list) == 1:
        is_myoperator = False
        data, jump_node = fetch_days_node(conn, org_id, uid, selected_input_option, is_myoperator)
        conn.commit()
        return data, jump_node


def fetch_days_node(conn, org_id, uid, selected_input_option, is_myoperator):
    non_real_dict_cursor = get_non_real_dict_cursor(conn)

    # fetch doctor_id for the selected input
    sql_parameters_input = {'input': selected_input_option, 'org_id': org_id, 'uid': uid}
    non_real_dict_cursor.execute(query_to_fetch_doct_id, sql_parameters_input)
    doct_id_selected = non_real_dict_cursor.fetchone()[0]

    # fetch working days of the selected doctor id
    sql_parameters_org_id = {'org_id': org_id, 'doctor_id': doct_id_selected['doctor_id']}
    non_real_dict_cursor.execute(query_to_fetch_days, sql_parameters_org_id)
    available_days = non_real_dict_cursor.fetchall()

    data = ""
    for day in available_days:
        data = data + day[0] + ","

    # update "selected=1" for the user opted dept id
    real_dict_cursor = get_real_dict_cursor(conn)
    doct_id_selected['selected'] = 1
    sql_parameters_for_transaction = {'input': int(selected_input_option),
                                      'selected_doct_update': json.dumps(doct_id_selected), 'org_id': org_id,
                                      'uid': uid}
    real_dict_cursor.execute(query_to_update_doct_id_selected, sql_parameters_for_transaction)
    conn.commit()
    data = doctor_available_days_message.format(data)
    if is_myoperator:
        return data, None
    else:
        non_real_dict_cursor.execute(query_to_fetch_node_id, {'org_id': org_id, 'node_type': TIME_SLOTS_NODE_TYPE})
        jump_node = non_real_dict_cursor.fetchone()[0]
        return data, jump_node


def fetch_timings_node(conn, org_id, uid, selected_input_option):
    non_real_dict_cursor = get_non_real_dict_cursor(conn)
    appointment_date = selected_input_option

    if len(appointment_date) == 3:
        day = int(appointment_date[0])
        month = int(appointment_date[1:])
        year = datetime.datetime.now().year
    elif len(appointment_date) == 4:
        day = int(appointment_date[0:2])
        month = int(appointment_date[2:])
        year = datetime.datetime.now().year
    elif len(appointment_date) > 4:
        return incorrect_date_format_message

    # used in book appointment
    appointment_day_name = calendar.day_name[calendar.weekday(year, month, day)]

    # fetch the doctors list for finding the doctor id that is selected by the user
    sql_parameters_input = {'org_id': org_id, 'uid': uid}
    non_real_dict_cursor.execute(query_to_fetch_doct_id_for_time_slot, sql_parameters_input)
    doct_list = non_real_dict_cursor.fetchone()[0]

    # inserting the date given by user
    appointment_date = {'appointment_date': str(day) + '-' + str(month) + '-' + str(year)}
    sql_parameters_for_update_date = {'org_id': org_id, 'uid': uid, 'appointment_date': json.dumps(appointment_date)}
    non_real_dict_cursor.execute(query_to_update_appointment_date, sql_parameters_for_update_date)

    doctor_id = ''
    for doctor in doct_list.values():
        if doctor['selected'] == 1:
            doctor_id = doctor['doctor_id']
            break

    # fetch the time slots available for above fetched doctor id on on user selected date
    real_dict_cursor = get_real_dict_cursor(conn)
    sql_parameters_for_time_slots = {'org_id': org_id, 'doctor_id': doctor_id, 'day': appointment_day_name}
    real_dict_cursor.execute(query_to_fetch_time_slots, sql_parameters_for_time_slots)
    available_time_slots = real_dict_cursor.fetchall()
    print(available_time_slots)
    message = doctor_available_time_slots_message
    if len(available_time_slots) != 0:
        timings = ""
        for time_slot in available_time_slots:
            # slice the start and end timings of the each slot
            start_hours = int(time_slot['start_tm'][0:2])
            start_minutes = int(time_slot['start_tm'][3:])
            end_hours = int(time_slot['end_tm'][0:2])
            end_minutes = int(time_slot['end_tm'][3:])

            # conditions to check the time AM or PM
            if 12 < start_hours <= 24:
                timings = timings + str(start_hours - 12) + ":" + str(start_minutes) + "PM"
            else:
                timings = timings + str(start_hours) + ":" + str(start_minutes) + "AM"

            if 12 < end_hours <= 24:
                timings = timings + " TO " + str(end_hours - 12) + ":" + str(end_minutes) + "PM,"
            else:
                timings = timings + " TO " + str(end_hours) + ":" + str(end_minutes) + "AM,"

        message = message.format(str(day), str(month), str(year), timings)
        conn.commit()

    else:
        message = slots_not_available_on_given_date_message.format(str(day), str(month), str(year))

    return message, None


def book_appointment_node(conn, org_id, uid, selected_input_option):
    non_real_dict_cursor = get_non_real_dict_cursor(conn)
    patient_given_appointment_time = selected_input_option
    message = ""
    hours = 0
    minutes = 0
    doctor_id = ''

    #: checking is time format given by patient is valid or not
    if len(patient_given_appointment_time) == 1:
        hours = int(patient_given_appointment_time)
    elif len(patient_given_appointment_time) == 2:
        hours = int(patient_given_appointment_time)
    elif len(patient_given_appointment_time) == 3:
        hours = int(patient_given_appointment_time[0])
        minutes = int(patient_given_appointment_time[1:])
    elif len(patient_given_appointment_time) == 4:
        hours = int(patient_given_appointment_time[0:2])
        minutes = int(patient_given_appointment_time[2:])
    elif len(patient_given_appointment_time) > 4:
        return incorrect_time_format_message

    print(hours, minutes)

    #: fetch the appointment date
    sql_parameters_for_fetching_patient_entered_date = {'org_id': org_id, 'uid': uid}
    non_real_dict_cursor.execute(query_to_fetch_appointment_date, sql_parameters_for_fetching_patient_entered_date)
    patient_given_appointment_date = non_real_dict_cursor.fetchone()[0]
    patient_given_appointment_date = datetime.datetime.strptime(patient_given_appointment_date, '%d-%m-%Y').strftime(
        '%Y-%m-%d')

    # fetch the doctors list for finding the doctor id that is selected by the user
    non_real_dict_cursor.execute(query_to_fetch_doct_id_for_time_slot, sql_parameters_for_fetching_patient_entered_date)
    doct_list = non_real_dict_cursor.fetchone()[0]

    for doctor in doct_list.values():
        if doctor['selected'] == 1:
            doctor_id = doctor['doctor_id']
            break

    print(doctor_id)
    print(patient_given_appointment_date)

    #: case-1:first check weather doctor will available at the patient_given_appointment_time on patient_given_appointment_date
    appointment_day_name = calendar.day_name[
        datetime.datetime.strptime(patient_given_appointment_date, '%Y-%m-%d').weekday()]
    patient_given_appointment_time = str(hours) + ':' + str(minutes)

    real_dict_cursor = get_real_dict_cursor(conn)
    sql_parameters_to_check_doctor_available = {'org_id': org_id, 'time': patient_given_appointment_time,
                                                'day': appointment_day_name, 'doctor_id': doctor_id}
    real_dict_cursor.execute(query_to_check_doctor_available, sql_parameters_to_check_doctor_available)
    result = real_dict_cursor.fetchall()

    if len(result) != 0:
        slot_available_at_given_time = dict(result[0])
        #: check if any slot is free in available time period
        #: fetch slots already booked on the patient given date at patient given time
        appointment_start_time = patient_given_appointment_date + ' ' + slot_available_at_given_time['start_tm']
        print(appointment_start_time)
        sql_parameters_for_booked_slots = {'org_id': org_id, 'doctor_id': doctor_id,
                                           'appointment_starttime': appointment_start_time}
        real_dict_cursor.execute(query_to_fetch_slots_booked_on_given_date, sql_parameters_for_booked_slots)
        slots_booked_on_given_date = real_dict_cursor.fetchall()
        start_time = slot_available_at_given_time['start_tm']
        end_time = slot_available_at_given_time['end_tm']

        #: condition to check is all slots at given time are booked or not
        if len(slots_booked_on_given_date) == 0:
            return slot_confirmation_request_message.format(start_time, end_time)

        else:
            # find no of slots get booked on given time
            each_slot_duration = dict(slots_booked_on_given_date[0])['appointment_duration']
            no_of_slots_completed = len(slots_booked_on_given_date)
            timedelta_total_no_of_slots_available = datetime.datetime.strptime(end_time,
                                                                               '%H:%M') - datetime.datetime.strptime(
                start_time, '%H:%M')
            total_no_of_slots_available = timedelta_total_no_of_slots_available.seconds / 60
            print(start_time, end_time, "Time Period of Appointment")
            print(int(total_no_of_slots_available / each_slot_duration), "total")
            print(no_of_slots_completed, "booked")
            print("Each Slot Duration: ", each_slot_duration, "seconds")
            # response message for the node id related to time slot of appointment.
            message = slot_confirmation_request_message.format(start_time, end_time)

    else:
        message = slot_not_available_at_given_time_message

    return message, None


#: This function executes for organisations with single departments
def flow_for_organisation_with_single_department(conn, org_id, uid, departments_list):
    data = ''
    insert_departments_as_json = {}

    #: convert Real dict to dict
    department = dict(departments_list[0])

    #: get cursor object for inserting data
    real_dict_cursor = get_real_dict_cursor(conn)

    insert_departments_as_json[str(department['sno'])] = {"dept_id": department['dept_id'], "dept_nm": department['dept_nm'], "selected": 1}

    #: insert the department of a organisation into my operator temp trans table
    sql_parameters_for_inserting_department = {'caller_uid': uid, 'dept_list': json.dumps(insert_departments_as_json), 'org_id': org_id}
    real_dict_cursor.execute(query_to_insert_uid_and_department_list, sql_parameters_for_inserting_department)

    return data


#: This function executes for organisations with single departments
def flow_for_organisation_with_single_department(conn, org_id, uid, departments_list):
    data = ''
    insert_departments_as_json = {}

    #: convert Real dict to dict
    department = dict(departments_list[0])

    #: get cursor object for inserting data
    real_dict_cursor = get_real_dict_cursor(conn)

    insert_departments_as_json[str(department['sno'])] = {"dept_id": department['dept_id'], "dept_nm": department['dept_nm'], "selected": 1}

    #: insert the department of a organisation into my operator temp trans table
    sql_parameters_for_inserting_department = {'caller_uid': uid, 'dept_list': json.dumps(insert_departments_as_json), 'org_id': org_id}
    real_dict_cursor.execute(query_to_insert_uid_and_department_list, sql_parameters_for_inserting_department)

    return data


#: This Api takes node id as input and returns corresponding input
@app.route('/bookAppointment', methods=['POST'])
def fetch_all():

    #: read request data from my operator
    uid = request.form["uid"]
    node_id = request.form['node_id']
    clid = request.form['clid']

    #: get db connection from pool
    conn = threaded_postgres_sql_pool.getconn()

    #: fetch the node type and org id for the given node id
    real_dict_cursor = conn.cursor(cursor_factory=RealDictCursor)
    sql_parameters_node_id = {'node_id': node_id}
    real_dict_cursor.execute(query_to_fetch_node_type_and_org_id, sql_parameters_node_id)
    node_type_and_org_id = real_dict_cursor.fetchone()

    org_id = node_type_and_org_id['org_id']
    node_type = node_type_and_org_id['myop_node_type']
    message = ""
    jump_node = None

    #: fetching departments of an organization for given node id
    if node_type == DEPARTMENTS_NODE_TYPE:
        message, jump_node = fetch_departments_node(conn, org_id, uid)

    #: fetching doctors of a department based on department id
    elif node_type == DOCTORS_NODE_TYPE:
        selected_input_option = request.form['input']
        message, jump_node = fetch_doctors_node(conn, org_id, uid, selected_input_option)

    #: fetching days of a doctor based on doctor id
    elif node_type == DAYS_NODE_TYPE:
        selected_input_option = request.form['input']
        message, jump_node = fetch_days_node(conn, org_id, uid, selected_input_option)

    #: fetching timings of a day based on day
    elif node_type == TIME_SLOTS_NODE_TYPE:
        selected_input_option = request.form['input']
        message, jump_node = fetch_timings_node(conn, org_id, uid, selected_input_option)

    #: book appointment based on user given time
    elif node_type == BOOK_APPOINTMENT_NODE_TYPE:
        selected_input_option = request.form['input']
        message, jump_node = book_appointment_node(conn, org_id, uid, selected_input_option)

    threaded_postgres_sql_pool.putconn(conn)

    #: It checks for weather flow need to be continue or have to jump
    if jump_node is None:
        continue_response['value'] = message
        return jsonify(continue_response)
    else:
        jump_to_node_response['value'] = message
        jump_to_node_response['operation_data']['node_id'] = jump_node
        return jsonify(jump_to_node_response)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port="5000", debug=True)
