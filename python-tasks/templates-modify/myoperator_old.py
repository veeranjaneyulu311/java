import calendar
import datetime
import json
import logging
import os
import time
import traceback
import uuid

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

#: Constants
# =========== #

#: 1.Db configuration
#: Dev
DB_NM = "drucare_dev"
DB_USER_NM = "drucare_emp"
DB_PWD = "Dru@143$care"
DB_HOST = "192.168.1.111"
DB_PORT = "5432"
DB_MIN_CONNECTIONS = 5
DB_MAX_CONNECTIONS = 15

#: 2.My Operator Nodes
DEPARTMENTS_NODE_TYPE = 'departments'
DOCTORS_NODE_TYPE = 'doctors'
DAYS_NODE_TYPE = 'days'
TIME_SLOTS_NODE_TYPE = 'timings'
BOOK_APPOINTMENT_NODE_TYPE = 'bookappointment'
CONFIRM_APPOINTMENT_NODE_TYPE = 'confirmappointment'

#: 3.Patient Id Generation
APPLICATION_SETTINGS_ID = 1
SETTINGS_ORG_ID = 1

#: Queries And Messages
# ===================== #

#: queries required for all nodes
query_to_fetch_node_type_and_org_id = "SELECT MYOP_NODE_TYPE, ORG_ID FROM PUBLIC.MYOPERATOR_NODE_ORG_REF WHERE MYOP_NODE_CODE=%(node_id)s"
query_to_fetch_node_id = "SELECT MYOP_NODE_CODE FROM PUBLIC.MYOPERATOR_NODE_ORG_REF WHERE MYOP_NODE_TYPE=%(node_type)s, ORG_ID=%(org_id)s"


#: queries and messages required for node_type=departments
#: queries
query_to_fetch_department_list = "SELECT ROW_NUMBER () OVER (ORDER BY DEPT_NM) AS SNO, count(edx.dept_id), edx.dept_id,d.dept_nm FROM public.employee_dept_xref edx join public.employee_designation_xref ed on edx.emp_id=ed.emp_id and ed.isactive=true and designation_id=1 join public.organisation_employee_xref eir on edx.emp_id=eir.emp_id and eir.org_id=%(org_id)s join employees_info_ref ei on ei.emp_id=edx.emp_id join department_ref d on edx.dept_id=d.dept_id where edx.isactive=true and ei.isactive=true group by edx.dept_id,d.dept_nm order by dept_id"
query_to_insert_uid_and_mobile_no_and_department_list = "INSERT INTO PUBLIC.MYOPERATOR_APPOINTMENT_TEMP_TRANS(MYOP_CALLER_CODE, DEPT_LIST, ORG_ID, MOBILE_NO) VALUES (%(caller_uid)s, %(dept_list)s, %(org_id)s, %(mobile_no)s)"

#: messages
department_select = 'Please select the department '
department_message = 'PRESS {} FOR {}, '

#: queries and messages required for node_type=doctors
#: queries
query_to_fetch_dep_id = "SELECT DEPT_LIST -> %(input)s AS DEPT_ID FROM PUBLIC.MYOPERATOR_APPOINTMENT_TEMP_TRANS WHERE ORG_ID=%(org_id)s AND MYOP_CALLER_CODE=%(uid)s"
query_to_update_dep_id_selected = "UPDATE PUBLIC.MYOPERATOR_APPOINTMENT_TEMP_TRANS SET DEPT_LIST = JSONB_SET(DEPT_LIST, '{%(input)s}', %(dept_selected_update)s) WHERE ORG_ID=%(org_id)s AND MYOP_CALLER_CODE=%(uid)s"
query_to_fetch_doctors_list = "SELECT ROW_NUMBER () OVER (ORDER BY EMP_USER_NM) AS SNO,OE.EMP_ID, REPLACE(CONCAT(INITCAP(EIR.FIRST_NM),' ',INITCAP(EIR.MIDDLE_NM),' ',INITCAP(EIR.LAST_NM)),' ',' ') AS EMP_USER_NM FROM ORGANISATION_EMPLOYEE_XREF OE JOIN EMPLOYEES_INFO_REF EIR ON EIR.EMP_ID=OE.EMP_ID JOIN EMPLOYEE_DEPT_XREF ED ON ED.EMP_ID= EIR.EMP_ID WHERE OE.ORG_ID=%(org_id)s AND DEPT_ID=%(dept_id)s AND DOCTOR_REGISTER_NO IS NOT NULL"
query_to_update_doctors_list = "UPDATE PUBLIC.MYOPERATOR_APPOINTMENT_TEMP_TRANS SET DOCTORS_LIST= %(doctors_list)s WHERE ORG_ID=%(org_id)s AND MYOP_CALLER_CODE=%(uid)s"

#: messages
doctor_select = 'Please select the doctor '

#: queries and messages required for node_type=days
#: queries
query_to_fetch_doct_id = "SELECT DOCTORS_LIST -> %(input)s AS DOCT_ID FROM PUBLIC.MYOPERATOR_APPOINTMENT_TEMP_TRANS WHERE ORG_ID=%(org_id)s AND MYOP_CALLER_CODE=%(uid)s"
query_to_update_doct_id_selected = "UPDATE PUBLIC.MYOPERATOR_APPOINTMENT_TEMP_TRANS SET DOCTORS_LIST = JSONB_SET(DOCTORS_LIST, '{%(input)s}', %(selected_doct_update)s) WHERE ORG_ID=%(org_id)s AND MYOP_CALLER_CODE=%(uid)s"
query_to_fetch_days = "SELECT DISTINCT(WORKING_DAY) FROM APPOINTMENT.DOCTOR_WORK_INFO_TRANS WHERE ORG_ID=%(org_id)s AND DOCTOR_ID=%(doctor_id)s AND DOCTOR_REGISTER_NO IS NOT NULL"

#: messages
doctor_available_days_message = "The doctor will be available on {} Please enter the date of appointment in dd mm format"

#: queries and messages required for node_type=time slots
#: queries
query_to_fetch_doct_id_for_time_slot = "SELECT DOCTORS_LIST FROM PUBLIC.MYOPERATOR_APPOINTMENT_TEMP_TRANS WHERE ORG_ID=%(org_id)s AND MYOP_CALLER_CODE=%(uid)s"
query_to_fetch_time_slots = "SELECT DOCTOR_ID, START_TM, END_TM FROM APPOINTMENT.DOCTOR_WORK_INFO_TRANS WHERE ISACTIVE=TRUE AND DOCTOR_ID=%(doctor_id)s AND ORG_ID=%(org_id)s AND WORKING_DAY ilike %(day)s"
query_to_update_appointment_date = "UPDATE PUBLIC.MYOPERATOR_APPOINTMENT_TEMP_TRANS SET TIMESLOT_LIST= %(appointment_date)s WHERE ORG_ID=%(org_id)s AND MYOP_CALLER_CODE=%(uid)s"

#: messages
doctor_available_time_slots_message = "On your given date, the doctor will be available from {}.please enter the time in twenty four hours format for booking the appointment as hours and minutes"
slots_not_available_on_given_date_message = "The Doctor has no appointments on Your given date.Please book appointment on another date"
incorrect_date_format_message = "Please enter correct date format.It should be three or four numbers"
invalid_day_or_month = "please enter valid day and month"


#: queries and messages required for node_type=book appointment
#: queries
query_to_fetch_appointment_date = "select timeslot_list->'appointment_date' from public.myoperator_appointment_temp_trans WHERE ORG_ID=%(org_id)s AND MYOP_CALLER_CODE=%(uid)s"
query_to_fetch_slots_booked_on_given_date = "SELECT PAT.DOCTOR_ID, DST.APPOINTMENT_DURATION, APPOINTMENT_DT FROM APPOINTMENT.PATIENT_APPOINTMENT_TRANS PAT LEFT JOIN APPOINTMENT.DOCTOR_SETTINGS_TRANS DST ON PAT.DOCTOR_ID=DST.DOCTOR_ID AND PAT.ORG_ID=DST.ORG_ID WHERE PAT.DOCTOR_ID=%(doctor_id)s AND PAT.ORG_ID=%(org_id)s AND APPOINTMENT_DT=timestamp %(appointment_starttime)s and PAT.isactive=true"
query_to_check_doctor_available = "SELECT start_tm, end_tm FROM APPOINTMENT.DOCTOR_WORK_INFO_TRANS where TO_TIMESTAMP(%(time)s, 'HH24:MI')::TIME between start_tm::time and end_tm::time and working_day = %(day)s and doctor_id = %(doctor_id)s and org_id = %(org_id)s"
query_to_update_appointment_time = "UPDATE PUBLIC.MYOPERATOR_APPOINTMENT_TEMP_TRANS SET TIMESLOT_LIST= %(appointment_time)s WHERE ORG_ID=%(org_id)s AND MYOP_CALLER_CODE=%(uid)s"
query_to_fetch_next_nearest_time_slot = "SELECT start_tm, end_tm FROM APPOINTMENT.DOCTOR_WORK_INFO_TRANS where TO_TIMESTAMP(%(time)s, 'HH24:MI')::TIME < start_tm::time and working_day = %(day)s and doctor_id = %(doctor_id)s and org_id = %(org_id)s order by start_tm::time limit 1"


#: messages
incorrect_time_format_message = "Please enter correct time format. it should not be more than four numbers."
invalid_time_message = "enter valid hours and minutes"
slot_confirmation_request_message = "The Doctor is available from {} to {}.press one to confirm the appointment and two to cancel the appointment"
slot_not_available_at_given_time_message = "The doctor has no appointments at your given time."
next_available_slot_for_given_time_message = "The doctor is having slot from {} to {}. press one to confirm the appointment and two to cancel the appointment"


#: queries and messages required for node_type=confirm appointment
#: queries
query_to_update_booking_status_on_confirmation = "update public.myoperator_appointment_temp_trans set is_booked= %(is_confirmed)s where org_id=%(org_id)s and myop_caller_code=%(uid)s"
query_to_fetch_patient_appoi_details = "select myop_caller_code, dept_list, doctors_list, timeslot_list	FROM public.myoperator_appointment_temp_trans where org_id=%(org_id)s and myop_caller_code=%(uid)s"
query_update_appointment_details_in_appointment_trans = "insert into appointment.patient_appointment_trans(patient_id,appointment_dt,org_id,dept_id,doctor_id,appointment_type) values(%(patient_id)s,%(appointment_dt)s::timestamp without time zone,%(org_id)s,%(dept_id)s,%(doctor_id)s,%(appointment_type)s)"
query_to_delete_booking_data_on_cancellation = "delete from public.myoperator_appointment_temp_trans where org_id=%(org_id)s and myop_caller_code=%(uid)s"

#: messages
confirmation_message = "Your appointment is confirmed"
cancellation_message = "Your appointment is cancelled"
invalid_input_message = "please enter valid option"

#: queries required for patient registration
fetch_application_org_settings = "SELECT ORG_SETTING_ID,SETTING_ID,ORG_ID,PREFIX, IS_DATE_REQUIRED,DATE_FORMAT,LENGTH,PRE_FIX_POSITION FROM PUBLIC.APPLICATION_ORG_SETTINGS_TRANS WHERE SETTING_ID=%(setting_id)s AND ORG_ID=%(org_id)s"
query_for_patient_registration = "insert into patient_info_ref(patient_id,mobile_no) values(%(patient_id)s,%(mobile_no)s)"
query_for_mapping_patient_to_org ="INSERT INTO PUBLIC.PATIENT_ORGANISATION_XREF(PATIENT_ID, ORG_ID) VALUES ( %(patient_id)s, %(org_id)s )"


#: logging configuration
logger = logging.getLogger("my_operator")
handler = logging.FileHandler('my_operator.log')
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.INFO)


#: connection pool;
try:
    threaded_postgres_sql_pool = psycopg2.pool.ThreadedConnectionPool(DB_MIN_CONNECTIONS, DB_MAX_CONNECTIONS, database=DB_NM, user=DB_USER_NM, password=DB_PWD, host=DB_HOST, port=DB_PORT)

except (Exception, psycopg2.DatabaseError) as error:
    logger.info("Error while connecting to PostgreSQL", error)


#: success response
success_response = {"action": 'tts', "value": ''}


# It returns the computer name from environment variables. otherwise Unknown Computer
def get_computer_name():
        if os.getenv('HOSTNAME') is not None:
                return os.getenv('HOSTNAME')
        elif os.getenv('COMPUTERNAME') is not None:
                return os.getenv('COMPUTERNAME')
        else:
                return 'Unknown Computer'


#: the cursor object that returns the result set as list of tuples
def get_non_real_dict_cursor(conn):
    return conn.cursor()


#: the cursor object that returns the result set as list of Real Dict objects containing column names as keys
def get_real_dict_cursor(conn):
    return conn.cursor(cursor_factory=RealDictCursor)


#: This function gets executed when node type is departments
def fetch_departments_node(conn, org_id, uid, mobile_no):
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

    data = department_select + data
    #: insert all the departments of a organisation into my operator temp trans table
    sql_parameters_for_transaction = {'caller_uid': uid, 'dept_list': json.dumps(insert_departments_as_json), 'org_id': org_id, 'mobile_no': mobile_no}
    real_dict_cursor.execute(query_to_insert_uid_and_mobile_no_and_department_list, sql_parameters_for_transaction)

    #: check is organisation having exactly one department
    if len(departments_list) > 1:
        # for multi department clinic
        return data
    #: check is organisation having exactly one department
    elif len(departments_list) == 1:
        selected_input_option = "1"
        if dict(departments_list[0])['count'] == 1:  #: single department and single doctor
            # single department with single doctor clinic
            fetch_doctors_node(conn, org_id, uid, selected_input_option)
            data = fetch_days_node(conn, org_id, uid, selected_input_option)
        else:
            # single department with multiple doctors clinic
            data = fetch_doctors_node(conn, org_id, uid, selected_input_option)
        return data


#: This function gets executed when node type is doctors
def fetch_doctors_node(conn, org_id, uid, selected_input_option):
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

    data = doctor_select + data
    # insert all the doctors available into transaction table
    sql_parameters_for_transaction = {'doctors_list': json.dumps(insert_doctors_as_json), 'org_id': org_id, 'uid': uid}
    real_dict_cursor.execute(query_to_update_doctors_list, sql_parameters_for_transaction)

    # update "selected=1" for the user opted dept id
    dept_id_selected['selected'] = 1
    sql_parameters_for_transaction = {'input': int(selected_input_option),
                                      'dept_selected_update': json.dumps(dept_id_selected), 'org_id': org_id,
                                      'uid': uid}
    real_dict_cursor.execute(query_to_update_dep_id_selected, sql_parameters_for_transaction)
    return data


#: This function gets executed when node type is days
def fetch_days_node(conn, org_id, uid, selected_input_option):
    non_real_dict_cursor = get_non_real_dict_cursor(conn)

    # fetch doctor_id for the selected input
    sql_parameters_input = {'input': selected_input_option, 'org_id': org_id, 'uid': uid}
    non_real_dict_cursor.execute(query_to_fetch_doct_id, sql_parameters_input)
    doct_id_selected = non_real_dict_cursor.fetchone()[0]

    # fetch working days of the selected doctor id
    sql_parameters_org_id = {'org_id': org_id, 'doctor_id': doct_id_selected['doctor_id']}
    non_real_dict_cursor.execute(query_to_fetch_days, sql_parameters_org_id)
    available_days = non_real_dict_cursor.fetchall()
    available_days = [day[0] for day in available_days]

    data = ""
    days = ['monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    for day in days:
        if day in available_days:
            data = data + day + ","

    # update "selected=1" for the user opted dept id
    real_dict_cursor = get_real_dict_cursor(conn)
    doct_id_selected['selected'] = 1
    sql_parameters_for_transaction = {'input': int(selected_input_option),
                                      'selected_doct_update': json.dumps(doct_id_selected), 'org_id': org_id,
                                      'uid': uid}
    real_dict_cursor.execute(query_to_update_doct_id_selected, sql_parameters_for_transaction)

    data = doctor_available_days_message.format(data)
    return data


#: This function gets executed when node type is timings
#: in given input date,
#: out of 3 or 4 digits,last two numbers are taken as month and remaining as day
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
    # if enter date is more than 4 digits
    elif len(appointment_date) < 3 or len(appointment_date) > 4:
        return incorrect_date_format_message

    # used in book appointment
    try:
        appointment_day_name = calendar.day_name[calendar.weekday(year, month, day)]
    except Exception:
        return invalid_day_or_month

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

        message = message.format(timings)

    else:
        message = slots_not_available_on_given_date_message

    return message


#: fetch slots already booked on the patient given date at patient given time
def fetch_slots_already_booked(real_dict_cursor, appointment_start_time, org_id, doctor_id):

    #: fetch slots already booked on the patient given date at patient given time
    sql_parameters_for_booked_slots = {'org_id': org_id, 'doctor_id': doctor_id,
                                       'appointment_starttime': appointment_start_time}
    real_dict_cursor.execute(query_to_fetch_slots_booked_on_given_date, sql_parameters_for_booked_slots)
    return real_dict_cursor.fetchall()


# it returns no of slots available in the given period
def get_no_of_slots_remaining(slots_booked_on_given_date, start_time, end_time):
    # find no of slots get booked on given time
    each_slot_duration = dict(slots_booked_on_given_date[0])['appointment_duration']
    no_of_slots_completed = len(slots_booked_on_given_date)
    timedelta_total_no_of_slots_available = datetime.datetime.strptime(end_time,
                                                                       '%H:%M') - datetime.datetime.strptime(
        start_time, '%H:%M')
    slot_duration_in_minutes = timedelta_total_no_of_slots_available.seconds / 60
    total_no_of_slots_available = int(slot_duration_in_minutes / each_slot_duration)
    slots_remaining = total_no_of_slots_available - no_of_slots_completed
    return slots_remaining


# it returns next nearest slot based on patient given time if available
def get_nearest_time_slot(conn, sql_parameters_to_get_nearest_slot, patient_given_appointment_date, org_id, doctor_id, uid):
    non_real_dict_cursor = get_non_real_dict_cursor(conn)
    non_real_dict_cursor.execute(query_to_fetch_next_nearest_time_slot, sql_parameters_to_get_nearest_slot)
    next_slot = non_real_dict_cursor.fetchone()
    # next slot is None if not available
    if next_slot is None:
        return slot_not_available_at_given_time_message
    else:
        real_dict_cursor = get_real_dict_cursor(conn)
        start_time = next_slot[0]
        end_time = next_slot[1]

        #: check if any slot is free in available time period
        appointment_start_time = patient_given_appointment_date + ' ' + start_time
        slots_booked_on_given_date = fetch_slots_already_booked(real_dict_cursor, appointment_start_time, org_id, doctor_id)

        if len(slots_booked_on_given_date) == 0:
            # it indicates all slots are free and go for confirmation of appointment
            sql_parameters_for_update_time = {'org_id': org_id, 'uid': uid, 'appointment_time': json.dumps({'appointment_date_time': appointment_start_time})}
            real_dict_cursor.execute(query_to_update_appointment_time, sql_parameters_for_update_time)
            res_message = slot_not_available_at_given_time_message + next_available_slot_for_given_time_message.format(start_time, end_time)

        # it indicates few or all slots are booked and go for confirmation of appointment
        else:
            slots_remaining = get_no_of_slots_remaining(slots_booked_on_given_date, start_time, end_time)

            # if doctor has appointment at given time but slots are full.check is next slot available
            if slots_remaining == 0:
                res_message = slot_not_available_at_given_time_message
            else:
                sql_parameters_for_update_time = {'org_id': org_id, 'uid': uid, 'appointment_time': json.dumps({'appointment_date_time': appointment_start_time})}
                real_dict_cursor.execute(query_to_update_appointment_time, sql_parameters_for_update_time)
                res_message = slot_not_available_at_given_time_message + next_available_slot_for_given_time_message.format(start_time, end_time)

        return res_message


#: This function gets executed when node type is book appointment
#: in given input time,
#: out of 3 or 4 digits,last two numbers are taken as minutes and remaining as hours
def book_appointment_node(conn, org_id, uid, selected_input_option):
    non_real_dict_cursor = get_non_real_dict_cursor(conn)
    patient_given_appointment_time = selected_input_option
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

    #: check for incorrect hours and minutes
    if hours > 24 or minutes > 60:
        return invalid_time_message

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

    #: case-1:first check weather doctor will be available at the patient_given_appointment_time on patient_given_appointment_date
    appointment_day_name = calendar.day_name[
        datetime.datetime.strptime(patient_given_appointment_date, '%Y-%m-%d').weekday()]
    patient_given_appointment_time = str(hours) + ':' + str(minutes)

    real_dict_cursor = get_real_dict_cursor(conn)
    sql_parameters_to_check_doctor_available = {'org_id': org_id, 'time': patient_given_appointment_time,
                                                'day': appointment_day_name, 'doctor_id': doctor_id}

    real_dict_cursor.execute(query_to_check_doctor_available, sql_parameters_to_check_doctor_available)
    # gets start time and end time
    result = real_dict_cursor.fetchall()

    # True if doctor available
    if len(result) != 0:
        slot_available_at_given_time = dict(result[0])
        start_time = slot_available_at_given_time['start_tm']
        end_time = slot_available_at_given_time['end_tm']

        #: check if any slot is free in available time period
        appointment_start_time = patient_given_appointment_date + ' ' + start_time
        slots_booked_on_given_date = fetch_slots_already_booked(real_dict_cursor, appointment_start_time, org_id, doctor_id)

        #: condition to check is all slots at given time are booked or not
        if len(slots_booked_on_given_date) == 0:
            # it indicates all slots are free and go for confirmation of appointment
            sql_parameters_for_update_time = {'org_id': org_id, 'uid': uid, 'appointment_time': json.dumps({'appointment_date_time': appointment_start_time})}
            real_dict_cursor.execute(query_to_update_appointment_time, sql_parameters_for_update_time)
            return slot_confirmation_request_message.format(start_time, end_time)

        # it indicates few or all slots are booked and go for confirmation of appointment
        else:
            slots_remaining = get_no_of_slots_remaining(slots_booked_on_given_date, start_time, end_time)

            # if doctor has appointment at given time but slots are full.check is next slot available
            if slots_remaining == 0:
                message = get_nearest_time_slot(conn, sql_parameters_to_check_doctor_available, patient_given_appointment_date,org_id, doctor_id, uid)
            else:
                sql_parameters_for_update_time = {'org_id': org_id, 'uid': uid, 'appointment_time': json.dumps({'appointment_date_time': appointment_start_time})}
                real_dict_cursor.execute(query_to_update_appointment_time, sql_parameters_for_update_time)
                message = slot_confirmation_request_message.format(start_time, end_time)

    else:
        # if doctor has no appointment at given time.check is next slot available
        message = get_nearest_time_slot(conn, sql_parameters_to_check_doctor_available, patient_given_appointment_date, org_id, doctor_id, uid)

    return message


#: stores the appointment status in existing appointment trans table if confirmed
def confirm_appointment_node(conn, org_id, uid, selected_input_option, mobile_no):
    real_dict_cursor = get_real_dict_cursor(conn)

    if int(selected_input_option) == 1:
        # update is_confirmed column value to true
        sql_parameters_for_confirmation = {'org_id': org_id, 'uid': uid, 'is_confirmed': True}
        real_dict_cursor.execute(query_to_update_booking_status_on_confirmation, sql_parameters_for_confirmation)

        # step:1 creating the patient id
        patient_id = register_patient(conn, mobile_no)
        # step:2 mapping the patient id to organisation
        map_patient_to_org(conn, org_id, patient_id)

        # fetch all the patient appointment details from my operator temp table
        sql_parameters_for_fetching_appoi_deatils = {'org_id': org_id, 'uid': uid}
        real_dict_cursor.execute(query_to_fetch_patient_appoi_details, sql_parameters_for_fetching_appoi_deatils)

        appointment_details = dict(real_dict_cursor.fetchone())

        # user selected appointment date of the patient
        appointment_dt = appointment_details['timeslot_list']['appointment_date_time']

        # appointment type is taken as 'ivrs' for my operator booked appointments
        appointment_type = "ivrs"

        for department in appointment_details['dept_list'].values():
            if department['selected'] == 1:
                dept_id = department['dept_id']
                break

        for doctor in appointment_details['doctors_list'].values():
            if doctor['selected'] == 1:
                doctor_id = doctor['doctor_id']
                break

        # insert above appointment details into appointment trans table
        sql_parameters_for_inserting_in_appointment_trans = {'patient_id': patient_id, 'appointment_dt': appointment_dt, 'org_id': org_id, 'doctor_id': doctor_id, 'dept_id': dept_id, 'appointment_type': appointment_type}
        real_dict_cursor.execute(query_update_appointment_details_in_appointment_trans, sql_parameters_for_inserting_in_appointment_trans)

        return confirmation_message

    elif int(selected_input_option) == 2:
        sql_parameters_for_cancellation = {'org_id': org_id, 'uid': uid}
        real_dict_cursor.execute(query_to_delete_booking_data_on_cancellation, sql_parameters_for_cancellation)
        return cancellation_message
    else:
        return invalid_input_message


# function that fetches organisation settings for patient id generation
def get_organisation_settings(conn, setting_id, org_id):
    real_dict_cursor = get_real_dict_cursor(conn)
    # In order to generate patient_id for the patient, fetch organisation settings.
    sql_parameters_for_fetching_org_settings = {'setting_id': setting_id, 'org_id': org_id}
    real_dict_cursor.execute(fetch_application_org_settings, sql_parameters_for_fetching_org_settings)
    row = real_dict_cursor.fetchone()
    return row


# function that registers the patient
def register_patient(conn, mobile_no):

    non_real_dict_cursor = get_non_real_dict_cursor(conn)

    # Get all application settings for patient id generation
    row = get_organisation_settings(conn, APPLICATION_SETTINGS_ID, SETTINGS_ORG_ID)
    settings_details = dict(row)
    prefix = settings_details['prefix']
    date_required = settings_details['is_date_required']
    date_format = settings_details['date_format']
    pre_fix_postion = settings_details['pre_fix_position']
    num_length = settings_details['length']
    organization_id = settings_details['org_id']
    type_id = settings_details['setting_id']

    # generating patient id until it gets inserted in patient info ref table
    # below line executes "select public.sp_sequence_id_creation_generic1('1', true, 'yyyymmdd', 'B', 6, 1, 1)::bigint"
    while True:
        non_real_dict_cursor.callproc('public.sp_sequence_id_creation_generic1', (prefix, date_required, date_format, pre_fix_postion, num_length, organization_id, type_id))
        patient_id = int(non_real_dict_cursor.fetchone()[0])

        sql_parameters_for_patient_registration = {'patient_id': patient_id, 'mobile_no': mobile_no}
        try:
            non_real_dict_cursor.execute(query_for_patient_registration, sql_parameters_for_patient_registration)
            break
        except psycopg2.errors.UniqueViolation:
            conn.rollback()

    return patient_id


# maps the current patient to the organisation
def map_patient_to_org(conn, org_id, patient_id):
    non_real_dict_cursor = get_non_real_dict_cursor(conn)
    sql_parameters_for_mapping_patient_to_org = {'patient_id': patient_id, 'org_id': org_id}
    non_real_dict_cursor.execute(query_for_mapping_patient_to_org, sql_parameters_for_mapping_patient_to_org)


#: This method log's the every request given
@app.before_request
def start():
        global response_token
        response_token = str(uuid.uuid4()).upper()
        logger.info("{'transactionId':%s,'systemName':%s,'moduleName':'MyOperator','timeStamp':%s,'apiName':%s,'status':'START','payLoad':[%s]}",response_token, get_computer_name(), time.strftime('%Y-%m-%d %H:%M:%S'), request.url_rule, request.get_json())


#: This method log's the every request on successful completion
@app.after_request
def end(response):
        response.headers['Response_Token'] = response_token
        if response.status_code == 200:
                logger.info("{'transactionId':%s,'systemName':%s,'moduleName':'MyOperator','timeStamp':%s,'apiName':%s,'status':'END','payLoad':[%s]}", response_token, get_computer_name(), time.strftime('%Y-%m-%d %H:%M:%S'), request.url_rule, request.get_json())
        return response


#: This Api takes node id as input and returns corresponding input
@app.route('/myOperatorBookAppointment', methods=['POST'])
def book_appointment():
    try:
        #: get db connection from pool
        conn = threaded_postgres_sql_pool.getconn()

        #: read request data from my operator
        uid = request.form["uid"]
        node_id = request.form['node_id']
        mobile_no = request.form['clid']

        #: fetch the node type and org id for the given node id
        real_dict_cursor = conn.cursor(cursor_factory=RealDictCursor)
        sql_parameters_node_id = {'node_id': node_id}
        real_dict_cursor.execute(query_to_fetch_node_type_and_org_id, sql_parameters_node_id)
        node_type_and_org_id = real_dict_cursor.fetchone()

        org_id = node_type_and_org_id['org_id']
        node_type = node_type_and_org_id['myop_node_type']
        message = ""

        print(node_type)

        #: fetching departments of an organization for given node id
        if node_type == DEPARTMENTS_NODE_TYPE:
            message = fetch_departments_node(conn, org_id, uid, mobile_no)

        #: fetching doctors of a department based on department id
        elif node_type == DOCTORS_NODE_TYPE:
            selected_input_option = request.form['input']
            print(selected_input_option)
            message = fetch_doctors_node(conn, org_id, uid, selected_input_option)

        #: input: It takes doctor selected option
        #: returns: available days of a doctor based on doctor id
        elif node_type == DAYS_NODE_TYPE:
            selected_input_option = request.form['input']
            print(selected_input_option)
            message = fetch_days_node(conn, org_id, uid, selected_input_option)

        #: input: It takes date
        #: returns: timings of a day based on date
        elif node_type == TIME_SLOTS_NODE_TYPE:
            selected_input_option = request.form['input']
            print(selected_input_option)
            message = fetch_timings_node(conn, org_id, uid, selected_input_option)

        #: input: It takes time
        #: returns: book appointment confirmation option if available based on user given time
        elif node_type == BOOK_APPOINTMENT_NODE_TYPE:
            selected_input_option = request.form['input']
            print(selected_input_option)
            message = book_appointment_node(conn, org_id, uid, selected_input_option)

        #: input: It takes confirmation input
        #: returns: book appointment confirmation option if available based on user given time
        elif node_type == CONFIRM_APPOINTMENT_NODE_TYPE:
            selected_input_option = request.form['input']
            print(selected_input_option)
            message = confirm_appointment_node(conn, org_id, uid, selected_input_option, mobile_no)

        conn.commit()
        threaded_postgres_sql_pool.putconn(conn)

        #   : It checks for weather flow need to be continue or have to jump
        success_response['value'] = message
        return jsonify(success_response), 200
    except Exception:
        threaded_postgres_sql_pool.putconn(conn)
        # This is logged only at the time of Exception
        logger.info(
            "{'transactionId':%s,'systemName':%s,'moduleName':'MyOperator','timeStamp':%s,'apiName':%s,'status':'ERROR','exception':%s,'payLoad':[%s]}",
            response_token, get_computer_name(), time.strftime('%Y-%m-%d %H:%M:%S'), request.url_rule, traceback.format_exc(), "")
        response = {'responseCode': "E400", 'responseMessage': "OPERATION FAILED GENERIC MESSAGE", 'data': ''}
        return jsonify(response), 400


if __name__ == '__main__':
    app.run(host="0.0.0.0", port="5000", debug=True)
